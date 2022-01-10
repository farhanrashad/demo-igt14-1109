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
    
    #App fields
    has_hotel = fields.Selection(related="custom_entry_type_id.has_hotel")
    
    
    #application common extra fields for hotel/accomodation
    customer_type = fields.Selection([('local', 'Local'), ('expat', 'Expat')], string='Customer Type')
    date_effective = fields.Date(string='Effective Date')
    date_subscription = fields.Date(string='Date of Subscription')
    
class CustomEntryLine(models.Model):
    _inherit = 'account.custom.entry.line'
    
    #has hotel/accomodation
    h_category = fields.Selection([
        ('travel', 'Travel'),
        ('ha', 'Housing Allowance'),
        ], string='Accomodation Category', default='travel')
    hotel_detail = fields.Char(string="Hotel Detail")
    h_check_in = fields.Date(string="Check-In")
    h_check_out = fields.Date(string="Check-Out")
    h_number_of_nights = fields.Float(string="Number of Nights", compute='_number_of_nights')
    h_travel_id = fields.Many2one('travel.request' , string="Travel Reference")
    h_travel_description = fields.Char(related='h_travel_id.description_main')
    h_travel_type = fields.Selection(related='h_travel_id.travel_type')
    h_unit_price = fields.Float(string="Hotel Unit Price")
    h_extra_charges = fields.Float(string="Hote Extra Charges")
    h_amount = fields.Float(string="Total Amount", compute='_compute_all_amount_hotel')
    
    @api.depends('h_number_of_nights', 'h_unit_price', 'h_extra_charges')
    def _compute_all_amount_hotel(self):
        total_amount = 0
        for line in self:
            total_amount = (line.h_number_of_nights * line.h_unit_price) + line.h_extra_charges
            line.update({
                'h_amount': total_amount
            })
            
    @api.onchange('h_check_in','h_check_out')
    def _number_of_nights(self):
        for line in self:
            if line.h_check_in and line.h_check_out:
                if line.h_check_in > line.h_check_out:
                    raise UserError(("Check Out cant be before Check in."))
                else:
                    delta = line.h_check_out - line.h_check_in
                    if abs(delta.days) > 0:
                        line.h_number_of_nights = abs(delta.days)
                    else:
                        line.h_number_of_nights = 1
            else:
                line.h_number_of_nights = 0

    
    