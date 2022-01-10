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
    has_fuel_drawn = fields.Selection(related="custom_entry_type_id.has_fuel_drawn")
    has_fuel_filling = fields.Selection(related="custom_entry_type_id.has_fuel_filling")
    
class CustomEntryLine(models.Model):
    _inherit = 'account.custom.entry.line'
    
    #has fuel Drawn
    d_date = fields.Date(string='Drawn Date')
    d_partner_id = fields.Many2one('res.partner',string='Drawn Purchase From', ondelete='cascade')
    d_contact_id = fields.Many2one('res.partner',string='Drawn Contact From', ondelete='cascade')
    d_product_qty = fields.Float(string='Drawn Qty', default=1.0, digits='Product Unit of Measure', )
    d_price_unit = fields.Float(string='Drawn Unit Price', default=1.0, digits='Product Price')
    d_price_subtotal = fields.Float(compute='_compute_fuel_drawn_total', string='Drawn Subtotal')
    d_booklet_no = fields.Char(string='Booklet')
    d_receipt_no = fields.Char(string='Receipt No.')
    
    #fuel drawn methods
    @api.depends('d_product_qty', 'd_price_unit')
    def _compute_fuel_drawn_total(self):
        for line in self:
            tot = 0
            if line.d_product_qty > 0 and line.d_price_unit > 0:
                tot = line.d_product_qty * line.d_price_unit
            line.d_price_subtotal = tot
        
    #Fuel Filling
    f_date = fields.Date(string='Filling Date')
    f_partner_id = fields.Many2one('res.partner',string='Filling Purchase From', ondelete='cascade')
    f_contact_id = fields.Many2one('res.partner',string='Filling Contact From', ondelete='cascade')
    f_gen_name = fields.Char(string='Generator Name')
    f_gen_capacity = fields.Integer(string='Generator Capacity')
    f_curr_drgh = fields.Float(string='Current DRGH')
    f_opening_stock = fields.Float(string='Opening Stock')
    f_closing_stock = fields.Float(string='Closting Stock', compute='_compute_fuel_filled_closing_stock', store=True)
    f_product_qty = fields.Float(string='Filling Qty', default=1.0, digits='Product Unit of Measure', )
    f_price_unit = fields.Float(string='Filling Unit Price', default=1.0, digits='Product Price')
    f_price_subtotal = fields.Float(compute='_compute_fuel_filled_total', string='Filling Subtotal')
    f_booklet_no = fields.Char(string='Filling Booklet')
    f_receipt_no = fields.Char(string='Filling Receipt No.')
    
    #fuel filling methods
    @api.depends('f_product_qty', 'f_price_unit')
    def _compute_fuel_filled_total(self):
        for line in self:
            tot = 0
            if line.f_product_qty and line.f_price_unit:
                tot = line.f_product_qty * line.f_price_unit
            line.f_price_subtotal = tot
    
    
    @api.depends('f_opening_stock','f_product_qty')
    def _compute_fuel_filled_closing_stock(self):
        tot = 0
        for line in self:
            tot = line.f_opening_stock + line.f_product_qty
            line.f_closing_stock = tot

    
    