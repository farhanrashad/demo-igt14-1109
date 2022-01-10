# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class StockCmaOrder(models.Model):
    _inherit = 'stock.cma.order'

    reason = fields.Char(string="Reasson", readonly=True)
    is_force_close = fields.Boolean()
    
    
    
    
    
#     def action_force_close(self):
#         raise UserError('sdfksdfjksdk')
#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
