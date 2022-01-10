# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date
from dateutil.relativedelta import relativedelta

import json
from lxml import etree

MONTH_LIST = [('1', 'Jan'), ('2', 'Feb'), ('3', 'Mar'), ('4', 'Apr'), ('5', 'May'), ('6', 'Jun'), ('7', 'Jul'), ('8', 'Aug'), ('9', 'Sep'), ('10', 'Oct'), ('11', 'Nov'),('12', 'Dec')]

class CustomEntry(models.Model):
    _inherit = 'account.custom.entry'
    
    #Line Item fields
    has_hse_fields = fields.Selection(related="custom_entry_type_id.has_hse_fields")
    has_pm_fields = fields.Selection(related="custom_entry_type_id.has_pm_fields")
    has_sla_fields = fields.Selection(related="custom_entry_type_id.has_sla_fields")
    has_spmrf_fields = fields.Selection(related="custom_entry_type_id.has_spmrf_fields")
    
    adjustment_per = fields.Float(string="Adjustment %")
    
    allow_penalty_adjustment = fields.Boolean(compute='_compute_allow_penalty_adjustment')
    
    def _compute_allow_penalty_adjustment(self):
        for order in self:
            if order.custom_entry_type_id.allow_penalty_adjustment == True and order.stage_id.allow_penalty_adjustment == True:
                order.update({
                    'allow_penalty_adjustment': True 
                }) 
            else:
                order.update({
                    'allow_penalty_adjustment': False
                })
        
    
    def action_update_panalty_amount(self):
        if self.stage_category == 'closed':
             raise UserError(_('Document is not open for adjustmnet.'))
        tot_om_charges = 0
        tot_penalty_amt = 0
        for line in self.custom_entry_line:
            tot_om_charges += line.om_service_charges
            tot_penalty_amt += line.amount_penalty
        for line in self.custom_entry_line:
            if tot_om_charges > 0:
                line.amount_approved_penalty = (line.amount_penalty/tot_penalty_amt) * (tot_om_charges * (self.adjustment_per/100))
            
class CustomEntryLine(models.Model):
    _inherit = 'account.custom.entry.line'
    
    #sla
    service_class = fields.Selection([
        ('Critical Site', 'Critical Site'), 
        ('Class B', 'Class B'), 
        ('Class C', 'Class C')], default='Critical Site', string='Classification')
    service_level = fields.Selection([
        ('critical', 'Critical'), 
        ('major', 'Major'), 
        ('minor', 'Minor'), 
        ('normal', 'Normal')], default='normal', string='Service Level')
    uptime = fields.Float(string='Uptime', default=0.0)
    #occurence
    #sow
    penalty_sow_type_id = fields.Many2one('op.penalty.config.sow.type', string='SOW Type')
    penalty_sow_id = fields.Many2one('op.penalty.config.sow', string='SOW')
    frequency = fields.Char(related='penalty_sow_id.frequency')
    sow_deduct_type = fields.Selection([
        ('a', 'A'), 
        ('b', 'B'), 
        ], default='a', string='Deduction Type')
    amount_penalty = fields.Float(string='Penalty Amount',copy=False)
    om_service_charges = fields.Float(string='Service Charges',copy=False)
    amount_approved_penalty = fields.Float(string='Penalty Approved', copy=False)
    