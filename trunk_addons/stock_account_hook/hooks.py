# Copyright 2020 ForgeFlow, S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from collections import defaultdict
from datetime import datetime

from odoo import _
from odoo.tools import float_is_zero

from odoo.addons.stock_account.models.stock_move import StockMove
from odoo.addons.stock_account.models.stock_valuation_layer import StockValuationLayer


# flake8: noqa: C901
def post_load_hook():
    def _validate_accounting_entries_new(self):
        am_vals = []
        aml_to_reconcile = defaultdict(set)
        enabled_types = {}
        for svl in self:
            if not svl.with_company(svl.company_id).product_id.valuation == 'real_time':
                continue
            if svl.currency_id.is_zero(svl.value):
                continue
            move = svl.stock_move_id
            if not move:
                move = svl.stock_valuation_layer_id.stock_move_id
            am_vals += move.with_company(svl.company_id)._account_entry_move(svl.quantity, svl.description, svl.id, svl.value)
            if not move.picking_id.id in enabled_types:
                enabled_types[move.picking_id.id] = {}
            enabled_types[move.picking_id.id].update({
                move.id: 'in' if not move.location_id._should_be_valued() else 'out'
            })
        if am_vals:
            picking_ids = self.stock_move_id.mapped('picking_id')
            am_new_vals = []
            account_moves = self.env['account.move']
            for am in am_vals:                
                picking_id = picking_ids.filtered(lambda x: x.id == am['stock_grp_picking_id'])
                stm_id = (self.mapped('stock_move_id') + self.stock_valuation_layer_id.mapped('stock_move_id')).filtered(lambda x: x.picking_id.id == picking_id.id)
                # value_type = enabled_types[picking_id.id][stm_id[0].id]
                value_type = enabled_types.get(picking_id.id, {}).get(stm_id[0].id) if len(stm_id) > 0 else ''
                enable_grouped = False
                if value_type == 'in' and picking_id.company_id.svl_grouped_move_purchase:
                    enable_grouped = True 
                elif value_type == 'out' and picking_id.company_id.svl_grouped_move_sale:
                    enable_grouped = True
                if not enable_grouped:
                    am_new_vals += [am]
                    continue
                am_id = None
                if picking_id:
                    am_id = self.env['account.move'].sudo().search([('stock_grp_picking_id', '=',picking_id.id), ('state', '=', 'draft')])
                if not am_id:
                    am.update({'ref': picking_id.name ,
                               'stock_valuation_layer_ids': [(6, None,self.ids)],
                               'stock_grp_move_ids': [(6, None, self.mapped('stock_move_id').ids)]
                               })
                                       
                    account_moves |= self.env['account.move'].sudo().create(am)
                else:
                    am_id.write({
                        'line_ids': am['line_ids'],
                        'stock_grp_move_ids': [(6, None, self.mapped('stock_move_id').ids)]
                    })
            for acm in account_moves:
                stm_count = len(acm.stock_grp_move_ids) or 0
                spm_count = len(acm.stock_grp_picking_id.move_ids) or 0
                if stm_count and spm_count and stm_count == spm_count:
                    acm._post()
            if am_new_vals:                
                account_moves = self.env['account.move'].sudo().create(am_new_vals)
                account_moves._post()
            # for acm in account_moves:
            #    acm.write({'stock_grp_move_ids': [(6, None, self.mapped('stock_move_id').ids)]})
            # account_moves._post()
        for svl in self:
            move = svl.stock_move_id
            product = svl.product_id
            if svl.company_id.anglo_saxon_accounting:
                move._get_related_invoices()._stock_account_anglo_saxon_reconcile_valuation(product=product)
            for aml in (move | move.origin_returned_move_id)._get_all_related_aml():
                if aml.reconciled or aml.move_id.state != "posted" or not aml.account_id.reconcile:
                    continue
                aml_to_reconcile[(product, aml.account_id)].add(aml.id)
        for aml_ids in aml_to_reconcile.values():
            self.env['account.move.line'].browse(aml_ids).reconcile()

    if not hasattr(StockValuationLayer, "_validate_accounting_entries_original"):
        StockValuationLayer._validate_accounting_entries_original = StockValuationLayer._validate_accounting_entries
    StockValuationLayer._validate_accounting_entries = _validate_accounting_entries_new
