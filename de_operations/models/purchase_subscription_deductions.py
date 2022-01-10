# -*- coding: utf-8 -*-

from datetime import datetime, time
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date
from random import randint
    
class PurchaseSubsDedsSlaType(models.Model):
    _name = 'purchase.subs.deds.sla.categ'
    _description = 'Deduction SLA Categories'
    
    name = fields.Char(string='Name', required=True, translate=True)
    active = fields.Boolean(default=True)
    subscription_type_id = fields.Many2one('purchase.subscription.type', string='Subscription Type', 
                                           required=True, help="The subscription type categories agreement.",)
    purchase_sub_deds_sla_frequency_ids = fields.One2many('purchase.subs.deds.sla.frequency', 'purchase_subs_deds_sla_categ_id', string='Frequency Lines', copy=True)



class PurchaseSubsDedsSlaFrequency(models.Model):
    _name = 'purchase.subs.deds.sla.frequency'
    _description = 'Deduction SLA Frequency'
    
    name = fields.Char(string='Name', required=True, translate=True)
    purchase_subs_deds_sla_categ_id = fields.Many2one('purchase.subs.deds.sla.categ', string='Deudction Category', ondelete='cascade')

    
class PurchaseSubsDedsSla(models.Model):
    _name = 'purchase.subs.deds.sla'
    _description = 'Deduction SLA'
    
    name = fields.Char(string='Name', translate=True, store=True, compute='_compute_name')
    active = fields.Boolean(default=True)
    company_id = fields.Many2one('res.company', string="Company", default=lambda s: s.env.company, required=True, )
    partner_id = fields.Many2one('res.partner', string='Vendor', required=True, auto_join=True, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    date_start = fields.Date(string='Start Date', required=True)
    date_end = fields.Date(string='End Date', required=True)
    subscription_type_id = fields.Many2one('purchase.subscription.type', string='Subscription Type', required=True, help="The subscription type categories agreement.",)
        
    purchase_sub_deds_sla_rule_ids = fields.One2many('purchase.subs.deds.sla.rule', 'purchase_subs_deds_sla_id', string='Subscription Lines', copy=True)

    @api.depends('partner_id','subscription_type_id')
    def _compute_name(self):
        name = ''
        for sla in self:
            if sla.subscription_type_id and sla.partner_id:
                name = sla.subscription_type_id.name + ' - ' + sla.partner_id.name 
        self.name = name
        
        
class PurchaseSubsDedsSlarules(models.Model):
    _name = 'purchase.subs.deds.sla.rule'
    _description = 'Deduction SLA Rules'
    
    purchase_subs_deds_sla_id = fields.Many2one('purchase.subs.deds.sla', string='Deudction SLA', ondelete='cascade')
    subscription_type_id = fields.Many2one('purchase.subscription.type', related='purchase_subs_deds_sla_id.subscription_type_id')
    name = fields.Char(string='Name', required=True, translate=True)
    purchase_subs_deds_sla_categ_id = fields.Many2one('purchase.subs.deds.sla.categ', string='Deduction Category', required=True, domain="[('subscription_type_id', '=', subscription_type_id)]")
    deds_percentage = fields.Float(string='Deduction (%)', required=True, default=0.0)
    
    @api.onchange('purchase_subs_deds_sla_categ_id')
    def _onchange_categ_id(self):
        if self.purchase_subs_deds_sla_categ_id:
            self.name = self.purchase_subs_deds_sla_categ_id.name