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
    has_rent_vechile = fields.Selection(related="custom_entry_type_id.has_rent_vechile")

    #fleet/rent vehicle extra fields
    f_duration_from = fields.Date(string='Duration From')
    f_duration_to = fields.Date(string='Duration To')
    
class CustomEntryLine(models.Model):
    _inherit = 'account.custom.entry.line'
    
    #has fleet/rent vehicle
    f_fleet_id = fields.Many2one('fleet.vehicle', string="Car Detail")
    f_driver_id = fields.Many2one('res.partner', string="Driver", ondelete='cascade')
    f_job_scope = fields.Selection(
        [('0_rental_charges', 'Car Rental.'),
         ('1_ot_charges', 'Driver OT.'),
         ('2_salary_charges', 'Driver Salary.'),
         ('3_maintenancee_fee', 'Maintenance Fee.'),
         ('4_management_fee', 'Management Fee.'),
         ('5_ondemand_charges', 'On Demand.'),
         ('6_petrol_charges', 'Petrol Charges.'),
         ('7_toll_fee', 'Toll Fee.'),
         ('8_replacement_charges', 'Replacement.')],
        string='Job Scope', )
    f_rent_days = fields.Float(string='Days')
    f_amount = fields.Float(string="Amount")
    
    