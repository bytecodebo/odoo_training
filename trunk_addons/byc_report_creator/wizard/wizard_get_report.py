import base64

from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _, exceptions
from odoo.exceptions import Warning
from datetime import date, datetime


class WizardGetReport(models.TransientModel):
    _name = "wizard.get.report"
    _description = "Get Report"

    @api.model
    def _get_domain_company_partners(self):
        company_id = self.company_id or self.env.company
        domain = [('company_id', 'in', [False, company_id.id]), ('is_company', '=', True)]
        if company_id:
            domain += [('id', '=', company_id.partner_id.id)]
        partner_ids = self.env['res.partner'].search(domain)
        if partner_ids:
            return "[('id', 'in', %s)]" % partner_ids.ids
        return []

    name = fields.Many2one("report.definition", name="Report Name")
    ext = fields.Selection(related='name.export_as')
    # branch_id = fields.Many2many('company.branches',
    #                             string='Branch')
    start_date = fields.Date(string="Start Date",
                             default=lambda self: fields.Date.to_string(date.today().replace(day=1)))
    end_date = fields.Date(string="End Date", default=lambda self: fields.Date.to_string(
        (datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()))
    company_id = fields.Many2one('res.company', default=lambda x: x.env.company)
    partner_id = fields.Many2one('res.partner', default=lambda x: x.env.company.partner_id,
                                 domain=_get_domain_company_partners)
    print_header = fields.Boolean('Print Header', default=False, help="Only works with txt File")
    separator = fields.Selection([(",", "Comma"), ("|", "Pipe"), ("TAB", "TAB"), (" ", "Space")], default=",",
                                 help="Only works with txt File")
    paired_columns = fields.Boolean('Paired Columns', default=True, help="Only works with txt File")
    filecontent = fields.Binary()

    def get_report(self):
        # define data that tdo generate report
        format_date = "%Y-%m-%d"
        if datetime.strptime(str(self.end_date), format_date) < datetime.strptime(str(self.start_date), format_date):
            raise Warning("End date should be lower than start date")

        data = self._get_filters()
        #         call function generte report in report result to generate report
        self.env['report.result'].generate_report(data)

    def generate_report(self):
        format_date = "%Y-%m-%d"
        if datetime.strptime(str(self.end_date), format_date) < datetime.strptime(str(self.start_date), format_date):
            raise Warning("End date should be lower than start date!")

        if not self.separator:
            raise Warning(_("Select a separator please!"))
        data = self._get_filters()

        file_data, report_name, ext = self.env['report.result'].generate_report_v2(data)

        if not file_data or len(file_data) <= 0:
            raise Warning("There is no data to generate file!")
        else:
            self.filecontent = base64.b64encode(file_data)
            return {
                'type': 'ir.actions.act_url',
                'url': "web/content/?model=wizard.get.report&id=" + str(self.id) +
                       "&field=filecontent&download=true&filename=" + report_name,
                'target': 'self',
            }

    def _get_filters(self):
        data = {"start_date": str(self.start_date), "end_date": str(self.end_date),
                "partner_id": str(self.partner_id.id), 'report_def_obj': self.name, 'print_header': self.print_header,
                'separator': self.separator, 'paired_columns': self.paired_columns}

        return data
