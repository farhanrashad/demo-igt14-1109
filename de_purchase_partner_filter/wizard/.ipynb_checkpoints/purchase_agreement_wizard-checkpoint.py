# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import time
from odoo import api, fields, models, _
from datetime import datetime
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError


class PurchaseAgreementWizard(models.TransientModel):
    _name = 'purchase.requisition.wizard'
    _description = "Wizard to create purchase order from purchase requisition"

    wizard_line_ids = fields.One2many( 'purchase.requisition.line.wizard', 'wizard_id',string="Wizard Line")
    partner_id = fields.Many2one('res.partner', string='Vendor', required = True)
    partner_ids = fields.Many2many('res.partner', string='Partners', compute="_compute_partners")
    select_all = fields.Boolean(string='Select All', default=False)
    #company_id = fields.Many2one('res.company', related='requisition_id.company_id', string='Company', store=True, readonly=True, default= lambda self: self.env.company)
    #currency_id = fields.Many2one('res.currency', 'Currency', required=True, default=lambda self: self.env.company.currency_id.id)

    #date_order = fields.Datetime(string='Order Date', required=True, copy=False, default=fields.Datetime.now)
    @api.onchange('select_all')
    def _select_all(self):
        for line in self.wizard_line_ids:
            line.record_selection = self.select_all
                
    @api.model
    def default_get(self,  default_fields):
        res = super(PurchaseAgreementWizard, self).default_get(default_fields)
        requisition_id = self.env['purchase.requisition'].browse(self._context.get('active_ids',[]))
        pr_lines_list = []
        for line in requisition_id.line_ids:
            if (line.product_qty - line.qty_ordered) > 0:
                pr_lines_list.append((0,0,{
                    'product_id' : line.product_id.id,
                    'product_uom' : line.product_uom_id.id,
                    'requisition_id': line.requisition_id.id,
                    'name' : line.product_description_variants,
                    'product_qty' : line.product_qty - line.qty_ordered,
                    'price_unit' : line.price_unit,
                }))
        res.update({
            'wizard_line_ids':pr_lines_list,
            #'vendor_ids' : [(4, x.id) for x in self.wizard_line_ids if x.state not in ('done', 'cancel')],
        })
        return res

    @api.depends('wizard_line_ids.product_id','wizard_line_ids.record_selection')
    def _compute_partners(self):
        vendors = filtered_vendors = self.env['res.partner']
        vend_product = self.env['product.supplierinfo']
        
        pricelist_ids = self.env['product.supplierinfo']
        item_count = 0
        
        for wizard in self:
            vendors = wizard.wizard_line_ids.filtered(lambda p: p.record_selection == True).partner_ids
            for vendor in vendors:
                item_count = 0
                for line in wizard.wizard_line_ids.filtered(lambda p: p.record_selection == True):
                    #vend_product = self.env['product.supplierinfo'].search([('product_tmpl_id','=',line.product_id.product_tmpl_id.id),('name','=',vendor.id)],limit=1)
                    if vendor in line.partner_ids:
                    #if vend_product:
                    #if line.product_id.product_tmpl_id.id == vendor.product_tmpl_id.id:
                        item_count += 1
                if item_count == len(wizard.wizard_line_ids.filtered(lambda p: p.record_selection == True)):
                    filtered_vendors += vendor
                        
            wizard.partner_ids = filtered_vendors
        #if all()
            
        #cr.execute("SELECT id, num_bl FROM stock_picking WHERE state='done' and invoice_state='2binvoiced' and partner_id= %d" %(partner) )
        #if all(picking.state == 'done' for picking in order.picking_ids.filtered(lambda p: p.picking_type_id.id == order.picking_type_id.id)) and any(picking.state in ('waiting','confirmed','assigned') for picking in order.picking_ids.filtered(lambda p: p.picking_type_id.id == order.transfer_order_category_id.return_picking_type_id.id)):

        
    @api.depends('wizard_line_ids.product_id')
    def _compute_partners1(self):
        #vendors = self.env['res.partner'].search([])
        vendors = self.env['res.partner']
        vend_product = self.env['product.supplierinfo']
        item_count = 0
        partners = self.env['res.partner']
        for wizard in self:
            #for vend in wizard.wizard_line_ids.partner_ids:
                #vendors += vend
            for vendor in wizard.wizard_line_ids.partner_ids:
                item_count = 0
                for line in wizard.wizard_line_ids:
                    vend_product = self.env['product.supplierinfo'].search(['|',('product_tmpl_id','=',line.product_id.product_tmpl_id.id),('product_id','=',line.product_id.id),'&', ('name','=',vendor.id)],limit=1)
                    if vend_product:
                    #if line.product_id.product_tmpl_id.id == vendor.product_tmpl_id.id:
                        item_count += 1
                    if item_count == len(wizard.wizard_line_ids):
                        partners += vendor
            wizard.partner_ids = wizard.wizard_line_ids.partner_ids #partners
            
            
    def action_create_purchase_order(self):
        self.ensure_one()
        purchase_id = self.env['purchase.order'].browse(self._context.get('id',[]))
        order_lines_list = []
        requisition_id = self.env['purchase.requisition'].browse(self._context.get('active_id'))
        pricelist = self.partner_id.property_product_pricelist
        partner_pricelist = self.partner_id.property_product_pricelist
        order_name = ""
        price = 0
        for data in self.wizard_line_ids.filtered(lambda p: p.record_selection == True):
            order_name = data.requisition_id.name
            if not order_name:
                order_name = requisition_id.name
            if partner_pricelist:
                product_context = dict(self.env.context, partner_id=self.partner_id.id, date=fields.Datetime.now(), uom=data.product_uom.id)
                final_price, rule_id = partner_pricelist.with_context(product_context).get_product_price_rule(data.product_id, data.product_qty or 1.0, self.partner_id)
			
            else:
                final_price = data.product_id.standard_price
            if data.price_unit == 0 or not data.price_unit:
                price = final_price
            else:
                price = data.price_unit
            
            #pricelist
            order_lines_list.append([0,0,{
                'product_id' : data.product_id.id,
				'name' : data.product_id.name,
				'product_qty' : data.product_qty,
				#'purchase_demand_line_id':data.purchase_demand_id.id,
				'product_uom' : data.product_uom.id,
				'taxes_id' : data.product_id.supplier_taxes_id.ids,
				'date_planned' : data.date_planned,
				'price_unit' : price,
                #'analytic_tag_ids': [(6, 0, line.analytic_tag_ids.ids)],
                #'partner_ids': [(6, 0, line.analytic_tag_ids.ids)],
            }])
        purchase_id.create({
            'partner_id' : self.partner_id.id,
            'date_order' : fields.Datetime.now(),
            'company_id': requisition_id.company_id.id,
            'currency_id': requisition_id.currency_id.id,
            'order_line':order_lines_list,
            'origin' : order_name,
            'partner_ref' : order_name,
            'requisition_id' : requisition_id.id,
        })
        return purchase_id


