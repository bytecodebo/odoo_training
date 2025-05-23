from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    siat_doc_type_id = fields.Many2one(comodel_name="siat.document.type", string="Doc. type", required=False, )
    siat_extension_di = fields.Char(string="Extension", required=False, )
    full_vat = fields.Char(string="No. Document", compute="_compute_full_vat")

    @api.depends('siat_doc_type_id', "siat_extension_di", "vat")
    def _compute_full_vat(self):
        for rec in self:
            full_vat = rec.vat
            if rec.siat_doc_type_id and rec.siat_doc_type_id.code_classificator == 1 and rec.company_type == 'person' \
                and rec.siat_extension_di:
                full_vat = "%s-%s" % (full_vat, rec.siat_extension_di)
            if full_vat != rec.full_vat:
                rec.full_vat = full_vat

