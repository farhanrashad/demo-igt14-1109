# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from datetime import date

class StockTransferOrderStage(models.Model):
    _name = 'stock.transfer.order.stage'
    _description = 'Order Stage'
    _order = 'sequence, stage_category, id'

    def _get_default_transfer_order_type_ids(self):
        default_transfer_order_type_id = self.env.context.get('default_transfer_order_type_id')
        return [default_transfer_order_type_id] if default_transfer_order_type_id else None
    
    name = fields.Char(string='Stage Name', translate=True)
    stage_code = fields.Char(string='Stage Code', size=3, copy=False)
    active = fields.Boolean('Active', default=True, help="If unchecked, it will allow you to hide the stage without removing it.")

    description = fields.Text(
        "Requirements", help="Enter here the internal requirements for this stage. It will appear "
                             "as a tooltip over the stage's name.", translate=True)
    sequence = fields.Integer(default=1)
    fold = fields.Boolean(string='Folded in Kanban',
                          help='This stage is folded in the kanban view when there are no records in that stage to display.')
    transfer_order_type_ids = fields.Many2many('stock.transfer.order.type', 'transfer_order_type_stage_rel', 'transfer_order_stage_id', 'transfer_order_type_id', string='Transfer Types', default=_get_default_transfer_order_type_ids)
    
    transfer_order_category_ids = fields.Many2many('stock.transfer.order.category', 'transfer_order_category_stage_rel', 'transfer_order_stage_id', 'transfer_order_category_id', string='Transfer Categories', domain="[('transfer_order_type_id','=',transfer_order_type_ids)]")
    
    allow_transactions = fields.Boolean(string='Allow Transactions')
    stage_category = fields.Selection([
        ('draft', 'Draft'),
        ('progress', 'In Progress'),
        ('confirm', 'Confirmed'),
        ('transfer', 'Transferred'),
        ('close', 'Closed'),
        ('cancel', 'Cancelled'),
    ], string='Stage Category', default='draft')
    
    next_stage_id = fields.Many2one('stock.transfer.order.stage', string='Next Stage' )
    prv_stage_id = fields.Many2one('stock.transfer.order.stage', string='Previous Stage')

    group_id = fields.Many2one('res.groups', string='Security Group')
    allow_special_edit = fields.Boolean(string='Allow Special Edit')

    _sql_constraints = [
        ('code_uniq', 'unique (stage_code)', "Code already exists!"),
    ]

    