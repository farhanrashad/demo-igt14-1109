# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from datetime import date

class AccountMove(models.Model):
    _inherit = 'account.move'

    deduction_fields = fields.Boolean(related='journal_id.deduction_fields')
    
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    invoiced_amount = fields.Monetary(string='Invoiced', store=True, readonly=True,
        currency_field='currency_id')
    deds_amount = fields.Monetary(string='Deds Amt', store=True, readonly=True,
        currency_field='currency_id')
    deds_percentage = fields.Float(string='Deds(%)', required=True, default=0.0)

    # field for electicity bills
    e_opening_units = fields.Integer(string='Opening Units', default=0)
    e_closing_units = fields.Integer(string='Closing Units', default=0)
    e_total_units = fields.Integer(string="Total Units", default=0, compute="_compute_all_units")
    e_maintenance_fee = fields.Float(string="Maintenance Fees", default=0)
    e_hp_fee = fields.Float(string="Horseposwer Fees", default=0)
    e_kwh_charges = fields.Float(string="KWH Charges", default=0)
    e_other_charges = fields.Float(string="Other Charges", default=0)
    e_total_unit_amount = fields.Float(string="Total Amount", default=0, compute="_compute_all_units_amount")
    
    #fields for Fuel
    f_booklet_no = fields.Char(string="Booklet No.")
    f_receipt_no = fields.Char(string="Receipt No.")
    
    @api.onchange('deds_amount')
    def _onchange_deds_amount(self):
        if self.deds_amount:
            self.price_unit = self.deds_amount
        
    @api.depends('e_opening_units','e_closing_units')
    def _compute_all_units(self):
        units = 0
        if self.move_id.group_fields_template == 'electric':
            for line in self:
                units = line.e_closing_units - line.e_opening_units
        self.e_total_units = units
        
    @api.depends('e_maintenance_fee','e_hp_fee','e_kwh_charges','e_other_charges')
    def _compute_all_units_amount(self):
        tot = 0
        if self.move_id.group_fields_template == 'electric':
            for line in self:
                tot = line.e_maintenance_fee + line.e_hp_fee + line.e_kwh_charges + line.e_other_charges
        self.e_total_unit_amount = tot
        
    @api.onchange('e_total_unit_amount')
    def _onchange_total_unit_amount(self):
        if self.move_id.group_fields_template == 'electric':
            for line in self:
                line.quantity = line.e_total_units
                line.price_unit = line.e_total_unit_amount / line.e_total_units