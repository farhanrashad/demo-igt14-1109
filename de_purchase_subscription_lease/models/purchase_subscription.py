# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date

class PurchaseSubscriptionType(models.Model):
    _inherit = 'purchase.subscription.type'
    
    allow_lease = fields.Boolean(string='Lease Management')
    
class PurchaseSubscriptionPlan(models.Model):
    _inherit = 'purchase.subscription.plan'
    
    allow_payment_schedule = fields.Boolean(string='Plan Payment Schedule')
    subscription_plan_schedule_ids = fields.One2many('purchase.subscription.plan.schedule', 'subscription_plan_id', string='Payment Schedules', copy=True)
    
    @api.constrains('subscription_plan_schedule_ids','recurring_interval_count')
    def _check_intervals_payment_schedules(self):
        tot = 0
        for schedule in self.subscription_plan_schedule_ids:
            tot += schedule.recurring_interval
        if self.recurring_interval_count != tot:
            raise ValidationError(_("Schedule intervals %s must be equal to total intervals %s",tot,self.recurring_interval_count))


class PurchaseSubscriptionPlanSchedule(models.Model):
    _name = 'purchase.subscription.plan.schedule'
    _description = 'Purchase Subscription Plan Schedule'
    
    subscription_plan_id = fields.Many2one('purchase.subscription.plan', string='Subscription Plan',)
    name = fields.Char(string='Name', compute='_compute_name', store=True,)
    recurring_interval = fields.Integer('Intervals', required=True)
    
