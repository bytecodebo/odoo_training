import math

from odoo import fields, models, api
from odoo.addons.account.models.account_tax import AccountTax as AccountTaxOdoo
from odoo.addons.trn_sale_order.models.account_tax import AccountTax as AccountTaxTrn


def post_load_hook():
    # sobreescribir methods

    def _compute_amount_new(self, base_amount, price_unit, quantity=1.0, product=None, partner=None, fixed_multiplicator=1, **kwargs):
        """ Returns the amount of a single tax. base_amount is the actual amount on which the tax is applied, which is
            price_unit * quantity eventually affected by previous taxes (if tax is include_base_amount XOR price_include)
        """
        value = 0.0
        if kwargs.get('ctx_dscto_linea', False):
            prec_decim  = 5
        prec_decim = 2
        if kwargs.get('ctx_run_compute_amount_bob', False):
            return AccountTaxTrn._reprocess_compute_amount(base_amount, price_unit, quantity,product, partner, fixed_multiplicator, **kwargs)

        return AccountTaxTrn._compute_amount_original()

    if not hasattr(AccountTaxTrn, "_compute_amount_original"):
        AccountTaxTrn._compute_amount_original = AccountTaxTrn._compute_amount

    AccountTaxTrn._compute_amount = _compute_amount_new

