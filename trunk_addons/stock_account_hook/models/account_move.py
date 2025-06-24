# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from ast import literal_eval
from pprint import pprint
from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    stock_grp_picking_id = fields.Many2one('stock.picking', string='Stock Picking')
    # stock_grp_picking_ids = fields.One2many('stock.picking', 'account_grp_move_id', string='Stock Pickings')
    stock_grp_move_ids = fields.One2many('stock.move', 'account_grp_move_id', string='Stock Moves')
    

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    svl_grp_id = fields.Many2one('stock.valuation.layer',string='Svl')
    stm_grp_id = fields.Many2one('stock.move',string='Stm')
    stp_grp_id = fields.Many2one('stock.picking',string='Stp')