class PurchaseSubscription(models.Model):
    _inherit = 'purchase.subscription'    
    
    purchase_subscription_schedule_line = fields.One2many('purchase.subscription.schedule', 'purchase_subscription_id', string='Subscription Schedules', copy=False)
    
    allow_lease = fields.Boolean(related='subscription_type_id.allow_lease')
    
    project_id = fields.Many2one('project.project', string='Project')
    product_id = fields.Many2one('product.product', string='Product')
    lease_hunter_partner_id = fields.Many2one('res.partner', string='Lease Hunter')
    lease_saq_partner_id = fields.Many2one('res.partner', string='SAQ Vendor')
    
    allow_registration = fields.Boolean(string='Allow Registration')
    date_registration = fields.Date(string='Registration Date')
    allow_stamp_duty = fields.Boolean(string='Allow Stamp Duty')
    date_stamp_duty = fields.Date(string='Stamp Duty Date')
    
    candidate = fields.Selection(string='Candidate',
                                 selection=[('c1', 'C1'),('c2', 'C2'),
                                            ('c3', 'C3'),('c4', 'C4'),
                                            ('c5', 'C5'),('c6', 'C6'),
                                            ('c7', 'C7'),('c8', 'C8'),
                                            ('c9', 'C9'),('c10', 'C10'),
                                            ('c11', 'C11'),('c12', 'C12'),
                                            ('c13', 'C13'),('c14', 'C14'),
                                            ('c15', 'C15'),('c16', 'C16'),
                                            ('c17', 'C17'),('c18', 'C18'),
                                            ('c19', 'C19'),('c20', 'C20'),
                                           ],)
    
    allow_payment_schedule = fields.Boolean(related='subscription_plan_id.allow_payment_schedule')
    select_all = fields.Boolean(string='Select All', default=False)
    
    #revision fields
    current_revision_id = fields.Many2one('purchase.subscription','Current revision',readonly=True,copy=True)
    old_revision_ids = fields.One2many('purchase.subscription','current_revision_id','Old revisions',readonly=True,context={'active_test': False})
    revision_number = fields.Integer('Revision',copy=False)
    unrevisioned_name = fields.Char('Order Reference',copy=False,readonly=True)
    active = fields.Boolean('Active',default=True,copy=True) 
    revised = fields.Boolean('Revised Subscription')
    
    amount_lease_original = fields.Monetary(string='Original Amount')
    amount_lease_current = fields.Monetary(string='Current amount', compute='_compute_lease_current')
    amount_lease_total = fields.Monetary(string='Total Committment',  compute='_compute_lease_total')
    
    adj_purchase_subscription_id = fields.Many2one('purchase.subscription','Adjusting Subscription',readonly=True,copy=True)
    adj_no = fields.Integer(string='Adjustment No.')
    subscription_adjustment_count = fields.Integer(compute='_compute_adjustment_count')
    
    @api.onchange('adj_purchase_subscription_id')
    def _onchange_adj_purchase_subscription_id(self):
        if not self.adj_purchase_subscription_id:
            return

        self = self.with_company(self.company_id)
        subscription = self.adj_purchase_subscription_id
        
        self.company_id = subscription.company_id.id
        self.currency_id = subscription.currency_id.id
        self.partner_id = subscription.partner_id.id
        self.subscription_plan_id = subscription.subscription_plan_id.id
        self.subscription_type_id = subscription.subscription_type_id.id
        self.project_id = subscription.project_id.id
        self.product_id = subscription.product_id.id
        self.analytic_account_id = subscription.analytic_account_id.id
        self.candidate = subscription.candidate
        self.name = subscription.name + '-' + str(subscription.adj_no + 1)
        self.subscription_date = fields.Date.today()
        self.user_id = self.env.user
        self.amount_lease_original = subscription.amount_lease_original
        subscription.update({
            'adj_no': subscription.adj_no + 1
        })
        
    
    def _compute_adjustment_count(self):
        Adjustment = self.env['purchase.subscription']
        can_read = Adjustment.check_access_rights('read', raise_exception=False)
        for subscription in self:
            subscription.subscription_adjustment_count = can_read and Adjustment.search_count([('adj_purchase_subscription_id', '=', subscription.id)]) or 0
            
            
    def _compute_lease_current(self):
        amount = 0
        for subs in self:
            amount = 0
            subs_schedule_line_id = self.env['purchase.subscription.schedule'].search([('purchase_subscription_id','=',subs.id),('date_from','<=',fields.date.today()),('date_to','>=',fields.date.today())],limit=1,order="date_from")
            amount = subs_schedule_line_id.recurring_monthly_total
            subs.amount_lease_current = amount
            
    def _compute_lease_total(self):
        total = 0
        for subs in self:
            total = 0
            for line in subs.purchase_subscription_schedule_line:
                total += line.recurring_total
            subs.amount_lease_total = total
    
    @api.onchange('select_all')
    def _select_all(self):
        for line in self.purchase_subscription_schedule_line:
            if line.state =='draft':
                line.record_selection = self.select_all
    
    def add_record(self):
        lines_data = {}
        for line in self.purchase_subscription_schedule_line:
            date_from = line.date_from
            date_to = line.date_to
            accum = line.accum_escalation
        
        date_from = date_to + relativedelta(days=1)
        date_to = date_from + relativedelta(months=12,days=-1)
            
        subscription_schedule_id = self.env['purchase.subscription.schedule']
        for sub in self:
            lines_data = ({
                'purchase_subscription_id': self.id,
                'date_from': date_from,
                'date_to': date_to,
                'recurring_price': self.recurring_price,
                'recurring_intervals': 12,
                'discount': 0,
                'escalation':  0,
                'accum_escalation': accum,
            })
            #self.env['purchase.subscription.schedule'].create(lines_data)
            subscription_schedule_id.create(lines_data)
            #sub.purchase_subscription_schedule_line(lines_data)
    
    def create_bill(self):
        product_id = False
        for line in self.purchase_subscription_line:
            product_id = line.product_id  
        invoice = self.env['account.move']
        lines_data = []
        doc_name = doc_name1 = ''
        if self.purchase_subscription_schedule_line:
            for line in self.purchase_subscription_schedule_line.filtered(lambda r: r.record_selection == True and not r.invoice_id):
                #if line.record_selection:
                lines_data = []
                lines_data.append([0,0,{
                    'name': str(self.name) + ' ' + str(product_id.name),
                    'purchase_subscription_id': self.id,
                    'purchase_subscription_schedule_id': line.id,
                    'price_unit': line.recurring_monthly_total or 0.0,
                    #'discount': line.discount,
                    'quantity': line.recurring_intervals,
                    'product_uom_id': product_id.uom_id.id,
                    'product_id': product_id.id,
                    'tax_ids': [(6, 0, product_id.supplier_taxes_id.ids)],
                    'subscription_start_date': line.date_from,
                    'subscription_end_date':line.date_to,
                    #'analytic_account_id': line.analytic_account_id.id,
                    #'analytic_tag_ids': [(6, 0, line.analytic_tag_ids.ids)],
                    #'project_id': line.project_id.id,
                }])
                line.update({
                    'state': 'invoice',
                })
                #date_start = line.date_from
                #date_start = datetime.strptime(date_start, '%Y-%m-%d %H:%M:%S')
                #date_start = date_start.strftime("%d/%m/%Y")
                #doc_name = line.date_from.strftime("%d/%m/%Y")

                #doc_name = str(datetime.strptime(line.date_from, '%d-%m-%Y')) + str(datetime.strptime(line.date_to, '%d-%m-%Y'))
                #doc_name + str(line.date_from.strftime("%d/%m/%Y")) + str(line.date_to.strftime("%d/%m/%Y"))
                #do_date = datetime.strptime(line.date_from, "%Y-%m-%d %H:%M:%S")
                #day = do_date.day
                #month = str(do_date.month)
                #doc_name = fields.Datetime.to_string(line.date_from.strftime("%d/%m/%Y")) 
                #doc_name = fields.Datetime.to_string(line.date_from)
                doc_name = line.date_from.strftime("%Y") + '-' + str(line.date_from.strftime("%m"))
                doc_name1 = str(line.date_from.strftime("%-m"))
                invoice.create({
                    #'name': self.name + '-' + str(line.date_from) + '-' + str(line.date_to),
                    'la_inv_number': self.name + '-' + doc_name,
                    'name': '/',
                    'move_type': 'in_invoice',
                    'purchase_subscription_id': self.id,
                    'invoice_date': fields.Datetime.now(),
                    'partner_id': self.partner_id.id,
                    #'partner_shipping_id': self.partner_id.id,
                    'currency_id': self.currency_id.id,
                    'journal_id': self.subscription_plan_id.journal_id.id,
                    'invoice_origin': self.name,
                    #'fiscal_position_id': fpos.id,
                    'invoice_payment_term_id': self.partner_id.property_supplier_payment_term_id.id,
                    'narration': self.name,
                    'invoice_user_id': self.user_id.id,
                    #'partner_bank_id': company.partner_id.bank_ids.filtered(lambda b: not b.company_id or b.company_id == company)[:1].id,
                    'invoice_line_ids':lines_data,
                })
                invoice.update({
                    'name': self.name + str(line.date_from) + '-' + str(line.date_to),
                })
            #return invoice
        
    #revision methods
    @api.model
    def create1(self, vals):
        if 'unrevisioned_name' not in vals:
            if vals.get('name', 'New') == 'New':
                seq = self.env['ir.sequence']
                vals['name'] = seq.next_by_code('purchase.subscription') or '/'
            vals['unrevisioned_name'] = vals['name']
