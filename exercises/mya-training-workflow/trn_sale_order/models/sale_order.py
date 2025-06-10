from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_edited_data_invoice(self):
        for sale in self:
            sale.is_edited_invoice = True

    is_edited_invoice = fields.Boolean(compute=_get_edited_data_invoice)
    business_name = fields.Char('Business Name', default="")
    vat = fields.Char(string='NIT/CI', index=True,
                      help="The Tax Identification Number. Complete it if the contact is subjected to government "
                           "taxes. Used in some legal statements.")

    def action_download_invoice(self):
        data = self.invoice_ids
        return self.env.ref('account.account_invoices').report_action(data)

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['amount_untaxed'] = self.amount_untaxed
        invoice_vals['amount_tax'] = self.amount_tax
        invoice_vals['business_name'] = self.business_name or self.partner_id.name
        invoice_vals['vat'] = self.vat or self.partner_id.vat or '0'

        return invoice_vals
