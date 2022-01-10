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

READONLY_STATES = {
    'confirm': [('readonly', True)],
    'provision': [('readonly', True)],
    'paid': [('readonly', True)],
    'done': [('readonly', True)],
    'cancel': [('readonly', True)],
}

class AccountBill(models.Model):
    _name = 'account.custom.bill'
    _description = 'Custom Accounting Bills'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    company_id = fields.Many2one('res.company', 'Company', copy=False, required=True, index=True, default=lambda s: s.env.company, states=READONLY_STATES)
    currency_id = fields.Many2one('res.currency', 'Currency', required=True, states=READONLY_STATES,
                                  default=lambda self: self.env.company.currency_id.id)
    user_id = fields.Many2one('res.users', string='Purchase Representative', index=True, tracking=True,
        default=lambda self: self.env.user, check_company=True,states=READONLY_STATES,)
    
    custom_bill_type_id = fields.Many2one('account.custom.bill.type', string='Bill Type', index=True, required=True, states=READONLY_STATES,)


    state = fields.Selection([
        ('draft', 'New'),
        ('confirm', 'Confirmed'),
        ('provision', 'Paid in Advance'),
        ('paid', 'Actual Paid'),
        ('done', 'Closed'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, tracking=4, default='draft')

    date_from = fields.Date('From Date', required=True, states=READONLY_STATES, index=True, copy=False,)
    date_to = fields.Date('To Date', required=True, states=READONLY_STATES, index=True, copy=False,)

    ref = fields.Char(string='Reference')
    description = fields.Char('Description')
    
    invoice_date = fields.Date('Bill Date', required=True, states=READONLY_STATES,)
    partner_id = fields.Many2one('res.partner', 'Partner', required=True, states=READONLY_STATES,)
    
    date_confirm = fields.Datetime('Confirm Date', readonly=True)
    date_advance_payment = fields.Date('Advance Payment Date', readonly=True)
    date_actual_bill = fields.Date('Actual Bill Date', readonly=True)
    
    amount_forecast = fields.Float('Advance Pay Amount', compute='_amount_all')
    total_amount = fields.Float('Actual Bill Amount', compute='_amount_all')
    
    custom_bill_line = fields.One2many('account.custom.bill.line', 'custom_bill_id', string='Custom Bill Line', copy=True, auto_join=True)    

    bill_count = fields.Integer('Vendor Bill', compute='_compute_bill_count')

    @api.model
    def create(self, values):
        if values.get('name', _('New')) == _('New'):
            values['name'] = self.env['ir.sequence'].next_by_code('custom.account.bill') or _('New')
        return super(AccountBill, self).create(values)
    
    def _compute_bill_count(self):
        self.bill_count = self.env['account.move'].search_count([('custom_bill_id','=',self.id)])

    @api.depends('custom_bill_line','custom_bill_line.amount_forecast','custom_bill_line.total_amount')
    def _amount_all(self):
        adv = tot = 0
        for line in self.custom_bill_line:
            adv += line.amount_forecast
            tot += line.total_amount
        self.amount_forecast = adv
        self.total_amount = tot
            
    def get_VendorBill(self):
        """
        To get Count against MO for Different PO
        """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'binding_type': 'action',
            'name': 'Vendor Bill',
            'res_model': 'account.move',
            'domain': [('invoice_origin', '=', self.name)],
            'target': 'current',
            'view_mode': 'tree,form',
        }

    def action_confirm(self):
        self.state = 'confirm'
        self.date_confirm = fields.Datetime.now()

    def action_approved(self):
        self.state = 'approved'

    def action_done(self):
        self.state = 'done'

    def create_advance_bill(self):
        line_vals = []
        for line in self:
            line_vals.append((0, 0, {
                'name': line.name,
                'account_id': line.custom_bill_type_id.adv_account_id.id,
                'quantity': 1,  
                'currency_id': line.currency_id.id,
                'price_unit': line.amount_forecast,
            }))
            line_vals.append(line_vals)

        vals = {
            'partner_id': self.partner_id.id,
            'journal_id': line.custom_bill_type_id.adv_journal_id.id,
            'invoice_date_due': False,
            'invoice_date': fields.Date.today(),
            'move_type': 'in_invoice',
            'invoice_origin': self.name,
            'custom_bill_id':self.id,
            'invoice_line_ids': line_vals,
        }
        move = self.env['account.move'].create(vals)
        if move:
            self.state = 'provision'
            self.date_advance_payment = fields.Datetime.now()
        else:
            raise UserError("Unable to Create Vendor Bill")

    def create_actual_bill(self):
        line_vals = []
        for line in self.custom_bill_line:
            line_vals.append((0, 0, {
                'product_id': line.product_id.id,
                'name': line.product_id.name,
                'quantity': 1,  # self.schedule_id.order_line.product_qty
                # 'currency_id': line.currency_id.id,
                'price_unit': line.total_amount,
                'product_uom_id': line.product_uom.id,
                'custom_bill_line_id': line.id,
                'analytic_account_id': line.analytic_account_id.id,
                'analytic_tag_ids': [(6, 0, line.analytic_tag_ids.ids)],
                'project_id': line.project_id.id,
            }))
            line_vals.append(line_vals)

        vals = {
            'partner_id': self.partner_id.id,
            'journal_id': self.custom_bill_type_id.act_journal_id.id,
            'invoice_date': fields.Date.today(),
            'move_type': 'in_invoice',
            'invoice_origin': self.name,
            'custom_bill_id':self.id,
            'invoice_line_ids': line_vals,
        }
        move = self.env['account.move'].create(vals)
        self.state = 'paid'
        self.date_actual_bill = fields.Datetime.now()

class AccountBillLine(models.Model):
    _name = 'account.custom.bill.line'
    _description = 'Custom Bill Line'

    custom_bill_id = fields.Many2one('account.custom.bill', string='Custom Bill', required=True, ondelete='cascade', index=True, copy=False)

    date_from = fields.Date(related='custom_bill_id.date_from')
    date_to = fields.Date(related='custom_bill_id.date_to')
   
    project_id = fields.Many2one('project.project', string="Projects", check_company=True)
    analytic_account_id = fields.Many2one('account.analytic.account', store=True, string='Analytic Account', )
    analytic_tag_ids = fields.Many2many('account.analytic.tag', store=True, string='Analytic Tags', )

    product_id = fields.Many2one('product.product', string="Products", check_company=True)
    product_uom = fields.Many2one('uom.uom', string="UOM", domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')

    company_id = fields.Many2one(related='custom_bill_id.company_id')
    amount_forecast = fields.Float('Forecast', help='Bill Forecast')
    meter_number = fields.Char('Meter')
    opening_reading = fields.Integer('Opening Reading', help='Opening reading of meter')
    closing_reading = fields.Integer('Closing Reading', help='Closing Reading of meter')
    total_unit = fields.Integer('Total Unit', compute='_compute_total_units')
    additional_unit = fields.Integer('Additional Units')
    maintainence_fee = fields.Float('Mnt. Fees', help='Maintenance Fees')
    hp_fee = fields.Float('HP Fee', help='Horsepower Fees')
    KHW_charges = fields.Float('KHW')
    actual_KHW_charges = fields.Float('Actual KHW')
    total_amount = fields.Float('Total', compute='_compute_total_amount')
    other_charges = fields.Float('Other Charges')

    def _compute_total_units(self):
        for rec in self:
            rec.total_unit = rec.closing_reading - rec.opening_reading

    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = rec.maintainence_fee + rec.hp_fee + rec.KHW_charges + rec.other_charges