class PurchaseAgreementLineWizard(models.TransientModel):
    _name = 'purchase.requisition.line.wizard'
    _description = "Get purchase requisition lines in wizard"
    
    wizard_id = fields.Many2one('purchase.requisition.wizard')
    record_selection = fields.Boolean(string='Selection', default=False)
    product_id = fields.Many2one('product.product', string="Product", required=True)
    name = fields.Char(string="Description")
    product_qty = fields.Float(string='Quantity', required=True)
    date_planned = fields.Datetime(string='Scheduled Date', default = datetime.today())
    product_uom = fields.Many2one('uom.uom', string='Product Unit of Measure')
    requisition_id = fields.Many2one('purchase.requisition', string='Requisition', ondelete='cascade', index=True)
    price_unit = fields.Float(string='Unit Price', digits='Product Price')
    product_subtotal = fields.Float(string="Sub Total", compute='_compute_total')
    partner_ids = fields.Many2many('res.partner', string='Partners', compute='_compute_partners')
    
    @api.depends('product_qty', 'price_unit')
    def _compute_total(self):
        for record in self:
            record.product_subtotal = record.product_qty * record.price_unit
            
    def _compute_partners(self):
        pricelist = self.env['product.supplierinfo']
        vendors = self.env['res.partner']
        for line in self:
            vendors = self.env['res.partner']
            pricelist_ids = self.env['product.supplierinfo'].search([('product_tmpl_id','=',line.product_id.product_tmpl_id.id)])
            for pl in pricelist_ids:
                vendors += pl.name
            line.partner_ids = vendors