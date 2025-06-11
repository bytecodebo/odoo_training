from contextlib import contextmanager
from xmlrpc.client import ServerProxy
import odoorpc
# from ..tools.api_peeko import CnxAPI


class RPCProxyOne(object):

    def __init__(self, server, resource):
        """Class to store one RPC proxy server."""
        self.server = server
        server_url = server.server_url
        if not 'http' in server_url:
            server_url = "http://%s" % server_url
        local_url = "%s:%d/xmlrpc/common" % (server_url, server.server_port,)
        rpc = ServerProxy(local_url)
        self.uid = rpc.login(server.server_db, server.login, server.password)
        local_url = "%s:%d/xmlrpc/object" % (
            server_url,
            server.server_port,
        )
        self.rpc = ServerProxy(local_url)
        self.resource = resource

    def __getattr__(self, name):
        return lambda *args, **kwargs: self.rpc.execute(
            self.server.server_db,
            self.uid,
            self.server.password,
            self.resource,
            name,
            *args
        )


class RPCProxyOneV2(object):

    def __init__(self, server, resource):
        """Class to store one RPC proxy server."""
        self.server = server
        server_url = server.server_url
        if not 'http' in server_url:
            server_url = "http://%s" % server_url
        local_url = "%s:%d/xmlrpc/2/common" % (server_url, server.server_port,)
        rpc = ServerProxy(local_url)
        if resource and resource == 'server_data':
            server_data = rpc.version()
            db_url = "%s:%d/xmlrpc/2/db" % (server_url, server.server_port,)
            rpc_db = ServerProxy(db_url)
            server_dbs = rpc_db.list()
            server_data['db_list'] = server_dbs
            self.server_data = server_data
        # elif resource and resource == 'db_list':
        # local_url = "%s:%d/xmlrpc/2/db" % (server_url, server.server_port,)
        # rpc = ServerProxy(local_url)
        # self.db_list = rpc.list()
        else:
            self.uid = rpc.authenticate(server.server_db, server.login, server.password, {})
            local_url = "%s:%d/xmlrpc/2/object" % (
                server_url,
                server.server_port,
            )
            self.rpc = ServerProxy(local_url)
        self.resource = resource

    def __getattr__(self, name):
        if name == 'get_version_data':
            return self.server_data
        else:
            return lambda *args, **kwargs: self.rpc.execute_kw(
                self.server.server_db,
                self.uid,
                self.server.password,
                self.resource,
                name,
                [*args],
                **kwargs
            )


class RPCOdooProxy(object):
    __slots__ = ['_func', '_args', '_kwargs', '_options', '_pool', '_user_id', '_resource']
    _fields = ['server', '_user_id', '_resource', '_pool']
    _server_fields = ['server_url', 'server_port', 'login', 'password', 'provider', 'server_db']

    # _options = {}
    # def __init__(self, func, *args, **kwargs):
    #     # bypass own __setattr__
    #     object.__setattr__(self, '_func', func)
    #     object.__setattr__(self, '_args', args)
    #     object.__setattr__(self, '_kwargs', kwargs)

    def __init__(self, server, resource=None):
        kwargs = {}
        for k in self._server_fields:
            if k != 'server':
                kwargs[k] = server[k]
                # self.__setattr__(self, k, kwargs[k])
        self._options = kwargs or {}
        srv_url = str(server.server_url)
        protocol = 'jsonrpc'
        if 'https://' in srv_url:
            protocol += '+ssl'
            srv_url = srv_url.replace('https://', '')
        elif 'http://' in srv_url:
            srv_url = srv_url.replace('http://', '')
        elif 'http' in srv_url:
            srv_url = srv_url.replace('http', '')
        srv_url = srv_url.replace('//', '')
        self._pool = odoorpc.ODOO(host=srv_url, port=server.server_port, protocol=protocol)
        # if resource and resource == 'server_data':
        #    server_data = self.pool.version()
        #    server_dbs = self.pool.db.list()
        #    server_data['db_list'] = server_dbs
        #    server_data = server_data
        # if not self._user_id:
        self._pool.login(server.server_db, server.login, server.password)
        self._user_id = self._pool.env.user
        #     if user_id:
        #         pool.login(server.server_db, server.login, server.password)
        #         self.user_id = pool.env.user
        #     self.pool = pool
        self._resource = resource

    def __getitem__(self, key):
        return self._options[key]

    def __setitem__(self, key, value):
        self._options[key] = value

    def __call__(self, name):
        if name == 'check_login':
            return self._user_id
        else:
            return lambda *args, **kwargs: self.call_odoo_kw(self._resource, name, *args, **kwargs)

    def __getattr__(self, name):
        if name == 'check_login':
            return self._user_id
        else:
            return lambda *args, **kwargs: self.call_odoo_kw(self._resource, name, *args, **kwargs)

    def call_odoo_kw(self, resource, name, *args, **kwargs):
        """ Invoke the given method ``name`` on the recordset ``model``. """
        real_method = resource or name
        method = None
        result = []
        if hasattr(self._pool, real_method):
            method = getattr(self._pool, real_method)
            if args and kwargs:
                result = method(*args, **kwargs)
            elif args:
                result = method(*args)
            elif kwargs:
                result = method(None, **kwargs)
        elif name == 'get_version_data':
            result = self._pool.json('/jsonrpc', params={'service': 'common', 'method': 'version', 'args': []})
            server_dbs = self._pool.db.list()
            result = result.get('result', {})
            result.update({'db_list': server_dbs})
        else:
            model = resource
            if args and kwargs:
                method = getattr(self._pool, 'execute_kw')
                result = method(model, name, args, kwargs)
            elif args:
                method = getattr(self._pool, 'execute')
                result = method(model, name, *args)
            elif kwargs:
                method = getattr(self._pool, 'execute_kw')
                result = method(model, name, None, kwargs)

        return result


class RPCProxy(object):
    """Class to store RPC proxy server."""

    def __init__(self, server):
        self.server = server

    def get(self, resource):
        if self.server.provider == 'xmlrpc':
            return RPCProxyOne(self.server, resource)
        elif self.server.provider == 'xmlrpc2':
            return RPCProxyOneV2(self.server, resource)
        else:
            return RPCOdooProxy(self.server, resource)


class OdooRPCx(object):
    def __init__(self, server):
        params = server.get_conx()
        self.server = odoorpc.ODOO(**params.start)
        self.server.login(**params.credentials)

    def get(self, model):
        return self.server.env[model]


# def get_conx_peeko(model=None, **kwargs):
#    cx = CnxAPI(model, **kwargs)
#    return cx


# def conx_api_peeko(model=None, **kwargs):
#     conx = CnxAPI(model, **kwargs)
#     return conx
#

if __name__ == '__main__':
    kwargs = {'db': 'cruzimex_tst_test',
              'password': 'd657a400db4a3c65231e107e45dddb723a0d8538', 'server': 'http://95.111.253.164:9621/jsonrpc',
              'user': 'soporte'}
    # pool1 = conx_api_peeko('account.move', **kwargs)
    # print(pool1.api.server_version)
