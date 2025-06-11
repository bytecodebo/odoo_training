
from openupgradelib import openupgrade

_module_to_install = 'trn_main_setting'

def install_module(env, module):
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE ir_module_module
        SET state='to install'
        WHERE name = '{}' AND state='uninstalled'""".format(module),
    )


@openupgrade.migrate()
def migrate(env, version):

    if not openupgrade.is_module_installed(env.cr, _module_to_install):
        install_module(env, _module_to_install)