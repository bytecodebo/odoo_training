from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    file_store = fields.Char(string="File Store", default='/tmp/')
    # active = fields.Boolean(default=True)


# configuration for report
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    file_store = fields.Char(related='company_id.file_store', readonly=False)

    
    

