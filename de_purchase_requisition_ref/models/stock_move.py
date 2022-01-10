# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = 'stock.move'
    
    requisition_line_id = fields.Many2one('purchase.requisition.line', string='Requisition Line', compute='_compute_requisition_line')
    requisition_line_no = fields.Integer(string='Requisition Line No.', compute='_compute_requisition_line')


    @api.depends('purchase_line_id')
    def _compute_requisition_line(self):
        requisition_line = self.env['purchase.requisition.line'].browse(0)
        for stock in self:
            if stock.purchase_line_id:
                for line in stock.purchase_line_id.order_id.requisition_id.line_ids:
                    if line.product_id.id == stock.product_id.id:
                        requisition_line = line
                    continue
            stock.requisition_line_id = requisition_line.id
            stock.requisition_line_no = int(requisition_line.id)
