# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_is_zero

class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'
    
    final_cost_lines = fields.One2many(
        'stock.final.cost.lines', 'cost_id', 'Final Cost Lines',
        states={'done': [('readonly', True)]})
    
    def _get_targeted_product_ids(self):
        product_ids = []
        #if product_id:
         #   section_ids.append(section_id)
        #product_ids.extend(self.mapped(self.picking_ids.move_lines.product_id).ids)
        for product in self.picking_ids.move_lines.product_id:
            if not product in product_ids:
                product_ids.extend(product)
        #product_ids = self.picking_ids.move_lines.product_id.mapped('id')
        
        #product_ids = self.mapped(self.picking_ids.move_lines.product_id.id)
        return product_ids
    
    def get_product_final_cost_lines(self):
        self.ensure_one()
        lines = []

        for product in self._get_targeted_product_ids():
            vals = {
                'product_id': product.id,
            }
            lines.append(vals)
        return lines
            
    def compute_landed_cost(self):
        res = super(StockLandedCost, self).compute_landed_cost()
        fcLines = self.env['stock.final.cost.lines']
        fcLines.search([('cost_id', 'in', self.ids)]).unlink()
        #for product in _get_targeted_product_ids():
        #for cost in self.filtered(lambda cost: cost._get_targeted_move_ids()):
        all_final_cost_line_values = self.get_product_final_cost_lines()
        for line in all_final_cost_line_values:
            line.update({
                'cost_id': self.id, 
            })
            self.env['stock.final.cost.lines'].create(line)
        return res
    
class FinalCostLines(models.Model):
    _name = 'stock.final.cost.lines'
    _description = 'Stock Final Cost Lines'

    name = fields.Char('Description', compute='_compute_name', store=True)
    cost_id = fields.Many2one('stock.landed.cost', 'Landed Cost', ondelete='cascade', required=True)
    product_id = fields.Many2one('product.product', 'Product', required=True)
    
    former_cost = fields.Monetary(string='Original Value', compute='_compute_all_cost')
    additional_landed_cost = fields.Monetary(string='Additional Landed Cost', compute='_compute_all_cost')
    final_cost = fields.Monetary('New Value', compute='_compute_all_cost')
    currency_id = fields.Many2one('res.currency', related='cost_id.company_id.currency_id')
    
    @api.depends('product_id.code', 'product_id.name')
    def _compute_name(self):
        name = ''
        for line in self:
            #name = '%s - ' % (line.cost_line_id.name if line.cost_line_id else '')
            line.name = name + (line.product_id.code or line.product_id.name or '')
            
    @api.depends('product_id')
    def _compute_all_cost(self):
        for record in self:
            fc = ac = 0
            for AdjustementLine in record.cost_id.valuation_adjustment_lines:
                if AdjustementLine.product_id.id == record.product_id.id:
                    ac += AdjustementLine.additional_landed_cost
                    fc = AdjustementLine.former_cost
            record.former_cost = fc
            record.additional_landed_cost = ac
            record.final_cost = fc + ac