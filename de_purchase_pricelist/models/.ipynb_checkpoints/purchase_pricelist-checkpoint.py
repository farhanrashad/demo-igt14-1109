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



from odoo.tools import float_compare





class PurchasePricelist(models.Model):
    _name = 'purchase.pricelist'
    _description = 'Purchase Pricelist'
    
    name = fields.Char('Reference', required=True, index=True, copy=False, )
    partner_id = fields.Many2one('res.partner', string='Vendor', required=True, )
    
    company_id = fields.Many2one('res.company', 'Company',
        default=lambda self: self.env.company.id, index=1)
    currency_id = fields.Many2one(
        'res.currency', 'Currency',
        default=lambda self: self.env.company.currency_id.id,
        required=True)
    date_start = fields.Date('Start Date', help="Start date for this vendor price")
    date_end = fields.Date('End Date', help="End date for this vendor price")
    
    supplierinfo_ids = fields.One2many('product.supplierinfo', 'purchase_pricelist_id', string='Pricelist ', copy=True)
    
class ProductSupplierInfo(models.Model):
    _inherit = 'product.supplierinfo'
    
    purchase_pricelist_id = fields.Many2one('purchase.pricelist', string='Pricelist',)

    
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'    

    
    @api.onchange('partner_id')
    def onchange_partner_price(self):
        for line in self.order_line:
            line.action_purchase_pricelist()
                
    
class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    
    
    
    def action_purchase_pricelist(self):
        if not self.product_id:
            return
        params = {'order_id': self.order_id}
        seller = self.product_id._select_seller(
                partner_id=self.partner_id,
                quantity=self.product_qty,
                date=self.order_id.date_order and self.order_id.date_order.date(),
                uom_id=self.product_uom,
                params=params)
        if self.project_id.address_id.state_id:
            
            for sellerline in self.product_id.seller_ids:
                if self.order_id.partner_id:
                    if sellerline.x_studio_region.id == self.project_id.address_id.state_id.id and self.order_id.partner_id.id == sellerline.name.id:
                        seller = sellerline
                else:
                    if sellerline.x_studio_region.id == self.project_id.address_id.state_id.id :
                        seller = sellerline

        if seller or not self.date_planned:
            self.date_planned = self._get_date_planned(seller).strftime(DEFAULT_SERVER_DATETIME_FORMAT)

        # If not seller, use the standard price. It needs a proper currency conversion.
        if not seller:
            price_unit = self.env['account.tax']._fix_tax_included_price_company(
                self.product_id.uom_id._compute_price(self.product_id.standard_price, self.product_id.uom_po_id),
                self.product_id.supplier_taxes_id,
                self.taxes_id,
                self.company_id,
            )
            if price_unit and self.order_id.currency_id and self.order_id.company_id.currency_id != self.order_id.currency_id:
                price_unit = self.order_id.company_id.currency_id._convert(
                    price_unit,
                    self.order_id.currency_id,
                    self.order_id.company_id,
                    self.date_order or fields.Date.today(),
                )

            if self.product_uom:
                price_unit = self.product_id.uom_id._compute_price(price_unit, self.product_uom)

            self.price_unit = price_unit
            return

        price_unit = self.env['account.tax']._fix_tax_included_price_company(seller.price, self.product_id.supplier_taxes_id, self.taxes_id, self.company_id) if seller else 0.0
        if price_unit and seller and self.order_id.currency_id and seller.currency_id != self.order_id.currency_id:
            price_unit = seller.currency_id._convert(
                price_unit, self.order_id.currency_id, self.order_id.company_id, self.date_order or fields.Date.today())

        if seller and self.product_uom and seller.product_uom != self.product_uom:
            price_unit = seller.product_uom._compute_price(price_unit, self.product_uom)

        self.price_unit = price_unit
    
    
    
    @api.onchange('product_qty', 'product_uom', 'project_id')
    def _onchange_quantity(self):
        if not self.product_id:
            return
        params = {'order_id': self.order_id}
        seller = self.product_id._select_seller(
                partner_id=self.partner_id,
                quantity=self.product_qty,
                date=self.order_id.date_order and self.order_id.date_order.date(),
                uom_id=self.product_uom,
                params=params)
        if self.project_id.address_id.state_id:
          
        
        
            for sellerline in self.product_id.seller_ids:
                if self.order_id.partner_id:
                    if sellerline.x_studio_region.id == self.project_id.address_id.state_id.id and self.order_id.partner_id.id == sellerline.name.id:
                        seller = sellerline
                else:
                    if sellerline.x_studio_region.id == self.project_id.address_id.state_id.id :
                        seller = sellerline
                    

        if seller or not self.date_planned:
            self.date_planned = self._get_date_planned(seller).strftime(DEFAULT_SERVER_DATETIME_FORMAT)

        # If not seller, use the standard price. It needs a proper currency conversion.
        if not seller:
            price_unit = self.env['account.tax']._fix_tax_included_price_company(
                self.product_id.uom_id._compute_price(self.product_id.standard_price, self.product_id.uom_po_id),
                self.product_id.supplier_taxes_id,
                self.taxes_id,
                self.company_id,
            )
            if price_unit and self.order_id.currency_id and self.order_id.company_id.currency_id != self.order_id.currency_id:
                price_unit = self.order_id.company_id.currency_id._convert(
                    price_unit,
                    self.order_id.currency_id,
                    self.order_id.company_id,
                    self.date_order or fields.Date.today(),
                )

            if self.product_uom:
                price_unit = self.product_id.uom_id._compute_price(price_unit, self.product_uom)

            self.price_unit = price_unit
            return

        price_unit = self.env['account.tax']._fix_tax_included_price_company(seller.price, self.product_id.supplier_taxes_id, self.taxes_id, self.company_id) if seller else 0.0
        if price_unit and seller and self.order_id.currency_id and seller.currency_id != self.order_id.currency_id:
            price_unit = seller.currency_id._convert(
                price_unit, self.order_id.currency_id, self.order_id.company_id, self.date_order or fields.Date.today())

        if seller and self.product_uom and seller.product_uom != self.product_uom:
            price_unit = seller.product_uom._compute_price(price_unit, self.product_uom)

        self.price_unit = price_unit
            
    
        