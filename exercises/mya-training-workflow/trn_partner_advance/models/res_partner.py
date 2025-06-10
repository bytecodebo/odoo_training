import random

from odoo import api, fields, models


SIAT_TD_CI= 1
RND_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F']


class ResPartner(models.Model):
    _inherit = 'res.partner'

    siat_doc_type_id = fields.Many2one(comodel_name="siat.document.type", string="Doc. type", required=False, )
    siat_extension_di = fields.Char(string="Extension", required=False, )
    full_vat = fields.Char(string="No. Document", compute="_compute_full_vat")
    partner_code = fields.Char(string="Code", required=False, )

    @api.depends('siat_doc_type_id', "siat_extension_di", "vat")
    def _compute_full_vat(self):
        for rec in self:
            full_vat = rec.vat
            if rec.siat_doc_type_id and rec.siat_doc_type_id.code_classificator == SIAT_TD_CI and rec.company_type == 'person' \
                and rec.siat_extension_di:
                full_vat = "%s-%s" % (full_vat, rec.siat_extension_di)
            if full_vat != rec.full_vat:
                rec.full_vat = full_vat

    def action_create_partner_demos(self):
        partner_ids = self.env['res.partner'].search([('company_id', '=', self.env.company.id)])
        max_contacts = self._context.get('ctx_partner_qty_demo', 20)
        init = len(partner_ids)
        vals = []
        doc_type_ci = self.env.ref('trn_partner_advance.siat_dti_ci', raise_if_not_found=False).id
        doc_type_nit = self.env.ref('trn_partner_advance.siat_dti_nit', raise_if_not_found=False).id
        sequence_code_id = self.env.ref('trn_partner_advance.seq_partner_advance_code', raise_if_not_found=False)
        max_letter = len(RND_LETTERS)
        for x in range(init, init + max_contacts):
            is_company = bool(random.randint(0, 1))
            id_doc_type = doc_type_nit if is_company else doc_type_ci
            complement = None
            sequence = sequence_code_id.next_by_id(sequence_date=fields.Datetime.now())
            if not is_company:
                if bool(random.randint(0,1)): # Para asignarle complemento randomicamente
                    nro = random.randint(1, 5)
                    letter = random.randint(0, max_letter-1)
                    complement = "%s%s" % (nro,RND_LETTERS[letter])
            val = self._get_values_partner_demos(sequence,x, is_company, id_doc_type, complement)
            vals.append(val)
        new_partner_ids = self.env['res.partner'].sudo().create(vals)
        self._cr.commit()
        for partner in new_partner_ids:
            # partner._onchange_name()
            partner.onchange_company_type()

    def _get_values_partner_demos(self, sequence, start,is_company, id_doc_type, complement=None):
        customer = "%s %s" % ("Empresa" if is_company else "Cliente", start + 1000)
        company_type = "company" if is_company else "person"
        return {
            'name': customer,
            'partner_code': sequence,
            'country_id': self.env.company.country_id.id,
            'vat': "6234%s" % (start + 1013),
            'siat_doc_type_id': id_doc_type ,
            'siat_extension_di': complement,
            'is_company': is_company,
            'company_id': self.env.company.id,
            'state_id': self.env.company.state_id.id,
            'email': "cliente.%s@myapps.com.bo" % (start + 1000),
            # 'partner_code':(x + 1000),
            'company_type': company_type,
        }

    def action_pre_approval(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("trn_partner_advance.action_open_pre_approve")
        return action

    def action_load_massive_customer(self):
        self.ensure_one()
        action = self.env['ir.actions.actions']._for_xml_id("trn_partner_advance.action_load_data_huge_wizard")
        return action
