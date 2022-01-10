# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date
from dateutil.relativedelta import relativedelta

import json
from lxml import etree

MONTH_LIST = [('1', 'Jan'), ('2', 'Feb'), ('3', 'Mar'), ('4', 'Apr'), ('5', 'May'), ('6', 'Jun'), ('7', 'Jul'), ('8', 'Aug'), ('9', 'Sep'), ('10', 'Oct'), ('11', 'Nov'),('12', 'Dec')]

class CustomEntry(models.Model):
    _name = 'account.custom.entry'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Custom Entry'
    _order = "date_entry desc"
    
    def _get_default_stage_id(self):
        """ Gives default stage_id """
        custom_entry_type_id = self.env.context.get('default_custom_entry_type_id')
        if not custom_entry_type_id:
            return False
        return self.stage_find(custom_entry_type_id, [('fold', '=', False)])
    
    def _get_default_currency_id(self):
        default_currency_id = self.env.context.get('default_currency_id')
        return [default_currency_id] if default_currency_id else None
    
    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    date_entry = fields.Datetime(string='Entry Date', required=True, index=True, copy=False, default=fields.Datetime.now,)
    date_entry_month = fields.Selection(MONTH_LIST, string='Month')
    date_entry_year = fields.Char(string='Year', store=True)

    date_submit = fields.Datetime('Submission Date', readonly=False)
    date_approved = fields.Datetime('Approved Date', readonly=False)

    user_id = fields.Many2one('res.users', string="Request Owner",check_company=True, domain="[('company_ids', 'in', company_id)]", default=lambda self: self.env.user, required=True,readonly=True, )
    company_id = fields.Many2one('res.company', 'Company', copy=False, required=True, index=True, default=lambda s: s.env.company)
    currency_id = fields.Many2one('res.currency', 'Currency', required=True, default=_get_default_currency_id)
    
    stage_id = fields.Many2one('account.custom.entry.stage', string='Stage', compute='_compute_stage_id', store=True, readonly=False, ondelete='restrict', tracking=True, index=True, default=_get_default_stage_id, domain="[('custom_entry_type_ids', '=', custom_entry_type_id)]", copy=False)
    custom_entry_type_id = fields.Many2one('account.custom.entry.type', string='Entry Type', index=True, required=True, readonly=True,)
    
    amount_advanced_total = fields.Monetary('Total Advanced', compute='_amount_all')
    amount_total = fields.Monetary('Total Amount', compute='_amount_all', store=True)
    amount_balance = fields.Monetary('Balance', compute='_amount_all')
 
    custom_entry_line = fields.One2many('account.custom.entry.line', 'custom_entry_id', string='Entry Line', copy=True, auto_join=True,)
    
    @api.onchange('custom_entry_type_id')
    def _onchange_entry_type(self):
        for entry in self:
            entry.currency_id = entry.custom_entry_type_id.currency_id.id
    
    #account related fields
    stage_category = fields.Selection(related='stage_id.stage_category')
    stage_code = fields.Char(related='stage_id.stage_code')
    account_entry_type = fields.Char(string='Accounting Entry Type', compute='_account_entry_type', )
    expense_advance = fields.Boolean(related='custom_entry_type_id.expense_advance')
    journal_id = fields.Many2one('account.journal',related='custom_entry_type_id.journal_id')
    journal_type = fields.Selection(related='custom_entry_type_id.journal_type')
    move_type = fields.Selection(related='custom_entry_type_id.move_type')
    
    
    partner_id = fields.Many2one('res.partner', string='Vendor', ondelete='cascade', change_default=True, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", help="You can find a vendor by its Name, TIN, Email or Internal Reference.")
    
    
    #Header optional fields
    has_partner = fields.Selection(related="custom_entry_type_id.has_partner")
    has_ref = fields.Selection(related="custom_entry_type_id.has_ref")
    has_supplier_bill = fields.Selection(related="custom_entry_type_id.has_supplier_bill")
    has_period = fields.Selection(related="custom_entry_type_id.has_period")
    has_attachment = fields.Selection(related="custom_entry_type_id.has_attachment")
    has_description = fields.Selection(related="custom_entry_type_id.has_description")
    has_purchase_requisition = fields.Selection(related="custom_entry_type_id.has_purchase_requisition")
    has_purchase = fields.Selection(related="custom_entry_type_id.has_purchase")
    has_picking = fields.Selection(related="custom_entry_type_id.has_picking")
    has_invoice = fields.Selection(related="custom_entry_type_id.has_invoice")
    has_transfer_order = fields.Selection(related="custom_entry_type_id.has_transfer_order")
    
    ref = fields.Char('Reference', copy=False)
    supplier_bill_ref = fields.Char(string='Supplier Bill Ref.')
    attachment1 = fields.Boolean(string='Attachment 1')
    description = fields.Text(string='Description')
    purchase_requisition_id = fields.Many2one('purchase.requisition', string="Requisition", check_company=True, ondelete='cascade')
    purchase_id = fields.Many2one('purchase.order', string="Purchase Order", check_company=True, ondelete='cascade')
    invoice_id = fields.Many2one('account.move', string="Invoice Reference", check_company=True, ondelete='cascade')
    picking_id = fields.Many2one('stock.picking', string="Picking Reference", check_company=True, ondelete='cascade')
    stock_transfer_order_id = fields.Many2one('stock.transfer.order', string="Transfer Order", check_company=True, ondelete='cascade')
    
    
    #optional line items fields
    has_line_period = fields.Selection(related="custom_entry_type_id.has_line_period")
    has_note = fields.Selection(related="custom_entry_type_id.has_note")
    has_project = fields.Selection(related="custom_entry_type_id.has_project")
    has_analytic = fields.Selection(related="custom_entry_type_id.has_analytic")
    has_product = fields.Selection(related="custom_entry_type_id.has_product")
    has_employee = fields.Selection(related="custom_entry_type_id.has_employee")
    has_supplier = fields.Selection(related="custom_entry_type_id.has_supplier")
    has_advanced = fields.Selection(related="custom_entry_type_id.has_advanced")
    
    
    #invoice_ids = fields.Many2many('account.move', compute="_compute_invoice", string='Bills', copy=False, store=True)
    #move_ids = fields.Many2many('account.move', compute="_compute_invoice", string='Journal Entries', copy=False, store=True)
    #invoice_count = fields.Integer(compute="_compute_all_moves", string='Bill Count', copy=False, default=0,)
    #move_count = fields.Integer(compute="_compute_all_moves", string='Move Count', copy=False, default=0)
    
    invoice_count = fields.Integer(string='Invoice Count', compute='_get_invoiced', readonly=True)
    invoice_ids = fields.Many2many("account.move", string='Invoices', compute="_get_invoiced", readonly=True, copy=False)
    
    move_count = fields.Integer(string='Move Count', compute='_get_moves', readonly=True)
    move_ids = fields.Many2many("account.move", string='Moves', compute="_get_moves", readonly=True, copy=False)


    
    @api.depends('date_entry')
    def _compute_entry_year(self):
        for entry in self: 
            entry_year = entry.date_entry
            entry.date_entry_year = entry_year.year

    @api.depends('stage_id')
    def _account_entry_type(self):
        for entry in self:
            if entry.stage_id.next_stage_id:
                entry.account_entry_type = entry.stage_id.next_stage_id.account_entry_type
            else:
                entry.account_entry_type = 'none'
                
    @api.depends('custom_entry_type_id')
    def _compute_stage_id(self):
        for entry in self:
            if entry.custom_entry_type_id:
                if entry.custom_entry_type_id not in entry.stage_id.custom_entry_type_ids:
                    entry.stage_id = entry.stage_find(entry.custom_entry_type_id.id, [
                        ('fold', '=', False)])
            else:
                entry.stage_id = False
    
    def stage_find(self, section_id, domain=[], order='sequence'):
        """ Override of the base.stage method
            Parameter of the stage search taken from the lead:
            - section_id: if set, stages must belong to this section or
              be a default stage; if not set, stages must be default
              stages
        """
        # collect all section_ids
        section_ids = []
        if section_id:
            section_ids.append(section_id)
        section_ids.extend(self.mapped('custom_entry_type_id').ids)
        search_domain = []
        if section_ids:
            search_domain = [('|')] * (len(section_ids) - 1)
            for section_id in section_ids:
                search_domain.append(('custom_entry_type_ids', '=', section_id))
        search_domain += list(domain)
        # perform search, return the first found
        return self.env['account.custom.entry.stage'].search(search_domain, order=order, limit=1).id
    
    
    def stage_find(self, section_id, domain=[], order='sequence'):
        section_ids = category_ids = []
        if section_id:
            section_ids.append(section_id)
        section_ids.extend(self.mapped('custom_entry_type_id').ids)
        search_domain = []
        if section_ids:
            search_domain = [('|')] * (len(section_ids) - 1)
            for section_id in section_ids:
                search_domain.append(('custom_entry_type_ids', '=', section_id))
        search_domain += list(domain)
        return self.env['account.custom.entry.stage'].search(search_domain, order=order, limit=1).id
    
    @api.depends('custom_entry_line.invoice_lines.move_id')
    def _compute_invoice(self):
        for entry in self:
            if self._context.get('open_invoices', True):
                if entry.journal_id.type == 'purchase':
                    invoices = entry.mapped('custom_entry_line.invoice_lines.move_id')
            else:
                if entry.journal_id.type == 'general':
                    invoices = entry.mapped('custom_entry_line.invoice_lines.move_id')
            entry.invoice_ids = invoices
            #elif entry.journal_id.type == 'general':
            #entry.move_ids = mvoes
            #entry.invoice_count = len(invoices)
    
    @api.depends('custom_entry_line.invoice_lines.move_id')
    def _compute_all_moves(self):
        Move = self.env['account.move']
        can_read = Move.check_access_rights('read', raise_exception=False)
        for move in self:
            move.invoice_count = can_read and Move.search_count([('custom_entry_id', '=', move.id),('journal_id', '=', move.custom_entry_type_id.journal_id.id)]) or 0
            move.move_count = can_read and Move.search_count([('custom_entry_id', '=', move.id),('journal_id', '=', move.custom_entry_type_id.journal_id.id),('journal_id.type', '=', 'general') ]) or 0

    @api.depends('custom_entry_line.invoice_lines')
    def _get_invoiced(self):
        # The invoice_ids are obtained thanks to the invoice lines of the SO
        # lines, and we also search for possible refunds created directly from
        # existing invoices. This is necessary since such a refund is not
        # directly linked to the SO.
        for entry in self:
            invoices = entry.custom_entry_line.invoice_lines.move_id.filtered(lambda r: r.move_type in ('in_invoice', 'in_refund'))
            entry.invoice_ids = invoices
            entry.invoice_count = len(invoices)
            
    @api.depends('custom_entry_line.invoice_lines')
    def _get_moves(self):
        # The invoice_ids are obtained thanks to the invoice lines of the SO
        # lines, and we also search for possible refunds created directly from
        # existing invoices. This is necessary since such a refund is not
        # directly linked to the SO.
        for entry in self:
            moves = entry.custom_entry_line.invoice_lines.move_id.filtered(lambda r: r.move_type in ('entry'))
            entry.move_ids = moves
            entry.move_count = len(moves)
    
    @api.depends('custom_entry_line.invoice_lines')
    def _get_entries(self):
        # The invoice_ids are obtained thanks to the invoice lines of the SO
        # lines, and we also search for possible refunds created directly from
        # existing invoices. This is necessary since such a refund is not
        # directly linked to the SO.
        for entry in self:
            invoices = entry.custom_entry_line.invoice_lines.move_id.filtered(lambda r: r.move_type in ('entry'))
            entry.invoice_ids = invoices
            entry.invoice_count = len(invoices)
            
            
    def write1(self, values): #its temporarily commented for testing
        for order in self.sudo():
            group_id = order.stage_id.group_id
            if not order.stage_id.allow_editing:
                if group_id:
                    if not (group_id & self.env.user.groups_id):
                        raise UserError(_("You are not authorize to edit record at '%s'.", order.stage_id.name))
                    
        result = super(CustomEntry, self).write(values)
        return result
    
    def unlink(self):
        for entry in self:
            if not entry.stage_category == 'draft' or entry.invoice_ids:
                raise UserError(_('You cannot delete an entry which has been posted.'))
           
        return super(CustomEntry, self).unlink()
   
    @api.depends('custom_entry_line.price_subtotal','custom_entry_line.advance_subtotal')
    def _amount_all(self):
        for entry in self:
            adv = tot = 0
            for line in entry.custom_entry_line:
                tot += line.price_subtotal
                adv += line.advance_subtotal
            entry.amount_advanced_total = adv
            entry.amount_total = tot
            entry.amount_balance = tot - adv
        
    def button_draft(self):
        self.write({'stage_id': self.next_stage_id.id})
    
    def button_submit(self):
        #self.ensure_one()
        for order in self.sudo():
            group_id = order.custom_entry_type_id.group_id
            if group_id:
                if not (group_id & self.env.user.groups_id):
                    raise UserError(_("You are not authorize to submit requisition in category '%s'.", order.custom_entry_type_id.name))
            if not order.custom_entry_line:
                raise UserError(_("You cannot submit transaction '%s' because there is no line.", self.name))
           
        self.update({
            'date_submit' : fields.Datetime.now(),
            'stage_id' : self.stage_id.next_stage_id.id,
        })
        
    def button_confirm(self):
        for order in self.sudo():
            group_id = order.stage_id.group_id
            if group_id:
                if not (group_id & self.env.user.groups_id):
                    raise UserError(_("You are not authorize to approve '%s'.", order.stage_id.name))
                    
        self.update({
            'date_approved' : fields.Datetime.now(),
            'stage_id' : self.stage_id.next_stage_id.id,
        })
        
    def button_done(self):
        for order in self.sudo():
            group_id = order.stage_id.group_id
            if group_id:
                if not (group_id & self.env.user.groups_id):
                    raise UserError(_("You are not authorize to close '%s'.", order.stage_id.name))
                    
        self.update({
            'stage_id' : self.stage_id.next_stage_id.id,
        })
        
    def button_refuse(self):
        for order in self.sudo():
            group_id = order.stage_id.group_id
            if group_id:
                if not (group_id & self.env.user.groups_id):
                    raise UserError(_("You are not authorize to refuse '%s'.", order.stage_id.name))
        if self.stage_id.prv_stage_id:
            self.update({
                'stage_id' : self.stage_id.prv_stage_id.id,
            })

    def button_cancel(self):
        for order in self:
            for inv in order.invoice_ids:
                if inv and inv.state not in ('cancel', 'draft'):
                    raise UserError(_("Unable to cancel this purchase order. You must first cancel the related vendor bills."))

        stage_id = self.env['account.custom.entry.stage'].search([('custom_entry_type_ids','=',self.custom_entry_type_id.id)],limit=1)
        self.update({
            'stage_id': stage_id.id,
        })
      
    def _prepare_invoice(self):
        """Prepare the dict of values to create the new invoice for a purchase order.
        """
        self.ensure_one()
        #move_type = self._context.get('default_move_type', 'in_invoice')
        move_type = 'in_invoice'
        journal = self.custom_entry_type_id.journal_id.id
        if not journal:
            raise UserError(_('Please define an accounting purchase journal for the company %s (%s).') % (self.company_id.name, self.company_id.id))

        partner_invoice_id = self.partner_id.address_get(['invoice'])['invoice']
        invoice_vals = {
            'ref': self.name,
            'move_type': self.custom_entry_type_id.move_type,
            'journal_id': journal,
            #'narration': self.notes,
            'invoice_date': fields.Datetime.now(),
            'currency_id': self.currency_id.id,
            'invoice_user_id': self.user_id and self.user_id.id,
            'partner_id': self.partner_id.id,
            #'fiscal_position_id': (self.fiscal_position_id or self.fiscal_position_id.get_fiscal_position(partner_invoice_id)).id,
            #'payment_reference': self.partner_ref or '',
            'partner_bank_id': self.partner_id.bank_ids[:1].id,
            'invoice_origin': self.name,
            'invoice_payment_term_id': self.partner_id.property_supplier_payment_term_id.id,
            'invoice_line_ids': [],
            'company_id': self.company_id.id,
        }
        return invoice_vals
    
    def action_view_invoice(self):
        invoices = self.mapped('invoice_ids')
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
    
    def action_view_move(self):
        #invoices = self.mapped('invoice_ids')
        #invoices = self.env['account.move'].search([('custom_entry_id','=',self.id),('move_type','=','entry')])
        invoices = self.custom_entry_line.invoice_lines.move_id.filtered(lambda r: r.move_type in ('entry'))
        action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_journal_line")
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
            'default_move_type': 'entry',
        }
        return action
    
    
    def action_view_invoice1(self, invoices=False):
        """This function returns an action that display existing vendor bills of
        given purchase order ids. When only one found, show the vendor bill
        immediately.
        """
        if not invoices:
            # Invoice_ids may be filtered depending on the user. To ensure we get all
            # invoices related to the purchase order, we read them in sudo to fill the
            # cache.
            self.sudo()._read(['invoice_ids'])
            invoices = self.invoice_ids

        result = self.env['ir.actions.act_window']._for_xml_id('account.action_move_in_invoice_type')
        # choose the view_mode accordingly
        if len(invoices) > 1:
            result['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            res = self.env.ref('account.view_move_form', False)
            form_view = [(res and res.id or False, 'form')]
            if 'views' in result:
                result['views'] = form_view + [(state, view) for state, view in result['views'] if view != 'form']
            else:
                result['views'] = form_view
            result['res_id'] = invoices.id
        else:
            result = {'type': 'ir.actions.act_window_close'}

        return result
    
    def create_advance_expense(self):
        res = self._create_bill()
        #return self.action_subscription_invoice()
    
    def create_journal_entry(self):
        res = self._create_account_move()
        #for order in self.sudo():
        #    group_id = order.stage_id.group_id
        #    if group_id:
        #        if not (group_id & self.env.user.groups_id):
        #            raise UserError(_("You are not authorize to create Journal Entry '%s'.", order.stage_id.name))
        
        #self.update({
            #'stage_id' : self.stage_id.next_stage_id.id,
        #})
    def _create_account_move(self):
        move = self.env['account.move']
        company = self.company_id
        lines_data = []
        debit = credit = amount = balance = 0
        counter_debit = counter_credit = counter_amount = counter_balance = 0
        supplier_qty = 0
        
        suppliers = self.env['account.custom.entry.line'].read_group([('custom_entry_id', '=', self.id)], ['supplier_id'], ['supplier_id'])

        if self.custom_entry_type_id.entry_reverse:
            for supplier in suppliers:
                supplier_qty = 0
                counter_debit = counter_credit = counter_amount = counter_balance = 0
                for line in self.custom_entry_line.filtered(lambda x: x.supplier_id.id == supplier['supplier_id'][0]):
                    debit = credit = amount = balance = 0
                    if self.custom_entry_type_id.counterpart_mode == 'debit':
                        amount = line.price_subtotal
                        counter_amount += line.price_subtotal * -1
                    else:
                        amount = line.price_subtotal * -1
                        counter_amount += line.price_subtotal
                    supplier_qty += line.product_qty
                    
                    balance = line.currency_id._convert(amount, company.currency_id, company, self.date_entry or fields.Date.context_today(line))
                    debit = balance if balance > 0.0 else 0.0
                    credit = -balance if balance < 0.0 else 0.0
                
                    counter_balance = line.currency_id._convert(counter_amount, company.currency_id, company, self.date_entry or fields.Date.context_today(line))
                    counter_debit = counter_balance if counter_balance > 0.0 else 0.0
                    counter_credit = -counter_balance if counter_balance < 0.0 else 0.0
            
                    lines_data.append([0,0,{
                        'name': str(self.name) + ' ' ,
                        'custom_entry_line_id': line.id,
                        'account_id': self.custom_entry_type_id.account_id.id,
                        'amount_currency': amount,
                        'currency_id': self.currency_id.id,
                        'debit': debit,
                        'credit': credit,
                        'partner_id': self.partner_id.id,
                        'quantity': line.product_qty,
                        'product_uom_id': line.product_uom_id.id,
                        'product_id': line.product_id.id,
                        #'analytic_account_id': line.analytic_account_id.id,
                        #'analytic_tag_ids': [(6, 0, line.analytic_tag_ids.ids)],
                        'project_id': line.project_id.id,
                    }])
            
                lines_data.append([0,0,{
                    'name': str(self.name) + ' ' ,
                    #'custom_entry_line_id': line.id,
                    'account_id': self.custom_entry_type_id.counterpart_account_id.id,
                    'amount_currency': counter_amount,
                    'currency_id': self.currency_id.id,
                    'debit': counter_debit,
                    'credit': counter_credit,
                    'partner_id': supplier['supplier_id'][0],
                    'quantity': supplier_qty,
                    #'analytic_account_id': line.analytic_account_id.id,
                    #'analytic_tag_ids': [(6, 0, line.analytic_tag_ids.ids)],
                    #'project_id': line.project_id.id,
                }])
            move.create({
                'move_type': self.custom_entry_type_id.move_type,
                'custom_entry_id': self.id,
                'ref':  str(self.name), 
                'date': fields.Datetime.now(),
                'currency_id': self.currency_id.id,
                'journal_id': self.custom_entry_type_id.journal_id.id,
                'narration': self.name,
                'line_ids':lines_data,
            })
        else:
            debit = credit = amount = balance = 0
            counter_debit = counter_credit = counter_amount = counter_balance = 0
            counter_quantity = 0
            for line in self.custom_entry_line:
                counter_quantity += line.product_qty
                if self.custom_entry_type_id.counterpart_mode == 'debit':
                    amount = line.price_subtotal * -1
                    #ounter_amount += line.price_subtotal
                else:
                    amount = line.price_subtotal
                    #ounter_amount += line.price_subtotal * -1    
                
                balance = line.currency_id._convert(amount, company.currency_id, company, self.date_entry or fields.Date.context_today(line))
                debit = balance if balance > 0.0 else 0.0
                credit = -balance if balance < 0.0 else 0.0
                
                lines_data.append([0,0,{
                    'name': str(self.name) + ' ' + str(line.product_id.name),
                    'custom_entry_line_id': line.id,
                    'account_id': self.custom_entry_type_id.account_id.id,
                    'amount_currency': amount,
                    'currency_id': self.currency_id.id,
                    'debit': debit,
                    'credit': credit,
                    'quantity': line.product_qty,
                    'product_uom_id': line.product_uom_id.id,
                    'product_id': line.product_id.id,
                    'partner_id': line.supplier_id.id,
                    'analytic_account_id': line.analytic_account_id.id,
                    'analytic_tag_ids': [(6, 0, line.analytic_tag_ids.ids)],
                    'project_id': line.project_id.id,
                }])
            if self.custom_entry_type_id.counterpart_mode == 'debit':
                counter_debit = self.amount_total
                counter_amount = self.amount_total
            else:
                counter_credit = self.amount_total
                counter_amount = self.amount_total * -1
            counter_balance = line.currency_id._convert(counter_amount, company.currency_id, company, self.date_entry or fields.Date.context_today(line))
            counter_debit = counter_balance if counter_balance > 0.0 else 0.0
            counter_credit = -counter_balance if counter_balance < 0.0 else 0.0
            
            lines_data.append([0,0,{
                'name': str(self.name),
                'custom_entry_line_id': line.id,
                'quantity': counter_quantity,
                'account_id': self.custom_entry_type_id.counterpart_account_id.id,
                'debit': counter_debit,
                'credit': counter_credit,
                'amount_currency': counter_amount,
                'currency_id': self.currency_id.id,
                'partner_id': self.partner_id.id,
            }])
            move.create({
                'move_type': self.custom_entry_type_id.move_type,
                'custom_entry_id': self.id,
                'ref':  str(self.name), 
                'date': fields.Datetime.now(),
                'currency_id': self.currency_id.id,
                'journal_id': self.custom_entry_type_id.journal_id.id,
                'narration': self.name,
                'line_ids':lines_data,
            })
        return move
    
        
    def create_bill(self):
        for order in self.sudo():
            group_id = order.stage_id.group_id
            if group_id:
                if not (group_id & self.env.user.groups_id):
                    raise UserError(_("You are not authorize to create bill '%s'.", order.stage_id.name))
        res = self._create_bill()
        self.update({
            'stage_id' : self.stage_id.next_stage_id.id,
        })
        #return self.action_subscription_invoice()
    
    def _create_bill(self):
        invoice = self.env['account.move']
        lines_data = []
        for line in self.custom_entry_line:
            lines_data.append([0,0,{
                'name': str(self.name) + ' ' + str(line.product_id.name),
                'custom_entry_line_id': line.id,
                'price_unit': line.price_unit or 0.0,
                #'discount': line.discount,
                'quantity': line.product_qty,
                'product_uom_id': line.product_uom_id.id,
                'product_id': line.product_id.id,
                'tax_ids': [(6, 0, line.product_id.supplier_taxes_id.ids)],
                'analytic_account_id': line.analytic_account_id.id,
                'analytic_tag_ids': [(6, 0, line.analytic_tag_ids.ids)],
                'project_id': line.project_id.id,
            }])
        invoice.create({
            'move_type': self.custom_entry_type_id.move_type,
            'custom_entry_id': self.id,
            'invoice_date': fields.Datetime.now(),
            'partner_id': self.partner_id.id,
            #'partner_shipping_id': self.partner_id.id,
            'currency_id': self.currency_id.id,
            'journal_id': self.custom_entry_type_id.journal_id.id,
            'invoice_origin': self.name,
            #'fiscal_position_id': fpos.id,
            'invoice_payment_term_id': self.partner_id.property_supplier_payment_term_id.id,
            'narration': self.name,
            'invoice_user_id': self.user_id.id,
            #'partner_bank_id': company.partner_id.bank_ids.filtered(lambda b: not b.company_id or b.company_id == company)[:1].id,
            'invoice_line_ids':lines_data,
        })
        return invoice
    
    def get_payment_count(self):
        for entry in self:
            count = self.env['account.payment'].search_count([('custom_entry_id', '=', entry.id)])
            entry.payment_count = count
        
    payment_count = fields.Integer(string='Payments', compute='get_payment_count')
    
    def action_view_payment(self):
        self.ensure_one()
        return {
         'type': 'ir.actions.act_window',
         'binding_type': 'object',
         'domain': [('custom_entry_id', '=', self.id)],
         'multi': False,
         'name': 'Payment',
         'target': 'current',
         'res_model': 'account.payment',
         'view_mode': 'tree,form',
        }
    
    def create_payment(self):
        for order in self.sudo():
            group_id = order.stage_id.group_id
            if group_id:
                if not (group_id & self.env.user.groups_id):
                    raise UserError(_("You are not authorize to create payment '%s'.", order.stage_id.name))
        vals = {
            'payment_type': 'outbound',
            'journal_id': self.custom_entry_type_id.payment_journal_id.id,
            'partner_type': 'supplier',
            'custom_entry_id': self.id,
            'partner_id': self.partner_id.id,
            'currency_id': self.currency_id.id,
            'date': self.date_entry,
            'amount': self.amount_advanced_total,
        }
        payment = self.env['account.payment'].create(vals)
        self.update({
            'stage_id' : self.stage_id.next_stage_id.id,
        })
        
    
   
    """
    def create_forcast_invoice(self):
        line_ids = []
        debit_sum = 0.0
        credit_sum = 0.0
        move_dict = {
#               'name': self.name,
              'journal_id': self.custom_entry_type_id.journal_id.id,
              'date': self.date_entry,
              'invoice_date': self.date_entry,
              'custom_entry_id': self.id,
              'partner_id': self.partner_id.id if self.partner_id.id else False,
              'move_type': 'in_invoice',
              'state': 'draft',
                   }
                        #step2:debit side entry
        debit_line = (0, 0, {
                'name': self.name +":"+ 'Forcast Advances',
                'debit': abs(self.amount_forecast),
                'credit': 0.0,
                'account_id': self.partner_id.property_account_payable_id.id,
                         })
        line_ids.append(debit_line)
        debit_sum += debit_line[2]['debit'] - debit_line[2]['credit']

                #step3:credit side entry
        credit_line = (0, 0, {
                  'name': self.name,
                  'debit': 0.0,
                  'credit': abs(self.amount_forecast),
                  'account_id': self.custom_entry_type_id.journal_id.default_account_id.id,
                          })
        line_ids.append(credit_line)
        credit_sum += credit_line[2]['credit'] - credit_line[2]['debit']

        move_dict['line_ids'] = line_ids
        move = self.env['account.move'].create(move_dict)
        lineid = 0
        for custom_line in self.custom_entry_line:
            lineid = custom_line.id    
        for line in move.invoice_line_ids:
            line.update({
                'custom_entry_line_id': lineid
            })
    
    def create_difference_invoice(self):
        line_ids = []
        debit_sum = 0.0
        credit_sum = 0.0
        move_dict = {
#               'name': self.name,
              'journal_id': self.custom_entry_type_id.journal_id.id,
              'date': self.date_entry,
              'invoice_date': self.date_entry,
              'custom_entry_id': self.id,
              'partner_id': self.partner_id.id if self.partner_id.id else False,
              'move_type': 'in_invoice',
              'state': 'draft',
                   }
                        #step2:debit side entry
        debit_line = (0, 0, {
                'name': self.name +":",
                'debit': abs(self.amount_difference),
                'credit': 0.0,
                'account_id': self.partner_id.property_account_payable_id.id,
                         })
        line_ids.append(debit_line)
        debit_sum += debit_line[2]['debit'] - debit_line[2]['credit']

                #step3:credit side entry
        credit_line = (0, 0, {
                  'name': self.name,
                  'debit': 0.0,
                  'credit': abs(self.amount_difference),
                  'account_id': self.custom_entry_type_id.journal_id.default_account_id.id,
                          })
        line_ids.append(credit_line)
        credit_sum += credit_line[2]['credit'] - credit_line[2]['debit']

        move_dict['line_ids'] = line_ids
        move = self.env['account.move'].create(move_dict)
        lineid = 0
        for custom_line in self.custom_entry_line:
            lineid = custom_line.id    
        for line in move.invoice_line_ids:
            line.update({
                'custom_entry_line_id': lineid
            })
        """
    
class CustomEntryLine(models.Model):
    _name = 'account.custom.entry.line'
    _description = 'Custom Entry Line'
    
    custom_entry_id = fields.Many2one('account.custom.entry', string='Custom Entry', required=True, ondelete='cascade', index=True, copy=False)
    note = fields.Char(string='Description')
    stage_category = fields.Selection(related='custom_entry_id.stage_category', readonly=True)
    date_entry = fields.Datetime(related='custom_entry_id.date_entry')
    date_entry_period = fields.Char(string='Month')
    
    company_id = fields.Many2one('res.company', related='custom_entry_id.company_id')
    currency_id = fields.Many2one('res.currency',related='custom_entry_id.currency_id')

    invoice_lines = fields.One2many('account.move.line', 'custom_entry_line_id', string="Bill Lines", readonly=True, copy=False)

    #Project   
    project_id = fields.Many2one('project.project', string="Project", check_company=True, ondelete='cascade')
    state_id = fields.Many2one('res.country.state', compute='_compute_state', string='Region', ondelete='cascade')
    analytic_account_id = fields.Many2one('account.analytic.account', store=True, string='Analytic Account',ondelete='cascade')
    analytic_tag_ids = fields.Many2many('account.analytic.tag', store=True, string='Analytic Tags', ondelete='cascade')
    
    #employee
    employee_id = fields.Many2one('hr.employee',string="Employee")
    supplier_id = fields.Many2one('res.partner',string="Supplier")
    
    #Product
    product_id = fields.Many2one('product.product', string="Products", check_company=True)
    product_uom_id = fields.Many2one('uom.uom', string="Unit of Measure",
        domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id', string="UOM Category")
    product_qty = fields.Float(string='Quantity', default=1.0, digits='Product Unit of Measure', )
    price_unit = fields.Float(string='Unit Price', default=0.0, digits='Product Price')
    taxes_id = fields.Many2many('account.tax', string='Taxes', compute='_compute_tax_id', domain=['|', ('active', '=', False), ('active', '=', True)])
    price_subtotal = fields.Monetary(compute='_compute_all_amount', string='Subtotal', store=True)
    advance_subtotal = fields.Monetary(string='Adv. Subtotal', store=True)
    
    def _compute_tax_id(self):
        for line in self:
            line = line.with_company(line.company_id)
            #fpos = line.order_id.fiscal_position_id or line.order_id.fiscal_position_id.get_fiscal_position(line.order_id.partner_id.id)
            # filter taxes by company
            taxes = line.product_id.supplier_taxes_id.filtered(lambda r: r.company_id == line.env.company)
            #line.taxes_id = fpos.map_tax(taxes, line.product_id, line.custom_entry_id.partner_id)
            line.taxes_id = taxes.ids
            
    @api.depends('product_qty', 'price_unit')
    def _compute_all_amount(self):
        tot = 0
        for line in self:
            line.price_subtotal = line.product_qty * line.price_unit
            #self.update({
             #   'price_subtotal': 100
            #})
        
    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.product_uom_id = self.product_id.uom_id.id
            self.taxes_id = self.product_id.supplier_taxes_id.ids
        
            
    
                
        
    def _compute_state(self):
        for line in self:
            line.state_id = line.project_id.address_id.state_id.id
    
    def _prepare_account_move_line(self, move=False):
        self.ensure_one()
        taxes_id = self.product_id.supplier_taxes_id
        res = {
            'name': '%s: ' % (self.custom_entry_id.name),
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom_id.id,
            'quantity': self.product_qty,
            'price_unit': self.price_unit,
            #'tax_ids': [(6, 0, self.taxes_id.ids)],
            #'tax_ids': [(6, 0, taxes_id.ids)],
            'analytic_account_id': self.analytic_account_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'custom_entry_line_id': self.id,
            'project_id': self.project_id.id,
        }
        if not move:
            return res

        if self.currency_id == move.company_id.currency_id:
            currency = False
        else:
            currency = move.currency_id

        res.update({
            'move_id': move.id,
            'currency_id': currency and currency.id or False,
            'date_maturity': move.invoice_date_due,
            'partner_id': move.partner_id.id,
        })
        return res