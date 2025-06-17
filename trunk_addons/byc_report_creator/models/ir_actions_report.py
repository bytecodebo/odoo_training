# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import lxml.html
from odoo import api, fields, models, tools, _
from lxml import etree


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    print_header = fields.Boolean(default=True)
    print_footer = fields.Boolean(default=True)
    render_pdfkit = fields.Boolean(default=False)

    def _render_template(self, template, values=None):
        if values is None:
            values = {}
        values.update(
            print_header='1' if self.print_header else '0',
            print_footer='1' if self.print_footer else '0',
        )
        return super(IrActionsReport, self)._render_template(template=template, values=values)

    def _render_qweb_pdf(self, report_ref, res_ids=None, data=None):
        if not self.env.context.get("res_ids"):
            return super(IrActionsReport, self.with_context(res_ids=res_ids))._render_qweb_pdf(
                report_ref, res_ids=res_ids, data=data)
        return super(IrActionsReport, self)._render_qweb_pdf(
            report_ref, res_ids=res_ids, data=data
        )

    @api.model
    def _render_qweb_html(self, docids, data=None):
        """This method generates and returns html version of a report.
        """
        if not data:
            data = {}
        rep_model = data.get('rep_model', {})
        rep_model.update({
            'print_header': '1' if self.print_header else '0',
            'print_footer': '1' if self.print_footer else '0',
        })
        data.update(rep_model)
        return super(IrActionsReport, self)._render_qweb_html(docids, data=data)

    def _get_readable_fields(self):
        return super()._get_readable_fields() | {"print_header",
                                                 "print_footer"}
