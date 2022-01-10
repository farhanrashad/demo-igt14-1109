# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date
from dateutil.relativedelta import relativedelta

import json
from lxml import etree

class AccountCustomEntryStage(models.Model):
    _inherit = 'account.custom.entry.stage'
    
    edit_om_deudction = fields.Boolean(string='Allow Editing for OM Deduction')
    
class CustomEntry(models.Model):
    _inherit = 'account.custom.entry'
    
    #App fields
    has_om = fields.Selection(related="custom_entry_type_id.has_om")
    allow_advance_inv = fields.Boolean(related='custom_entry_type_id.allow_advance_inv')
    om_amount_advance_bal = fields.Float(string='OM Advance Amount', copy=False)
    om_amount_advance_per = fields.Float(string='OM Advance %age', copy=False)
    om_amount_adv_current_per = fields.Float(string='OM Adv. Current %age', copy=False)
    
    om_deduction_total = fields.Monetary(string='Total Deduction', compute='_compute_all_deductions')
    om_amount_total = fields.Monetary(string='Total Amount', compute='_compute_all_total')
    om_amount_final_total = fields.Monetary(string='Final Total Amount', compute='_compute_all_total')
    om_amount_completion_per = fields.Monetary(string='Completion Per.', compute='_compute_all_total')
    om_amount_total_per = fields.Float(string='Completion %age', compute='_compute_all_total')
    om_invoiced_amount = fields.Monetary(string='Invoiced Amount', compute='_compute_all_total')
    
    credit_note_attachment = fields.Binary(string='Credit Note Attachment')
    crn_ref = fields.Char(string='CRN Reference')
    
    custom_entry_om_deduction_line = fields.One2many('account.custom.entry.om.deduction', 'custom_entry_id', string='OM Deduction', copy=True, auto_join=True,)
    
    om_invoice_count = fields.Integer(string='Invoice Count', compute='_get_om_invoiced', readonly=True)
    om_invoice_ids = fields.Many2many("account.move", string='Invoices', compute="_get_om_invoiced", readonly=True, copy=False)
    
    edit_om_deudction = fields.Boolean(related='stage_id.edit_om_deudction')
    allow_om_deudction = fields.Boolean(related='custom_entry_type_id.allow_om_deudction')
    
    def _compute_all_deductions(self):
        for entry in self:
            total = 0
            for line in entry.custom_entry_om_deduction_line:
                total += line.amount
            entry.om_deduction_total = total
            
    def _compute_all_total(self):
        for entry in self:
            total = final_total = comp = 0
            for line in entry.custom_entry_line:
                total += line.o_amount
                final_total += line.o_final_amount
                comp = entry.om_amount_advance_per
            entry.om_amount_total = total
            entry.om_amount_final_total = final_total
            entry.om_amount_total_per = comp
            entry.om_invoiced_amount = entry.om_amount_advance_bal
    
    def create_journal_entry(self):
        res = super(CustomEntry, self).create_journal_entry()
        if self.custom_entry_om_deduction_line:
            self._create_credit_invoice()
        return res
    
    def entry_close(self):
        self.update({
            'stage_id' : self.stage_id.next_stage_id.id,
        })
        
    def create_bill(self):
        res = super(CustomEntry, self).create_bill()
        if self.custom_entry_om_deduction_line:
            self._create_credit_invoice()
        return res
    
    def _create_credit_invoice(self):
        invoice = self.env['account.move']
        lines_data = []
        for line in self.custom_entry_om_deduction_line:
            lines_data.append([0,0,{
                'name': str(self.name) + ' ' + str(line.om_deduction_type_id.name),
                #'custom_entry_line_id': line.id,
                'price_unit': line.amount or 0.0,
                #'discount': line.discount,
                'quantity': 1.0,
                'product_uom_id': line.om_deduction_type_id.product_id.uom_id.id,
                'product_id': line.om_deduction_type_id.product_id.id,
                'tax_ids': [(6, 0, line.om_deduction_type_id.product_id.supplier_taxes_id.ids)],
                #'analytic_account_id': line.analytic_account_id.id,
                #'analytic_tag_ids': [(6, 0, line.analytic_tag_ids.ids)],
                'project_id': line.project_id.id,
            }])
        invoice.create({
            'move_type': 'in_refund',
            'custom_entry_id': self.id,
            'invoice_date': fields.Datetime.now(),
            'partner_id': self.partner_id.id,
            #'partner_shipping_id': self.partner_id.id,
            'currency_id': self.currency_id.id,
            'journal_id': self.custom_entry_type_id.advance_journal_id.id,
            'invoice_origin': self.name,
            #'fiscal_position_id': fpos.id,
            'invoice_payment_term_id': self.partner_id.property_supplier_payment_term_id.id,
            'narration': self.name,
            'invoice_user_id': self.user_id.id,
            #'partner_bank_id': company.partner_id.bank_ids.filtered(lambda b: not b.company_id or b.company_id == company)[:1].id,
            'invoice_line_ids':lines_data,
        })
        return invoice
    
    @api.depends('custom_entry_line.invoice_lines')
    def _get_om_invoiced(self):
        # The invoice_ids are obtained thanks to the invoice lines of the SO
        # lines, and we also search for possible refunds created directly from
        # existing invoices. This is necessary since such a refund is not
        # directly linked to the SO.
        for entry in self:
            invoices = self.env['account.move'].search([('custom_entry_id','=',self.id),('move_type','in',['in_invoice','in_refund'])])
            entry.om_invoice_ids = invoices
            entry.om_invoice_count = len(invoices)
            
    def action_view_om_invoices(self):
        #invoices = self.custom_entry_line.invoice_lines.move_id.filtered(lambda r: r.move_type in ('in_invoice','in_refund'))
        invoices = self.env['account.move'].search([('custom_entry_id','=',self.id),('move_type','in',['in_invoice','in_refund'])])
        action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_out_invoice_type")
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            form_view = [(self.env.ref('account.view_move_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = invoices.id
        else:
            action = {'type': 'ir.actions.act_window_close'}

        context = {
            'default_move_type': 'in_invoice',
        }
        return action
    

class CustomEntryLine(models.Model):
    _inherit = 'account.custom.entry.line'
    
    #OM line Item Fields
    o_tower_type = fields.Selection([
        ('COW', 'COW'),
        ('GBT', 'GBT'),
        ('RTP', 'RTP')],
        string='OM Tower Type')
    o_product_id = fields.Many2one('product.product', string="OM Power Model Product", check_company=True)
    o_date_rfi = fields.Date(string='RFI Date', )
    o_date_onair = fields.Date(string='On Air Date', )
    o_date_handover = fields.Date(string='Handover Date', )
    o_date_start = fields.Date(string='Start Date', )
    o_date_end = fields.Date(string='End Date', )
    o_days_rfi = fields.Integer(string='RFI Days')
    o_days_onair = fields.Integer(string='On Air Days')
    o_amount = fields.Float(string='OM Amount' )
    o_final_amount = fields.Float(string='OM Final Amount' )
    o_charges = fields.Float(string='OM Service Charges' )

class AccountCustomEntryOMDeduction(models.Model):
    _name = 'account.custom.entry.om.deduction'
    _description = 'Custom Entry OM Deduction'
    
    custom_entry_id = fields.Many2one('account.custom.entry', string='Custom Entry', required=True, ondelete='cascade', index=True, copy=False)
    
    project_id = fields.Many2one('project.project', string="Project", check_company=True, ondelete='cascade')
    company_id = fields.Many2one('res.company', related='custom_entry_id.company_id')
    currency_id = fields.Many2one('res.currency',related='custom_entry_id.currency_id')
    om_deduction_type_id = fields.Many2one('account.custom.entry.om.deduction.type', string='Deduction Type', index=True)
    amount = fields.Monetary(string='Amount')

    
    