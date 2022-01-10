# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import datetime, time

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    requisition_line_id = fields.Many2one('purchase.requisition.line', string='Requisition Line', compute='_compute_requisition_line')
    requisition_line_no = fields.Integer(string='Requisition Line No.', compute='_compute_requisition_line')


    #@api.depends('purchase_line_id')
    def _compute_requisition_line(self):
        requisition_line = self.env['purchase.requisition.line'].browse(0)
        for purchase in self:
            for line in purchase.order_id.requisition_id.line_ids:
                if line.product_id.id == purchase.product_id.id:
                    requisition_line = line
                continue
            purchase.requisition_line_id = requisition_line.id
            purchase.requisition_line_no = int(requisition_line.id)
    