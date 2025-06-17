# -*- coding: utf-8 -*-
import odoo
import json
import requests
import sys
from odoo import http, _

from odoo.addons.web.controllers import main as report
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError, MissingError
from odoo.http import Controller, request, Response, route, serialize_exception as _serialize_exception
import base64
import odoo.modules.registry

db_list = http.db_list

db_monodb = http.db_monodb


class TcpReportCreator(http.Controller):

    @http.route('/web/test', type='http', auth="public")
    def download_document(self, model, id, **kw):
        #         get the string html from database and return it
        test_report = ""
        if request.env[model].browse(int(id)).test_html:
            test_report = request.env[model].browse(int(id)).test_html

        return test_report


# class PortalAccount(CustomerPortal):
#
#     def _prepare_home_portal_values(self):
#         values = super(PortalAccount, self)._prepare_home_portal_values()
#         invoice_count = request.env['account.move'].search_count([
#             ('type', 'in', ('out_invoice', 'in_invoice', 'out_refund', 'in_refund', 'out_receipt', 'in_receipt')),
#         ]) if request.env['account.move'].check_access_rights('read', raise_exception=False) else 0
#         values['invoice_count'] = invoice_count
#         return values
#
#      # ------------------------------------------------------------
#     # My Invoices
#      # ------------------------------------------------------------
#
#     def _invoice_get_page_view_values(self, invoice, access_token, **kwargs):
#         values = {
#             'page_name': 'invoice',
#             'invoice': invoice,
#         }
#         return self._get_page_view_values(invoice, access_token, values, 'my_invoices_history', False, **kwargs)
#
#     @http.route(['/my/invoices', '/my/invoices/page/<int:page>'], type='http', auth="user", website=True)
#     def portal_my_invoices(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
#         values = self._prepare_portal_layout_values()
#         AccountInvoice = request.env['account.move']
#
#         domain = [('type', 'in', ('out_invoice', 'out_refund', 'in_invoice', 'in_refund', 'out_receipt', 'in_receipt'))]
#
#         searchbar_sortings = {
#             'date': {'label': _('Invoice Date'), 'order': 'invoice_date desc'},
#             'duedate': {'label': _('Due Date'), 'order': 'invoice_date_due desc'},
#             'name': {'label': _('Reference'), 'order': 'name desc'},
#             'state': {'label': _('Status'), 'order': 'state'},
#         }
#         # default sort by order
#         if not sortby:
#             sortby = 'date'
#         order = searchbar_sortings[sortby]['order']
#
#         archive_groups = self._get_archive_groups('account.move', domain) if values.get('my_details') else []
#         if date_begin and date_end:
#             domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]
#
#         # count for pager
#         invoice_count = AccountInvoice.search_count(domain)
#         # pager
#         pager = portal_pager(
#             url="/my/invoices",
#             url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
#             total=invoice_count,
#             page=page,
#             step=self._items_per_page
#         )
#         # content according to pager and archive selected
#         invoices = AccountInvoice.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
#         request.session['my_invoices_history'] = invoices.ids[:100]
#
#         values.update({
#             'date': date_begin,
#             'invoices': invoices,
#             'page_name': 'invoice',
#             'pager': pager,
#             'archive_groups': archive_groups,
#             'default_url': '/my/invoices',
#             'searchbar_sortings': searchbar_sortings,
#             'sortby': sortby,
#         })
#         return request.render("account.portal_my_invoices", values)
#
#     @http.route(['/my/invoices/<int:invoice_id>'], type='http', auth="public", website=True)
#     def portal_my_invoice_detail(self, invoice_id, access_token=None, report_type=None, download=False, **kw):
#         try:
#             invoice_sudo = self._document_check_access('account.move', invoice_id, access_token)
#         except (AccessError, MissingError):
#             return request.redirect('/my')
#
#         if report_type in ('html', 'pdf', 'text'):
#             return self._show_report(model=invoice_sudo, report_type=report_type, report_ref='account.account_invoices', download=download)
#
#         values = self._invoice_get_page_view_values(invoice_sudo, access_token, **kw)
#         request.session.authenticate("m2m_roger_v2", "yobi31018812@gmail.com", "admin123*")
#         acquirers = values.get('acquirers')
#         if acquirers:
#             country_id = values.get('partner_id') and values.get('partner_id')[0].country_id.id
#             values['acq_extra_fees'] = acquirers.get_acquirer_extra_fees(invoice_sudo.amount_residual, invoice_sudo.currency_id, country_id)
#
#         return request.render("account.portal_invoice_page", values)
#
#      # ------------------------------------------------------------
#     # My Home
#      # ------------------------------------------------------------
#
#     def details_form_validate(self, data):
#         error, error_message = super(PortalAccount, self).details_form_validate(data)
#         # prevent VAT/name change if invoices exist
#         partner = request.env['res.users'].browse(request.uid).partner_id
#         if not partner.can_edit_vat():
#             if 'vat' in data and (data['vat'] or False) != (partner.vat or False):
#                 error['vat'] = 'error'
#                 error_message.append(_('Changing VAT number is not allowed once invoices have been issued for your account. Please contact us directly for this operation.'))
#             if 'name' in data and (data['name'] or False) != (partner.name or False):
#                 error['name'] = 'error'
#                 error_message.append(_('Changing your name is not allowed once invoices have been issued for your account. Please contact us directly for this operation.'))
#             if 'company_name' in data and (data['company_name'] or False) != (partner.company_name or False):
#                 error['company_name'] = 'error'
#                 error_message.append(_('Changing your company name is not allowed once invoices have been issued for your account. Please contact us directly for this operation.'))
#         return error, error_message
#