#             vals['revised'] = True
        return super(PurchaseSubscription, self).create(vals)
    
    def action_revision(self):
        self.ensure_one()
        view_ref = self.env['ir.model.data'].get_object_reference('de_purchase_subscription', 'purchase_subcription_form_view')
        view_id = view_ref and view_ref[1] or False,
        self.with_context(purchase_revision_history=True).copy()
        stage_id = self.env['purchase.subscription.stage'].search([('subscription_type_ids','=',self.id),('stage_category','=','draft')],limit=1)
        self.write({'stage_id': stage_id.id})
        #self.order_line.write({'state': 'draft'})
        revision_seq= 1
        revision_r = self.name.__contains__("-R0")
        if revision_r: 
            revision_seq= int (self.name[-1:]) +1 
        final_revision_seq= str ('-R0') + str (revision_seq) 
        if not revision_r:
            self.name = self.name + str (final_revision_seq)
        if revision_r:
           self.name = self.name[:-1] + str (revision_seq) 
        
#         self.mapped('order_line').write(
#             {'sale_line_id': False})
        return {
            'type': 'ir.actions.act_window',
            'name': _('Purchase Subscription'),
            'res_model': 'purchase.subscription',
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'current',
            'nodestroy': True,
        }
        
    @api.returns('self', lambda value: value.id)
    def copy(self, defaults=None):
        stage_id = self.env['purchase.subscription.stage'].search([('subscription_type_ids','=',self.id),('stage_category','=','cancel')],limit=1)
        if not defaults:
            defaults = {}
        if not self.unrevisioned_name:
            self.unrevisioned_name = self.name
        if self.env.context.get('purchase_revision_history'):
            prev_name = self.name
            revno = self.revision_number
            self.write({'revision_number': revno + 1,})
            defaults.update({'revision_number': revno,'revised':True,'active': True,'current_revision_id': self.id,'unrevisioned_name': self.unrevisioned_name,})
        return super(PurchaseSubscription, self).copy(defaults)
    
