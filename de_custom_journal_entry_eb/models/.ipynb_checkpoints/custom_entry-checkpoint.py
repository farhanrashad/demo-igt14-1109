# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date
from dateutil.relativedelta import relativedelta

import json
from lxml import etree

class CustomEntry(models.Model):
    _inherit = 'account.custom.entry'
    
    has_advanced = fields.Selection(related="custom_entry_type_id.has_advanced")
    has_electricity = fields.Selection(related="custom_entry_type_id.has_electricity")
    
    amount_advanced_total = fields.Float('Total Advanced', compute='_amount_all')
    
    custom_entry_eb_history_line = fields.One2many('account.custom.entry.ebh.line', 'custom_entry_id', string='Entry Line for Electricity Bill', copy=True, auto_join=True,)
    
class CustomEntryLine(models.Model):
    _inherit = 'account.custom.entry.line'
    
    advance_subtotal = fields.Monetary(string='Adv. Subtotal', store=True)
    
    #has electricity
    e_paid_to = fields.Selection([
        ('govt', 'Government'),
        ('private', 'Private')],
        string='Paid To')
    date_bill_from = fields.Date(string='Date From', )
    date_bill_to = fields.Date(string='Date To', )
    amount_advanced = fields.Float(string='Forecast', help='Advanced Amount')
    meter_number = fields.Char(string='Meter')
    opening_reading = fields.Integer(string='Opening Reading', help='Opening reading of meter')
    closing_reading = fields.Integer(string='Closing Reading', help='Closing Reading of meter')
    additional_unit = fields.Integer(string='Additional Units')
    total_unit = fields.Integer(string='Total Unit', compute='_compute_total_units', store=True)
    maintainence_fee = fields.Float(string='Mnt. Fees', help='Maintenance Fees')
    hp_fee = fields.Float(string='HP Fee', help='Horsepower Fees')
    KHW_charges = fields.Float(string='KHW')
    actual_KHW_charges = fields.Float(string='Actual KHW')
    other_charges = fields.Float(string='Other Charges')
    amount_total_electricity = fields.Float(string='Total', compute='_compute_total_electricity_amount', store=True)
    
    @api.depends('opening_reading','closing_reading','additional_unit')
    def _compute_total_units(self):
        for rec in self:
            rec.total_unit = (rec.closing_reading - rec.opening_reading) + rec.additional_unit

    @api.depends('maintainence_fee','hp_fee','KHW_charges','other_charges')
    def _compute_total_electricity_amount(self):
        for rec in self:
            rec.amount_total_electricity = rec.maintainence_fee + rec.hp_fee + rec.KHW_charges + rec.other_charges
            
    
class CustomEntryLine(models.Model):
    _name = 'account.custom.entry.ebh.line'
    _description = 'Custom Entry Line Electricity Bill History'
    
    custom_entry_id = fields.Many2one('account.custom.entry', string='Custom Entry', required=True, ondelete='cascade', index=True, copy=False)
    
    project_id = fields.Many2one('project.project', string="Project", check_company=True, ondelete='cascade')
    amount = fields.Float(string='amount')
    company_id = fields.Many2one('res.company', related='custom_entry_id.company_id')
    currency_id = fields.Many2one('res.currency', related='custom_entry_id.currency_id')


