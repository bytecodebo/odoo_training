# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from ast import literal_eval
from pprint import pprint
from odoo import models, fields


class StockMove(models.Model):
    _inherit = 'stock.move'

    account_grp_move_id = fields.Many2one('account.move', string='AM grouped', auto_join=True, ondelete="cascade")

    def _prepare_account_move_line(self, qty, cost, credit_account_id, debit_account_id, svl_id, description):
        res = super()._prepare_account_move_line(qty, cost, credit_account_id, debit_account_id, svl_id, description)
        for line in res:
            line[2]['svl_grp_id'] = svl_id
            line[2]['stm_grp_id'] = self.id
            line[2]['stp_grp_id'] = self.picking_id.id
        return res 
    
    def _prepare_account_move_vals(self, credit_account_id, debit_account_id, journal_id, qty, description, svl_id, cost):
        vals = super()._prepare_account_move_vals(credit_account_id, debit_account_id, journal_id, qty, description, svl_id, cost)
        vals.update({
            'stock_grp_picking_id': self.picking_id.id,            
        })
        return vals