class PurchaseSubscriptionSchedule(models.Model):
    _name = 'purchase.subscription.schedule'
    _description = 'Purchase Subscription Schedule'
    
    purchase_subscription_id = fields.Many2one('purchase.subscription', string='Subscription', ondelete='cascade')
    
    record_selection = fields.Boolean(string='Selection', default=False, copy=False)

    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')
    recurring_price = fields.Float(string="Recurring Price", )
    recurring_intervals = fields.Integer(string="Intervals", )
    recurring_sub_total = fields.Float(string="Subtotal", compute='_compute_recurring_total_all')
    
    discount = fields.Float(string='Discount (%)', digits='Discount')
    escalation = fields.Float(string='Escalation (%)', digits='Discount')
    accum_escalation = fields.Float(string='Accum. Escalation (%)', digits='Discount')
    escalation_amount = fields.Float(string="Escalation Amount")
    
    recurring_monthly_total = fields.Float(string="Monthly Price", compute='_compute_recurring_total_all')
    recurring_total = fields.Float(string="Total", compute='_compute_recurring_total_all')
    
    invoice_id = fields.Many2one('account.move', string="Invoice", check_company=True, compute='_get_invoice')
    invoice_status = fields.Selection(related='invoice_id.state')
    company_id = fields.Many2one('res.company', related='purchase_subscription_id.company_id', store=True, index=True)    
    state = fields.Selection(selection=[
            ('draft', 'Draft'),
            ('invoice', 'Invoice Created'),
            ('posted', 'Posted'),
            ('cancel', 'Cancelled'),
        ], string='Status', required=True, readonly=True, copy=False, tracking=True,
        default='draft')
    
    schedule_note = fields.Char(string='Comments')
    is_refunded = fields.Boolean(string='Refunded')
    is_overlap = fields.Boolean(string='Is Overlap')
    payment_details = fields.Char(string='Payment Details')
    
    @api.onchange('escalation')
    def _onchange_escalation(self):
        for line in self:
            line.accum_escalation = line.escalation
    
    def _get_invoice(self):
        for line in self:
            line.invoice_id = self.env['account.move.line'].search([('purchase_subscription_schedule_id','=',line.id)],limit=1).move_id.id
            
    def _compute_recurring_total_all(self):
        for line in self:
            line.recurring_sub_total = line.recurring_price * line.recurring_intervals
            #line.recurring_total = line.recurring_sub_total + (line.recurring_sub_total * (line.accum_escalation / 100)) - (line.recurring_sub_total * (line.discount / 100))
            #line.recurring_monthly_total = line.recurring_price + (line.recurring_price * (line.accum_escalation / 100))
            line.recurring_monthly_total = line.escalation_amount
            line.recurring_total = line.escalation_amount * line.recurring_intervals

