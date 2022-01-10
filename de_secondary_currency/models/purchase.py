# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import datetime, time
from dateutil.relativedelta import relativedelta
from itertools import groupby
from pytz import timezone, UTC
from werkzeug.urls import url_encode

from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_is_zero
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.misc import formatLang, get_lang


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    
    company_currency_id = fields.Many2one('res.currency', string='Company Currency', related='company_id.currency_id')
    
    total_base_signed = fields.Monetary(string='Total base.Curr.', readonly=True, compute='_compute_all_currency_conversion_amount', currency_field='company_currency_id')

    conversion_date = fields.Date(string='Conversion Date', compute='_compute_secondary_currency_amount')
    
    @api.depends('order_line.price_total')
    def _compute_all_currency_conversion_amount(self):
        for order in self:
            total_base_signed = 0.0
            order.conversion_date = order.date_approve
            if not (order.currency_id.id == order.company_id.currency_id.id):
                    #total_base_signed = order.company_currency_id._convert(order.amount_total, order.currency_id, order.company_id, fields.date.today()) 
                    total_base_signed = order.currency_id._convert(order.amount_total, order.company_id.currency_id, order.company_id, fields.date.today()) 

                    
                #if not (order.currency_id.id == order.company_id.currency_id.id):
                #total_base_signed += order.currency_id._get_conversion_rate(order.currency_id, order.company_currency_id,order.company_id, fields.date.today()) * order.amount_total
            else:
                total_base_signed = order.amount_total
                
                
            order.update({
                'total_base_signed': total_base_signed,
            })
            
class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"
    
    company_currency_id = fields.Many2one('res.currency', string='Company Currency', related='company_id.currency_id')
    
    price_unit_base = fields.Monetary(string='BC Price', readonly=True, compute='_compute_all_currency_conversion_amount', currency_field='company_currency_id')
    price_total_base = fields.Monetary(string='BC Total', readonly=True, compute='_compute_all_currency_conversion_amount', currency_field='company_currency_id')
    
    @api.depends('price_unit')
    def _compute_all_currency_conversion_amount(self):
        price = total = 0
        for line in self:
            if not (line.order_id.currency_id.id == line.order_id.company_id.currency_id.id):
                #price = line.currency_id._get_conversion_rate(line.currency_id, line.company_currency_id,line.company_id, fields.date.today()) * line.price_unit
                price = line.order_id.currency_id._convert(line.price_unit, line.order_id.company_currency_id, line.order_id.company_id, fields.date.today()) 
                total = line.product_qty * price
            else:
                price = line.price_unit
                total = line.price_total
            line.update({
                'price_unit_base': price,
                'price_total_base': total,
            })