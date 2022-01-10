# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date

class ProjectProject(models.Model):
    _inherit = 'project.project'
    
    product_id = fields.Many2one('product.product', string='Tower Type', domain="[('is_product_category_tower','=',True)]")
    
    power_product_ids = fields.One2many('project.power.product.line', 'project_id', string='Power Line', copy=True)
    project_contractor_ids = fields.One2many('project.contractor.line', 'project_id', string='Contractors', copy=True)
    
    purchase_line_ids = fields.One2many('purchase.order.line', 'project_id', string='PO Lines', copy=False, readonly=True)
    site_billing_info_ids = fields.One2many('site.billing.info', 'site_id', string='Billing Info', copy=False, readonly=True)
    asset_ids = fields.One2many('account.asset', 'project_id', string='Assets', copy=False, readonly=True)
    
    purchase_subscription_ids = fields.One2many('purchase.subscription', 'project_id', string='Purchase Subscriptions', copy=False, readonly=True)
    
    amount_lease_current = fields.Monetary(string='Current amount', compute='_compute_lease_current')
    currency_id = fields.Many2one(string='Currency', compute='_compute_lease_current')
    def _compute_lease_current(self):
        amount = 0
        subscription_ids = self.env['purchase.subscription']
        subs_schedule_line_id = self.env['purchase.subscription.schedule']
        for project in self:
            amount = 0
            subscription_ids = self.env['purchase.subscription'].search([('project_id','=',project.id),('stage_category','not in',['closed','cancel'])])
            for sub in subscription_ids:
                amount += sub.amount_lease_current
                project.currency_id = sub.currency_id.id
            project.amount_lease_current = amount
            
            
    
    
class ProjectPowerModelLine(models.Model):
    _name = 'project.power.product.line'
    _description = 'Project Power Products'
    
    project_id = fields.Many2one('project.project', string='Project', index=True, required=True, ondelete='cascade')
    period = fields.Char(string='Period')
    date_start = fields.Date(string='Start Date')
    date_end = fields.Date(string='End Date')
    product_id = fields.Many2one('product.product', string='Power Product', readonly=False, ondelete='restrict', tracking=True, index=True, copy=False,  domain="[('is_product_category_power','=',True)]" )
    
class ProjectContract(models.Model):
    _name = 'project.contractor.line'
    _description = 'Project Contractors'
    
    project_id = fields.Many2one('project.project', string='Project', index=True, required=True, ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string='Partner')
    date_start = fields.Date(string='Start Date')
    date_end = fields.Date(string='End Date')