# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from datetime import date

class PurchaseSubscriptionStage(models.Model):
    _name = 'purchase.subscription.stage'
    _description = 'Purchase Subscription Stage'
    _order = 'sequence, id'

    def _get_default_subscription_type_ids(self):
        default_subscription_type_id = self.env.context.get('default_subscription_type_id')
        return [default_subscription_type_id] if default_subscription_type_id else None
    
    name = fields.Char(string='Stage Name', required=True, translate=True)
    stage_code = fields.Char(string='Code', size=3, copy=False)
    active = fields.Boolean(default=True)
    description = fields.Text(
        "Requirements", help="Enter here the internal requirements for this stage. It will appear "
                             "as a tooltip over the stage's name.", translate=True)
    sequence = fields.Integer(default=1)
    fold = fields.Boolean(string='Folded in Kanban',
                          help='This stage is folded in the kanban view when there are no records in that stage to display.')
    subscription_type_ids = fields.Many2many('purchase.subscription.type', 'purchase_subscription_type_stage_rel', 'subscription_stage_id', 'subscription_type_id', string='Subscription Types',
        default=_get_default_subscription_type_ids)
    
    stage_category = fields.Selection([
        ('draft', 'Draft'),
        ('progress', 'In Progress'),
        ('confirm', 'Confirmed'),
        ('closed', 'Closed'),
        ('cancel', 'Cancel'),
    ], string='Category', default='draft')
    
    next_stage_id = fields.Many2one('purchase.subscription.stage', string='Next Stage' )
    prv_stage_id = fields.Many2one('purchase.subscription.stage', string='Previous Stage')

    group_id = fields.Many2one('res.groups', string='Security Group')
    
    _sql_constraints = [
        ('code_uniq', 'unique (stage_code)', "Code already exists!"),
    ]
