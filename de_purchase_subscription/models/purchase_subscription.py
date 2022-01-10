# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
import datetime
import traceback

from ast import literal_eval
from collections import Counter
from dateutil.relativedelta import relativedelta
from uuid import uuid4

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression
from odoo.tools import format_date, float_compare
from odoo.tools.float_utils import float_is_zero


_logger = logging.getLogger(__name__)

INTERVAL_FACTOR = {
    'daily': 30.0,
    'weekly': 30.0 / 7.0,
    'monthly': 1.0,
    'yearly': 1.0 / 12.0,
}

PERIODS = {'daily': 'days', 'weekly': 'weeks', 'monthly': 'months', 'yearly': 'years'}

class PurchaseSubscription(models.Model):
    _name = 'purchase.subscription'
    _description = 'Purchase Subscription'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _check_company_auto = True
    _mail_post_access = 'read'
    _order = 'subscription_date desc, id desc'
    
    
    def _get_default_pricelist(self):
        return self.env['product.pricelist'].search([('currency_id', '=', self.env.company.currency_id.id)], limit=1).id

   
    
    def _get_default_stage_id(self):
        return self.env['purchase.subscription.stage'].search([], order='sequence', limit=1)
    
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        return stages.sudo().search([], order=order)
    
    
    name = fields.Char(tracking=True,)
    code = fields.Char(string="Reference", )
    #stage_id = fields.Many2one('purchase.subscription.stage', string='Stage', index=True, default=lambda s: s._get_default_stage_id(), copy=False, tracking=True)
    stage_id = fields.Many2one('purchase.subscription.stage', string='Stage', compute='_compute_stage_id',
        store=True, readonly=False, ondelete='restrict', tracking=True, index=True,
        default=_get_default_stage_id, group_expand='_read_group_stage_ids',
        domain="[('subscription_type_ids', '=', subscription_type_id)]", copy=False)
    stage_category = fields.Selection(related='stage_id.stage_category')

    
    company_id = fields.Many2one('res.company', string="Company", default=lambda s: s.env.company, required=True, )
    partner_id = fields.Many2one('res.partner', string='Vendor', required=True, auto_join=True, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    partner_invoice_id = fields.Many2one(
        'res.partner', string='Invoice Address',
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",)
    partner_shipping_id = fields.Many2one(
        'res.partner', string='Service Address',
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", )
    subscription_date = fields.Date(string='Subscription Date', default=fields.Date.today)
    date_start = fields.Date(string='Start Date', default=fields.Date.today)
    date = fields.Date(string='End Date', tracking=True, help="If set in advance, the subscription will be set to renew 1 month before the date and will be closed on the date set in this field.")
    automated_sequence = fields.Boolean(related="subscription_type_id.automated_sequence")
    
    recurring_next_date = fields.Date(string='Date of Next Invoice', default=fields.Date.today, help="The next invoice will be created on this date then the period will be extended.")
    recurring_invoice_day = fields.Integer('Recurring Invoice Day', copy=False, default=lambda e: fields.Date.today().day)
    recurring_interval_rule = fields.Selection(related='subscription_plan_id.recurring_interval_rule', )
    recurring_interval_type = fields.Selection(related='subscription_plan_id.recurring_interval_type', )
    recurring_interval = fields.Integer(related='subscription_plan_id.recurring_interval')
    recurring_interval_count = fields.Integer(related='subscription_plan_id.recurring_interval_count')
    invoicing_mode = fields.Selection(related='subscription_plan_id.invoicing_mode')
    
    
    currency_id = fields.Many2one('res.currency', 'Currency', required=True, default=lambda self: self.env.company.currency_id.id)
        
    subscription_plan_id = fields.Many2one('purchase.subscription.plan', string='Subscription Plan',
                                           domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", required=True, help="The subscription plan defines the invoice policy and the payment terms.", tracking=True, check_company=True)
    subscription_type_id = fields.Many2one('purchase.subscription.type', string='Subscription Type',
                                           required=True, help="The subscription type categories agreement.",)
    description = fields.Text()
    user_id = fields.Many2one('res.users', string='Purchase Representative', tracking=True, default=lambda self: self.env.user)
    purchase_subscription_line = fields.One2many('purchase.subscription.line', 'purchase_subscription_id', string='Subscription Lines', copy=True)
    subscription_log_ids = fields.One2many('purchase.subscription.log', 'subscription_id', string='Subscription Logs', readonly=True)
    subscription_invoice_ids = fields.One2many('account.move','purchase_subscription_id', string='Subscription', readonly=True)
    subscription_invoice_count = fields.Integer(compute='_compute_invoice_count')
    billing_cycle = fields.Integer(compute='_compute_billing_cycle',store=True, readonly=False, string="Billing Cycle")
    
    recurring_price = fields.Float(compute='_amount_all', string="Recurring Price", store=True, tracking=40)
    recurring_total = fields.Float(compute='_amount_all', string="Recurring Total", store=True, tracking=40)
    # add tax calculation
    recurring_tax = fields.Float('Taxes', compute="_amount_all", compute_sudo=True, store=True)
    recurring_total_incl = fields.Float('Total', compute="_amount_all", compute_sudo=True, store=True, tracking=50)
    
    recurring_billed_total = fields.Float(compute='_amount_billed_all', string="Total Billed")
    recurring_paid_total = fields.Float(compute='_amount_billed_all', string="Total Paid")
    billable_amount = fields.Float(compute='_amount_billed_all', string="Billable Amount")


    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account',
                                          domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", check_company=True)
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags')

    
    payment_term_id = fields.Many2one('account.payment.term', string='Default Payment Terms', check_company=True, tracking=True, help="These payment terms will be used when generating new invoices and renewal/upsell orders. Note that invoices paid using online payment will use 'Already paid' regardless of this setting.")
    
    date_submit = fields.Datetime('Submission Date', readonly=False)
    date_approved = fields.Datetime('Approved Date', readonly=False)
            
    @api.depends('subscription_type_id')
    def _compute_stage_id(self):
        for subscription in self:
            if subscription.subscription_type_id:
                if subscription.subscription_type_id not in subscription.stage_id.subscription_type_ids:
                    subscription.stage_id = subscription.stage_find(subscription.subscription_type_id.id, [
                        ('fold', '=', False), ('stage_category', '=', 'closed')])
            else:
                subscription.stage_id = False
    
    def stage_find(self, section_id, domain=[], order='sequence'):
        section_ids = []
        if section_id:
            section_ids.append(section_id)
        section_ids.extend(self.mapped('subscription_type_id').ids)
        search_domain = []
        if section_ids:
            search_domain = [('|')] * (len(section_ids) - 1)
            for section_id in section_ids:
                search_domain.append(('subscription_type_ids', '=', section_id))
        search_domain += list(domain)
        # perform search, return the first found
        return self.env['purchase.subscription.stage'].search(search_domain, order=order, limit=1).id
    
    def _compute_billing_cycle(self):
        billing_cycle = 0
        for subscription in self:
            if subscription.subscription_plan_id:
                billing_cycle = subscription.subscription_plan_id.recurring_interval
            subscription.billing_cycle = billing_cycle
        if self.billing_cycle == 0:
            self.billing_cycle = 1
                
        
    @api.depends('subscription_invoice_ids')
    def _amount_billed_all(self):
        billed_amount = paid_amount = 0.0
        for subscription in self:
            for invoice in subscription.subscription_invoice_ids:
                billed_amount += invoice.amount_total
                paid_amount += (invoice.amount_total - invoice.amount_residual)
            self.update({
                'recurring_billed_total': billed_amount,
                'recurring_paid_total': paid_amount,
                'billable_amount': subscription.recurring_total - billed_amount
            })
        
    @api.depends('purchase_subscription_line.price_subtotal')
    def _amount_all(self):
        """
        Compute the total amounts of the subscription.
        """
        for subscription in self:
            amount_tax = 0.0
            recurring_total = 0.0
            recurring_price = 0.0
            for line in subscription.purchase_subscription_line:
                recurring_price += line.price_subtotal
                # _amount_line_tax needs singleton
                amount_tax += line._amount_line_tax()
            recurring_tax = subscription.currency_id and subscription.currency_id.round(amount_tax) or 0.0
            recurring_total = recurring_price * (subscription.recurring_interval or 1.0)
            subscription.update({
                'recurring_price': recurring_price,
                'recurring_total': recurring_total,
                'recurring_tax': recurring_tax,
                'recurring_total_incl': recurring_tax + recurring_total,
            })
    
    
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.partner_id:
            self.payment_term_id = self.partner_id.with_company(self.company_id).property_payment_term_id.id
            #addresses = self.partner_id.address_get(['delivery', 'invoice'])
            #self.partner_shipping_id = addresses['delivery']
            #self.partner_invoice_id = addresses['invoice']
        if self.partner_id.user_id:
            self.user_id = self.partner_id.user_id
            

    @api.onchange('date_start', 'subscription_plan_id')
    def onchange_date_start(self):
        if self.date_start and self.recurring_interval_rule == 'limited':
            self.date = fields.Date.from_string(self.date_start) + relativedelta(**{
                PERIODS[self.recurring_interval_type]: self.subscription_plan_id.recurring_interval_count * self.subscription_plan_id.recurring_interval})
            
    @api.onchange('recurring_next_date')
    def onchange_recurring_next_date(self):
        if self.recurring_next_date:
            recurring_next_date = self.recurring_next_date
            self.recurring_invoice_day = recurring_next_date.day
    
    def button_submit(self):
        #self.ensure_one()
        for order in self.sudo():
            group_id = order.subscription_type_id.group_id
            if group_id:
                if not (group_id & self.env.user.groups_id):
                    raise UserError(_("You are not authorize to submit subscription in category '%s'.", order.subscription_type_id.name))
            if not order.purchase_subscription_line:
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
            
    def start_subscription(self):
        self.ensure_one()
        next_stage_in_progress = self.env['purchase.subscription.stage'].search([('stage_category', '=', 'progress'), ('sequence', '>=', self.stage_id.sequence)], limit=1)
        if not next_stage_in_progress:
            next_stage_in_progress = self.env['purchase.subscription.stage'].search([('stage_category', '=', 'progress')], limit=1)
        self.stage_id = next_stage_in_progress
        return True
            
    @api.model
    def create(self, vals):
        #vals['code'] = (
        #    vals.get('code') or
        #    self.env.context.get('default_code') or
        #    self.env['ir.sequence'].with_company(vals.get('company_id')).next_by_code('purchase.subscription') or
        #    'New'
        #)
        #if vals.get('name', 'New') == 'New':
         #   vals['name'] = vals['code']
        if not vals.get('recurring_invoice_day'):
            sub_date = vals.get('recurring_next_date') or vals.get('date_start') or fields.Date.context_today(self)
            if isinstance(sub_date, datetime.date):
                vals['recurring_invoice_day'] = sub_date.day
            else:
                vals['recurring_invoice_day'] = fields.Date.from_string(sub_date).day
        subscription = super(PurchaseSubscription, self).create(vals)
       
        if subscription.partner_id:
            subscription.message_subscribe(subscription.partner_id.ids)
        return subscription
   
    def write(self, vals):
        recurring_next_date = vals.get('recurring_next_date')
        if recurring_next_date and not self.env.context.get('skip_update_recurring_invoice_day'):
            if isinstance(recurring_next_date, datetime.date):
                vals['recurring_invoice_day'] = recurring_next_date.day
            else:
                vals['recurring_invoice_day'] = fields.Date.from_string(recurring_next_date).day
        if vals.get('partner_id'):
            self.message_subscribe([vals['partner_id']])
        result = super(PurchaseSubscription, self).write(vals)
        return result
    
    def generate_recurring_invoice(self):
        res = self._recurring_create_invoice()
        return self.action_subscription_invoice()
       
        
        
    def _recurring_create_invoice(self):
        for subscription in self:
            current_date = subscription.recurring_next_date or self.default_get(['recurring_next_date'])['recurring_next_date']
            new_date = subscription._get_recurring_next_date(subscription.recurring_interval_type, subscription.recurring_interval * subscription.billing_cycle, current_date, subscription.recurring_invoice_day)
            new_values = {'recurring_next_date': new_date}
            if subscription.date:
                new_values['date'] = subscription.date + relativedelta(**{
                    PERIODS[subscription.recurring_interval_type]:
                        subscription.subscription_plan_id.recurring_interval_count * subscription.subscription_plan_id.recurring_interval
                })
            subscription.write(new_values)
        
        next_date = self.recurring_next_date
        if not next_date:
            raise UserError(_('Please define Date of Next Invoice of "%s".') % (self.display_name,))
        recurring_next_date = self._get_recurring_next_date(self.recurring_interval_type, self.recurring_interval * self.billing_cycle, next_date, self.recurring_invoice_day)
        end_date = fields.Date.from_string(recurring_next_date) - relativedelta(days=1)
        
        invoice = self.env['account.move']
        lines_data = []
        for line in self.purchase_subscription_line:
            lines_data.append([0,0,{
                'name': line.name,
                'purchase_subscription_id': line.purchase_subscription_id.id,
                'price_unit': line.price_unit or 0.0,
                'discount': line.discount,
                'quantity': line.quantity * (self.billing_cycle if self.billing_cycle > 0 else 1.0),
                'product_uom_id': line.uom_id.id,
                'product_id': line.product_id.id,
                #'tax_ids': [(6, 0, tax_ids.ids)],
                'analytic_account_id': line.analytic_account_id.id,
                'analytic_tag_ids': [(6, 0, line.analytic_tag_ids.ids)],
                'subscription_start_date': current_date,
                'subscription_end_date': next_date,
            }])
        invoice.create({
            'move_type': 'in_invoice',
            'purchase_subscription_id': self.id,
            'invoice_date': current_date,
            'partner_id': self.partner_id.id,
            'partner_shipping_id': self.partner_id.id,
            'journal_id': self.subscription_plan_id.journal_id.id,
            'invoice_origin': self.code,
            #'fiscal_position_id': fpos.id,
            'invoice_payment_term_id': self.payment_term_id.id,
            'narration': 'test entry',
            'invoice_user_id': self.user_id.id,
            #'partner_bank_id': company.partner_id.bank_ids.filtered(lambda b: not b.company_id or b.company_id == company)[:1].id,
            'invoice_line_ids':lines_data,
        })
        return invoice
    
    @api.model
    def _get_recurring_next_date(self, interval_type, interval, current_date, recurring_invoice_day):
        """
        This method is used for calculating next invoice date for a subscription
        :params interval_type: type of interval i.e. yearly, monthly, weekly etc.
        :params interval: number of interval i.e. 2 week, 1 month, 6 month, 1 year etc.
        :params current_date: date from which next invoice date is to be calculated
        :params recurring_invoice_day: day on which next invoice is to be generated in future
        :returns: date on which invoice will be generated
        """
        interval_type = PERIODS[interval_type]
        recurring_next_date = fields.Date.from_string(current_date) + relativedelta(**{interval_type: interval})
        if interval_type == 'months':
            last_day_of_month = recurring_next_date + relativedelta(day=31)
            if last_day_of_month.day >= recurring_invoice_day:
                # In cases where the next month does not have same day as of previous recurrent invoice date, we set the last date of next month
                # Example: current_date is 31st January then next date will be 28/29th February
                return recurring_next_date.replace(day=recurring_invoice_day)
            # In cases where the subscription was created on the last day of a particular month then it should stick to last day for all recurrent monthly invoices
            # Example: 31st January, 28th February, 31st March, 30 April and so on.
            return last_day_of_month
        # Return the next day after adding interval
        return recurring_next_date
    
    def action_subscription_invoice(self):
        self.ensure_one()
        invoices = self.env['account.move'].search([('invoice_line_ids.purchase_subscription_id', 'in', self.ids)])
        action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_out_invoice_type")
        action["context"] = {
            "create": False,
            "default_move_type": "out_invoice"
        }
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            form_view = [(self.env.ref('account.view_move_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = invoices.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
    
    
    def _compute_invoice_count(self):
        Invoice = self.env['account.move']
        can_read = Invoice.check_access_rights('read', raise_exception=False)
        for subscription in self:
            subscription.subscription_invoice_count = can_read and Invoice.search_count([('invoice_line_ids.purchase_subscription_id', '=', subscription.id)]) or 0
    
    def _message_track(self, tracked_fields, initial):
        """ For a given record, fields to check (tuple column name, column info)
                and initial values, return a structure that is a tuple containing :
                 - a set of updated column names
                 - a list of ORM (0, 0, values) commands to create 'mail.tracking.value' """
        res = super()._message_track(tracked_fields, initial)
        updated_fields, commands = res
        if any(f in updated_fields for f in ['recurring_total', 'template_id']):
            # Intial may not always contains all the needed values if they didn't changed
            # Fallback on record value in that case
            initial_rrule_type = INTERVAL_FACTOR[initial.get('recurring_interval_type', self.recurring_interval_type)]
            initial_rrule_interval = initial.get('recurring_interval', self.recurring_interval)
            old_factor = initial_rrule_type / initial_rrule_interval
            old_value_monthly = initial.get('recurring_total', self.recurring_total) * old_factor
            new_factor = INTERVAL_FACTOR[self.recurring_interval_type] / self.recurring_interval
            new_value_monthly = self.recurring_total * new_factor
            delta = new_value_monthly - old_value_monthly
            cur_round = self.company_id.currency_id.rounding
            if not float_is_zero(delta, precision_rounding=cur_round):
                self.env['purchase.subscription.log'].sudo().create({
                    'event_date': fields.Date.context_today(self),
                    'subscription_id': self.id,
                    'currency_id': self.currency_id.id,
                    'recurring_monthly': new_value_monthly,
                    'amount_signed': delta,
                    'event_type': '1_change',
                    'category': self.stage_id.stage_category,
                    'user_id': self.user_id.id,
                })
        if 'stage_id' in updated_fields:
            old_stage_id = initial['stage_id']
            new_stage_id = self.stage_id
            if new_stage_id.stage_category in ['progress', 'closed'] and old_stage_id.stage_category != new_stage_id.stage_category:
                # subscription started or churned
                start_churn = {'progress': {'type': '0_creation', 'amount_signed': self.recurring_price,
                                            'recurring_monthly': self.recurring_price},
                                'closed': {'type': '2_churn', 'amount_signed': -self.recurring_price,
                                            'recurring_monthly': 0}}
                self.env['purchase.subscription.log'].sudo().create({
                    'event_date': fields.Date.context_today(self),
                    'subscription_id': self.id,
                    'currency_id': self.currency_id.id,
                    'recurring_monthly': start_churn[new_stage_id.stage_category]['recurring_monthly'],
                    'amount_signed': start_churn[new_stage_id.stage_category]['amount_signed'],
                    'event_type': start_churn[new_stage_id.stage_category]['type'],
                    'category': self.stage_id.stage_category,
                    'user_id': self.user_id.id,
                })
        return res
            
class PurchaseSubscriptionLine(models.Model):
    _name = 'purchase.subscription.line'
    _description = "Sale Subscription Line"
    _check_company_auto = True
        
    purchase_subscription_id = fields.Many2one('purchase.subscription', string='Subscription', ondelete='cascade')
    product_id = fields.Many2one(
        'product.product', string='Product', check_company=True, domain="[('purchase_subscription','=',True)]", required=True)
    company_id = fields.Many2one('res.company', related='purchase_subscription_id.company_id', store=True, index=True)
    name = fields.Text(string='Description', required=True)
    quantity = fields.Float(string='Quantity', help="Quantity that will be invoiced.", default=1.0, digits='Product Unit of Measure')
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure', required=True, domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id', readonly=True)
    price_unit = fields.Float(string='Unit Price', required=True, digits='Product Price')
    discount = fields.Float(string='Discount (%)', digits='Discount')
    price_subtotal = fields.Float(compute='_compute_amount', string='Subtotal', digits='Account', store=True)
    currency_id = fields.Many2one('res.currency', 'Currency', related='purchase_subscription_id.currency_id', store=True)
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account',
                                          domain="['|', ('company_id', '=', False), ('company_id', '=', parent.company_id)]", check_company=True)
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags')


    @api.depends('quantity', 'discount', 'price_unit', 'uom_id', 'company_id')
    def _compute_amount(self):
        """
        Compute the amounts of the Subscription line.
        """
        AccountTax = self.env['account.tax']
        for line in self:
            price = AccountTax._fix_tax_included_price_company(line.price_unit, line.product_id.sudo().taxes_id, AccountTax, line.company_id)
            price_subtotal = line.quantity * price * (100.0 - line.discount) / 100.0
            
            line.update({
                'price_subtotal': price_subtotal,
            })
    

    def _amount_line_tax(self):
        self.ensure_one()
        val = 0.0
        product = self.product_id
        product_tmp = product.sudo().product_tmpl_id
        for tax in product_tmp.taxes_id.filtered(lambda t: t.company_id == self.analytic_account_id.company_id):
            fpos_obj = self.env['account.fiscal.position']
            partner = self.analytic_account_id.partner_id
            fpos = fpos_obj.with_company(self.analytic_account_id.company_id).get_fiscal_position(partner.id)
            tax = fpos.map_tax(tax, product, partner)
            compute_vals = tax.compute_all(self.price_unit * (1 - (self.discount or 0.0) / 100.0), self.analytic_account_id.currency_id, self.quantity, product, partner)['taxes']
            if compute_vals:
                val += compute_vals[0].get('amount', 0)
        return val
    
    @api.onchange('product_id')
    def onchange_product_id(self):
        product = self.product_id
        partner = self.analytic_account_id.partner_id
        if partner.lang:
            product = product.with_context(lang=partner.lang)

        self.name = product.get_product_multiline_description_sale()
        self.uom_id = product.uom_id.id
        self.analytic_tag_ids = self.purchase_subscription_id.analytic_tag_ids.ids
        self.analytic_account_id = self.purchase_subscription_id.analytic_account_id.id
    
class PurchaseSubscriptionLog(models.Model):
    _name = 'purchase.subscription.log'
    _description = 'Purchase Log'
    _order = 'event_date desc, id desc'

    subscription_id = fields.Many2one(
        'purchase.subscription', string='Subscription',
        required=True, ondelete='cascade', readonly=True
        )
    create_date = fields.Datetime(string='Date', readonly=True)
    event_type = fields.Selection(
        string='Type of event',
        selection=[('0_creation', 'Creation'), ('1_change', 'Change in MRP'), ('2_churn', 'Churn')],
        required=True, readonly=True,)
    recurring_monthly = fields.Monetary(string='MRP after Change', required=True,
                                        help="MRP, Monthly recurring price after applying the changes of that particular event",
                                        group_operator=None, readonly=True)
    category = fields.Selection([
        ('draft', 'Draft'),
        ('progress', 'In Progress'),
        ('closed', 'Closed')], required=True, default='draft', help="Subscription stage category when the change occured")

    user_id = fields.Many2one('res.users', string='Purchase Representative')
    amount_signed = fields.Monetary(string='Change in MRP', readonly=True, help="Total MRP after change, Monthly recurring price total")
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, readonly=True)
    amount_company_currency = fields.Monetary(
        string='Change in MRR (company currency)', currency_field='company_currency_id',
        compute="_compute_amount_company_currency", store=True,
        readonly=True
    )
    event_date = fields.Date(string='Event Date', required=True)
    company_currency_id = fields.Many2one('res.currency', string='Company Currency', related='company_id.currency_id', store=True, readonly=True)
    company_id = fields.Many2one('res.company', string='Company', related='subscription_id.company_id', store=True, readonly=True)
    percentage = fields.Float(compute='_compute_percentage', string='Variation',
        help="The difference ")


    def _compute_percentage(self):
        for line in self:
            if line.amount_signed != 0.00 or line.recurring_monthly != 0:
                line.percentage = float(line.amount_signed / ((line.recurring_monthly - line.amount_signed) or 0.1))
                #line.percentage = 1
            else:
                line.percentage = 0.00
                
    @api.depends('company_id', 'company_currency_id', 'amount_signed', 'event_date')
    def _compute_amount_company_currency(self):
        for log in self:
            log.amount_company_currency = log.currency_id._convert(
                from_amount=log.amount_signed,
                to_currency=log.company_currency_id,
                date=log.event_date,
                company=log.company_id
            )