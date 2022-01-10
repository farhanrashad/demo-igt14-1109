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


class StockPicking(models.Model):
    _inherit = "stock.picking"
    
    company_currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    
    total_base_signed = fields.Monetary(string='Total base.Curr.', readonly=True, compute='_compute_all_currency_conversion_amount', currency_field='company_currency_id')

    
    @api.depends('move_lines.product_uom_qty','move_lines.quantity_done')
    def _compute_all_currency_conversion_amount(self):
        total_base_signed = 0.0
        price = total = 0.0
        for picking in self:
            total_base_signed = 0.0
            price = total = 0.0
            for line in picking.move_lines:
                if line.purchase_line_id:
                    if not (line.currency_id.id == picking.company_id.currency_id.id):
                        #price = line.currency_id._get_conversion_rate(line.currency_id, picking.company_id.currency_id,picking.company_id, fields.date.today()) * line.price_unit
                        price = line.currency_id._convert(line.price_unit, line.company_id.currency_id, picking.company_id, fields.date.today()) 
                    #price = 1
                    else:
                        price = line.purchase_line_id.price_unit
                    if line.state == 'done':
                        total += (price * line.quantity_done)
                    else:
                       total += (price * line.product_uom_qty)
        
            picking.update({
                'total_base_signed': total,
            })
            
class StockMove(models.Model):
    _inherit = "stock.move"
    
    company_currency_id = fields.Many2one('res.currency', string="Base Currency", related='company_id.currency_id')
    
    currency_id = fields.Many2one('res.currency', compute='_compute_all_purchase')
    price_unit = fields.Monetary(string='Price', readonly=True, compute='_compute_all_purchase', currency_field='currency_id')
    price_total = fields.Monetary(string='Total', readonly=True, compute='_compute_all_purchase', currency_field='currency_id')

    
    price_unit_base = fields.Monetary(string='BC Price', readonly=True, compute='_compute_all_currency_conversion_amount', currency_field='company_currency_id')
    price_total_base = fields.Monetary(string='BC Total', readonly=True, compute='_compute_all_currency_conversion_amount', currency_field='company_currency_id')
    
    @api.depends('purchase_line_id')
    def _compute_all_purchase(self):
        currency_id = self.env['res.currency'].browse(0)
        price_unit = price_total = 0.0
        for line in self:
            if line.purchase_line_id:
                currency_id = line.purchase_line_id.currency_id
                price_unit = line.purchase_line_id.price_unit
                if line.state == 'done':
                    price_total = line.purchase_line_id.price_unit * line.quantity_done
                else:
                    price_total = line.purchase_line_id.price_unit * line.product_uom_qty
                #price_total = line.purchase_line_id.price_unit * line.quantity_done
            line.currency_id = currency_id.id
            line.price_unit = price_unit
            line.price_total = price_total
                
    @api.depends('product_uom_qty','quantity_done')
    def _compute_all_currency_conversion_amount(self):
        for line in self:
            price = total = 0.0
            if line.product_uom_qty > 0 or line.quantity_done > 0:
                if not (line.currency_id.id == line.picking_id.company_id.currency_id.id):
                    if line.purchase_line_id:
                        #price = line.currency_id._get_conversion_rate(line.currency_id, line.picking_id.company_id.currency_id,line.picking_id.company_id, fields.date.today()) * line.price_unit
                        price = line.currency_id._convert(line.price_unit, line.company_id.currency_id, line.picking_id.company_id, fields.date.today()) 
                        #price = 1
                    else:
                        price = line.price_unit
                    if line.state == 'done':
                        total = price * line.quantity_done
                    else:
                        total = price * line.product_uom_qty
                        
            line.update({
                'price_unit_base': price,
                'price_total_base': total,
            })