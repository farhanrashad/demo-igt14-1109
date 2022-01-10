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
    
    has_travel = fields.Selection(related="custom_entry_type_id.has_travel")
    #travel fields
    t_travel_by = fields.Selection([
        ('ticket', 'Flight Ticket'),
        ('vehicle', 'Vehicle Rental')],
        string='Travel By', default='ticket')
    
class CustomEntryLine(models.Model):
    _inherit = 'account.custom.entry.line'
    
    #has travel
    t_travel_category = fields.Selection([
        ('domestic', 'Domestic'),
        ('international', 'International'),
        ], string='Travel Category', default='domestic')
    travel_from = fields.Char(string='From')
    travel_to = fields.Char(string='To')
    date_departure = fields.Date(string='Departure Date', )
    date_arrival = fields.Date(string='Arrival Date', )    
    number_of_days = fields.Float(string="Number of Days" , compute = '_number_of_days')
    travel_reference = fields.Many2one('travel.request' , string="Travel Reference")
    t_travel_description = fields.Char(related='travel_reference.description_main')
    t_travel_type = fields.Selection(related='travel_reference.travel_type')
    t_unit_price = fields.Float(string="Travel Unit Price")
    t_extra_charges = fields.Float(string="Travel Extra Charges")
    t_amount_travel = fields.Float(string="Travel Total Amount", compute='_compute_all_amount_travel')
    
    @api.depends('number_of_days', 't_unit_price', 't_extra_charges')
    def _compute_all_amount_travel(self):
        total_amount_travel = 0
        for line in self:
            total_amount_travel = (line.number_of_days * line.t_unit_price) + line.t_extra_charges
            line.update({
                't_amount_travel': total_amount_travel
            })
    
    @api.onchange('date_departure','date_arrival')
    def _number_of_days(self):
        for line in self:
            if line.date_departure and line.date_arrival:
                if line.date_departure > line.date_arrival:
                    raise UserError(("Arrival Date cant be before Departure Date."))
                else:
                    delta = line.date_arrival - line.date_departure
                    if abs(delta.days) > 0:
                        line.number_of_days = abs(delta.days)
                    else:
                        line.number_of_days = 1
            else:
                line.number_of_days = 0

    
    