class PreviewReports(report.Home):

    def dw_file(self, xmlid=None, model='ir.attachment', id=None, field='datas',
                filename=None, filename_field='name', unique=None, mimetype=None,
                download=None, data=None, token=None, access_token=None, **kw):

        status, headers, content = request.env['ir.http'].binary_content(
            xmlid=xmlid, model=model, id=id, field=field, unique=unique, filename=filename,
            filename_field=filename_field, download=download, mimetype=mimetype, access_token=access_token)

        if status != 200:
            return request.env['ir.http']._response_by_status(status, headers, content)
        else:
            content_base64 = base64.b64decode(content)
            headers.append(('Content-Length', len(content_base64)))
            response = request.make_response(content_base64, headers)
        if token:
            response.set_cookie('fileToken', token)
        return response

    @http.route('/invoice/<string:filename>', type='http', auth="none", cors="*")
    def invoice(self, filename, **kw):

        # AUTH_URL = 'http://144.91.78.229:8019/web/session/authenticate/'
        AUTH_URL = 'http://localhost:8111/web/session/authenticate/'
        headers = {'Content-type': 'application/json'}

        data = {
            'params': {
                "login": "fernando@m2m.bo",
                "password": "admin123*",
                "db": "m2m_roger_v2"
            }
        }

        res = requests.post(
            AUTH_URL,
            data=json.dumps(data),
            headers=headers
        )
        cookies = res.cookies
        # -print(cookies)
        nresp = None
        try:
            registry = odoo.modules.registry.Registry("m2m_roger_v2")
            # -print("before")
            with registry.cursor() as cr:
                cr.execute("""SELECT id, name
                                    FROM ir_attachment
                                    WHERE name = %s
                            """, (filename,))
                row = cr.fetchone()
                if row and row[0]:
                    reslt = row[0]
                    name = row[1]
                    nresp = json.dumps(reslt)
                    idattch = int(nresp)
                    request.session.authenticate("m2m_roger_v2", "fernando@m2m.bo", "admin123*")
                    status, headers, content = request.env['ir.http'].binary_content(
                        xmlid=None, model='ir.attachment', id=idattch, field='datas', unique=None, filename=filename,
                        filename_field='name', download=None, mimetype=None, access_token=None)
                    # -print("sss " + str(idattch))
                    if status != 200:
                        # -print("entro")
                        return request.env['ir.http']._response_by_status(status, headers, content)
                    else:
                        # -print("else! 200")
                        content_base64 = base64.b64decode(content)
                        headers.append(('Content-Length', len(content_base64)))
                        response = request.make_response(content_base64, headers)
                    token = None
                    if token:
                        response.set_cookie('fileToken', token)
                    return response
                else:
                    reslt = "xyz"
        except Exception as e:
            se = _serialize_exception(e)
