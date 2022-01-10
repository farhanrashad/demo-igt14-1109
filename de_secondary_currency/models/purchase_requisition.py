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


class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"
    
    company_currency_id = fields.Many2one('res.currency', string='Company Currency', related='company_id.currency_id')
    
    total_base_signed = fields.Monetary(string='Total base.Curr.', readonly=True, compute='_compute_all_currency_conversion_amount', currency_field='company_currency_id')
    
    @api.depends('line_ids.price_unit')
    def _compute_all_currency_conversion_amount(self):
        total_base_signed = 0.0
        for requisition in self:
            price = total = 0
            for line in requisition.line_ids:
                if not (requisition.currency_id.id == requisition.company_id.currency_id.id):
                    price = requisition.currency_id._convert(line.price_unit, requisition.company_currency_id, requisition.company_id, fields.date.today())  
                    #if not (requisition.currency_id.id == requisition.company_id.currency_id.id):
                    #price = requisition.currency_id._get_conversion_rate(requisition.currency_id, requisition.company_currency_id,requisition.company_id, fields.date.today()) * line.price_unit
                else:
                    price = line.price_unit
                total += price * line.product_qty
        
            requisition.update({
                'total_base_signed': total,
            })
            
class PurchaserequisitionLine(models.Model):
    _inherit = "purchase.requisition.line"
    
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    
    price_unit_base = fields.Monetary(string='BC Price', readonly=True, compute='_compute_all_currency_conversion_amount', currency_field='company_currency_id')
    price_total_base = fields.Monetary(string='BC Total', readonly=True, compute='_compute_all_currency_conversion_amount', currency_field='company_currency_id')
    
    @api.depends('price_unit','product_qty')
    def _compute_all_currency_conversion_amount(self):
        for line in self:
            price = total = 0
            if not (line.requisition_id.currency_id.id == line.requisition_id.company_id.currency_id.id):
                #price = line.requisition_id.currency_id._get_conversion_rate(line.requisition_id.currency_id, line.company_currency_id,line.requisition_id.company_id, fields.date.today()) * line.price_unit
                price = line.requisition_id.currency_id._convert(line.price_unit, line.requisition_id.company_currency_id, line.requisition_id.company_id, fields.date.today())  

            else:
                price = line.price_unit
            total = line.price_unit * line.product_qty
            line.update({
                'price_unit_base': price,
                'price_total_base': total,
            })