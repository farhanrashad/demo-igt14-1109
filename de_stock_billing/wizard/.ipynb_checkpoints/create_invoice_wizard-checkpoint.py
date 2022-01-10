# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date


class CreateInvoiceWizard(models.Model):
    _name = 'create.invoice.wizard'
    _description='Create Invoice Wizard'
    
    def get_default_journal(self):
        journal = self.env['account.journal'].search([('type','=','purchase')], limit=1)
        return journal
    journal_id = fields.Many2one('account.journal', string='Journal', required=True, default=get_default_journal)
    invoice_date = fields.Datetime(string='Invoice Date' , default=fields.Datetime.now)
    picking_ids = fields.Many2many('stock.picking', string='Picking')
    
    def action_create_bill(self):
        """Create the invoice associated to the PO.
        """
        move_type = 'entry'
        if self.journal_id.type == 'purchase':
            move_type = 'in_invoice'
        elif self.journal_id.type == 'sale':
            move_type = 'out_invoice'    
        
        vendor_list = []
        for picking in self.picking_ids:
            vendor_list.append(picking.partner_id.id)  
        uniq_vendor_list = set(vendor_list)
        for partner in uniq_vendor_list:
            product_list = []
            picking_list = ' '
            for picking in self.picking_ids:
                if picking.partner_id.id == partner:
                    currency_id = 0
                    picking_list = picking_list + ' '+ str(picking.name)
                    if not picking.state == 'done':
                        raise UserError(_("Please validate delivery to create bill '%s'.", picking.name))
                    if picking.invoice_control == '2binvoice':
                        partner = 0
                        purchaseorder = self.env['purchase.order'].search([('name','=',picking.origin)])
                        if purchaseorder:
                            partner = purchaseorder.partner_id.id
                            currency_id = purchaseorder.currency_id.id
                            for picking_line in picking.move_ids_without_package:
                                purchase_line = self.env['purchase.order.line'].search([('order_id','=',purchaseorder.id),('product_id','=',picking_line.product_id.id)])
                                for po_line in purchase_line:
                                    product_list.append((0,0, {
                                                'product_id': po_line.product_id.id,
                                                'currency_id': po_line.currency_id.id, 
                                                'name': '%s: %s' % (picking.name, po_line.name),
                                                'quantity': picking_line.product_uom_qty if  picking.state!='done' else picking_line.quantity_done, 
                                                'price_unit': po_line.price_unit,
                                                'partner_id': purchaseorder.partner_id.id,
                                                'purchase_line_id': po_line.id,
                                                    }))

                        else:

                            partner = purchaseorder.partner_id.id
                            for picking_line in picking.move_ids_without_package:

                                product_list.append((0,0, {
                                            'product_id': picking_line.product_id.id, 
                                            'currency_id': picking_line.currency_id.id, 
                                            'name': '%s: %s' % (picking.name, picking_line.product_id.name),
                                            'quantity': picking_line.product_uom_qty if  picking.state!='done' else picking_line.quantity_done, 
                                            'price_unit': picking_line.product_id.standard_price,
                                            'partner_id': picking.partner_id.id,
                                                }))
                       
            vals = {
                'partner_id': partner,
                'journal_id': self.journal_id.id,
                'invoice_date': self.invoice_date,
                'move_type': move_type,
                'currency_id': currency_id if currency_id > 0 else  False,
                'invoice_origin': picking_list,
                'invoice_line_ids': product_list   
                }
            move = self.env['account.move'].create(vals)
            for picking in self.picking_ids:
                if picking.partner_id.id == partner:
                    picking.update({
                            'move_id': move.id, 
                            'invoice_control': 'invoiced',
                            })           
                            

