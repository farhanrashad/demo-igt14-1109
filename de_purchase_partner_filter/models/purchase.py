# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    partner_ids = fields.Many2many('res.partner', compute="_compute_partners", string='Partners', copy=False)
    #total_items = fields.Integer(string='Total Items', compute="_compute_partners" )

    def show_message(self):
        #vendors = self.env['product.supplierinfo'].search([('name','!=', False)])
        vendors = self.env['res.partner'].search([('name','!=',False)])
        vend_product = self.env['product.supplierinfo']
        item_count = 0
        partners = ''
        for order in self:
            for vendor in vendors:
                #if all(line.product_id.product_tmpl_id.id == vendor.product_tmpl_id.id for line in order.order_line):
                 #   partners = partners + vendor.name.name
                #item_count += 1
                #.filtered(lambda p: p.picking_type_id.id == order.picking_type_id.id)):

                item_count = 0
                for line in order.order_line:
                    vend_product = self.env['product.supplierinfo'].search([('product_tmpl_id','=',line.product_id.product_tmpl_id.id),('name','=',vendor.id)],limit=1)
                    if vend_product:
                    #if line.product_id.product_tmpl_id.id == vendor.product_tmpl_id.id:
                        item_count += 1
                    if item_count == len(order.order_line):
                        partners += vendor.name
            raise UserError(_("partners='%s' ,items='%s'", partners, str(item_count)))
        
    @api.depends('order_line.product_id')
    def _compute_partners(self):
        vendors = self.env['res.partner'].search([('name','!=',False)])
        vend_product = self.env['product.supplierinfo']
        item_count = 0
        partners = self.env['res.partner']
        for order in self:
            for vendor in vendors:
                item_count = 0
                for line in order.order_line:
                    vend_product = self.env['product.supplierinfo'].search([('product_tmpl_id','=',line.product_id.product_tmpl_id.id),('name','=',vendor.id)],limit=1)
                    if vend_product:
                    #if line.product_id.product_tmpl_id.id == vendor.product_tmpl_id.id:
                        item_count += 1
                    if item_count == len(order.order_line):
                        partners += vendor
            order.partner_ids = partners
            #order.total_items = len(order.order_line)
            #raise UserError(_("Total Count '%s'.", item_count))
    
    def button_confirm1(self):
        for order in self:
            if order.partner_id not in order.partner_ids:
                raise ValidationError(_("One or more products are not avaiable for vendor '%s'.", order.partner_id.name))
    
            if order.state not in ['draft', 'sent']:
                continue
            order._add_supplier_to_product()
            # Deal with double validation process
            if order._approval_allowed():
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
            if order.partner_id not in order.message_partner_ids:
                order.message_subscribe([order.partner_id.id])
        return True
    
    #@api.constrains('partner_id', 'partner_ids')
    def _check_partner(self):
        for order in self:
            if order.state != 'draft' or self.env.context.get('state') != 'draft':
                if order.partner_id not in order.partner_ids:
                    raise ValidationError(_("One or more products are not avaiable for vendor '%s'.", order.partner_id.name))
    
    @api.onchange('order_line')
    def _onchange_product_id(self):
        self.partner_id = False
        
class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.order_id.partner_id = False