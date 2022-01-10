# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
#from datetime import date
from datetime import datetime, timedelta


#Penlaty Configiguration
class PenaltyConfig(models.Model):
    _name = 'op.penalty.config'
    _description = 'Operations Penalty Config'
    
    name = fields.Char(string='Name', compute='_compute_name', translate=True)
    active = fields.Boolean('Active', default=True, help="If unchecked, it will allow you to hide the stage without removing it.")

    description = fields.Text(
        "Requirements", help="Enter here the internal requirements for this penalty.", translate=True)
    
    partner_id = fields.Many2one('res.partner',  String="Supplier")
    effective_date = fields.Date(string='Effective From')
    #penalty_type_id = fields.Many2one('op.penalty.type', string='Penalty Type', index=True, required=True, )
    custom_entry_type_id = fields.Many2one('account.custom.entry.type', string='Entry Type', index=True, required=True,)

    rule_type = fields.Selection([
        ('normal', 'Normal'),
        ('sla', 'Service Level'),
        ('occur', 'Occurrence'),
        ('sow', 'SOW'),
    ], string='Rule Type', default='normal', required=True)
    
    penalty_config_line = fields.One2many('op.penalty.config.line', 'penalty_config_id', string='Penalty Config Line', copy=True, auto_join=True)
    penalty_config_occur_line = fields.One2many('op.penalty.config.occur.line', 'penalty_config_id', string='Penalty Config Occur Line', copy=True, auto_join=True)
    penalty_config_sow_line = fields.One2many('op.penalty.config.sow.line', 'penalty_config_id', string='Penalty Config SOW Line', copy=True, auto_join=True)


    
    @api.depends('partner_id','effective_date')
    def _compute_name(self):
        for record in self:
            record.name = record.partner_id.name
    
class PenaltyConfigLine(models.Model):
    _name = 'op.penalty.config.line'
    _description = 'Penalty Config SLA Line'
    
    penalty_config_id = fields.Many2one('op.penalty.config', string='Penalty Config', required=True, ondelete='cascade', index=True, copy=False)
    partner_id = fields.Many2one('res.partner',  related='penalty_config_id.partner_id')
    effective_date = fields.Date(related='penalty_config_id.effective_date')
    service_class = fields.Selection([
        ('Critical Site', 'Critical Site'), 
        ('Class B', 'Class B'), 
        ('Class C', 'Class C')], default='Critical Site', string='Classification')
    service_level = fields.Selection([
        ('critical', 'Critical'), 
        ('major', 'Major'), 
        ('minor', 'Minor'), 
        ('normal', 'Normal')], default='normal', string='Service Level')
    uptime_from = fields.Float(string='Uptime From', default=0.0)
    uptime_to = fields.Float(string='Uptime To', default=0.0)
    penalty_deduction_per = fields.Float(string='Penalty %age', default=0.0)
    penalty_deduction_factor = fields.Float(string='Factor', default=0.0)
    
class PenaltyConfigOccurLine(models.Model):
    _name = 'op.penalty.config.occur.line'
    _description = 'Penalty Config Occurence Line'
    
    penalty_config_id = fields.Many2one('op.penalty.config', string='Penalty Config', required=True, ondelete='cascade', index=True, copy=False)
    partner_id = fields.Many2one('res.partner',  related='penalty_config_id.partner_id')
    effective_date = fields.Date(related='penalty_config_id.effective_date')
    service_level = fields.Selection([
        ('1', '1st Offense'), 
        ('2', '2nd Offense'), 
        ('3', '3rd Offense'), 
        ('4', '4th Offense')], default='1', string='Service Level')
    occurence = fields.Integer(string='Occurence', default=1)
    penalty_amount = fields.Float(string='Penalty Amount', default=0.0)


    
class PenaltyConfigSOWType(models.Model):
    _name = 'op.penalty.config.sow.type'
    _description = 'Penalty Config SOW Type'
    
    name = fields.Char(string='Name', required=True)

class PenaltyConfigSOW(models.Model):
    _name = 'op.penalty.config.sow'
    _description = 'Penalty Config SOW'
    
    name = fields.Char(string='Name', required=True)
    frequency = fields.Char(string='Frequency')
    penalty_sow_type_id = fields.Many2one('op.penalty.config.sow.type', string='SOW Type')
    
class PenaltyConfigSOWLine(models.Model):
    _name = 'op.penalty.config.sow.line'
    _description = 'Penalty Config SOW Line'
    
    penalty_config_id = fields.Many2one('op.penalty.config', string='Penalty Config', required=True, ondelete='cascade', index=True, copy=False)
    partner_id = fields.Many2one('res.partner',  related='penalty_config_id.partner_id')
    effective_date = fields.Date(related='penalty_config_id.effective_date')
    penalty_sow_type_id = fields.Many2one('op.penalty.config.sow.type', string='SOW Type')
    penalty_sow_id = fields.Many2one('op.penalty.config.sow', string='SOW')
    penalty_deduction_a = fields.Float(string='Deduction-A(%)', default=0.0)
    penalty_deduction_b = fields.Float(string='Deduction-B(%)', default=0.0)


