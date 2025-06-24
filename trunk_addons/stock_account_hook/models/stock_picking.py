# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from ast import literal_eval
from pprint import pprint
from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    account_move_ids = fields.One2many('account.move', 'stock_grp_picking_id', string="AM grouped")
    enable_grouped_moves = fields.Boolean(compute="_compute_enable_grouped_moves", default=False, store=True)
    # account_grp_move_id = fields.Many2one('account.move', 'Journal Entry', readonly=True, check_company=True)
    
    def action_view_account_moves(self):
        self.ensure_one()
        form_view_name = "account.view_move_form"
        result = self.env["ir.actions.act_window"]._for_xml_id(
            "account.action_move_journal_line"
        )
        if len(self.account_move_ids) > 1:
            result["domain"] = "[('id', 'in', %s)]" % self.account_move_ids.ids
        else:
            form_view = self.env.ref(form_view_name)
            result["views"] = [(form_view.id, "form")]
            result["res_id"] = self.account_move_ids.id
        return result
    
    @api.depends('picking_type_id', 'state', 'company_id')
    def _compute_enable_grouped_moves(self):
        for rec in self:
            enable_grouped_moves = rec.enable_grouped_moves            
            if rec.picking_type_code in ['incoming'] and rec.company_id.svl_grouped_move_purchase:
                enable_grouped_moves = True
            elif rec.picking_type_code in ['outgoing'] and rec.company_id.svl_grouped_move_sale:
                enable_grouped_moves = True
            if enable_grouped_moves != rec.enable_grouped_moves:
                rec.enable_grouped_moves = enable_grouped_moves
                
    def action_generate_unique_entry(self):
        am_vals = []
        
        stock_pickings = {}        
        for stp in self:   
            unique_vals = []         
            counter = 1    
            stm_vals = []
            svl_vals = []        
            if not stp.id in stock_pickings:
                stock_pickings[stp.id] = []
            for rec in stp.move_ids:                
                print('stock move: %s' % rec.id, rec.product_id.id)
                stm_vals.append(rec.id)
                for svl in rec.stock_valuation_layer_ids:
                    svl_vals.append(svl.id)
                    move = svl.stock_move_id
                    if not move:
                        move = svl.stock_valuation_layer_id.stock_move_id
                    am_vals += move._account_entry_move(svl.quantity, svl.description, svl.id, svl.value)                    
                    if counter == 1:
                        unique_vals.append(am_vals[0])
                    else:
                        unique_vals[0]['line_ids'] += am_vals[counter - 1]['line_ids']
                        
                    #print(" svl: %s \n" % svl.id,unique_vals[0]['line_ids'], "\n")
                    # print(" svl: %s \n" % svl.id,am_vals[counter - 1]['line_ids'], "\n")
                    counter +=1                
            # unique_vals[0]['stock_valuation_layer_ids'] =[(6, None, svl_vals)]
            # unique_vals[0]['stock_grp_move_ids'] =[(6, None, stm_vals)]
            unique_vals[0]['ref'] =stp.name
            stock_pickings[stp.id] = unique_vals
        for am in am_vals:
            print("\n\n am: %s \n\n" % am)
        #print("\n\n Account move start \n\n")
        # pprint(am_vals)
        #print("\n\n Account move end\n\n")
        print("\n\n Account move unique start \n\n")
        pprint(stock_pickings, indent=2, width=180)
        print("\n\n Account move unique end\n\n")