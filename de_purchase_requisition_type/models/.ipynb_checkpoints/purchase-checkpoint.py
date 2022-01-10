# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError

    
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    requisition_type_id = fields.Many2one('purchase.requisition.type', string="Requisition Type", compute='_get_type_id', store=True, readonly=False)

    @api.depends('requisition_id')
    def _get_type_id(self):
        for purchase in self:
            purchase.requisition_type_id = purchase.requisition_id.type_id.id
