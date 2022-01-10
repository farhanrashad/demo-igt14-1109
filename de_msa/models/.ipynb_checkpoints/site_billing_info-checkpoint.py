# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class site_billing_info(models.Model):
    _name = 'site.billing.info'
    _description = 'Site Building Info'

    
#     @api.model
#     def create(self, vals):
#         record_exists = self.search([('site_id', '=', vals['site_id'])])
# 
#         if record_exists:
#             raise UserError(('Site ('+str(record_exists.site_id.name)+') in the current MSA already exists!'))
#         else:
#             pass
#            
#         rec = super(site_billing_info, self).create(vals)
#         return rec
    
    def compute_name(self):
        for rec in self:
            if rec.site_id:
                rec.name = rec.site_id.name
            else:
                rec.name = None
    

    name = fields.Char(string='Customer Site Reference', compute='compute_name')
    site_id = fields.Many2one('project.project', string='Site')
    site_tower_type = fields.Many2one('product.product', string='Site Tower Type')
    inv_tower_type = fields.Many2one('product.product', string='Invoiced Tower Type')
    site_power_model = fields.Many2one('product.product', string='Site Power Model')
    inv_power_model = fields.Many2one('product.product', string='Invoiced Power Model')
    indoor_bts = fields.Integer(string='# Indoor BTS', help="This is used for the O&M to be able to control the energy consumption.")
    outdoor_bts = fields.Integer(string='# Outdoor BTS', help="This is used for the O&M to be able to control the energy consumption.")
    ip_start_date = fields.Date(string='IP Fee Start Date')
    ip_end_date = fields.Date(string='IP Fee End Date')
    billable = fields.Boolean(string='Billable', help="Flag indicating that the site is now eligible for billing (this should be linked to the 80% cluster rule for Telenor")
    head_lease_full_extra = fields.Boolean(string='Lease Agreement Full Extra')
    billable_lease_amount = fields.Float(string='Billable Lease Amount', required=True)
    network_type_id = fields.Many2one('network.type', string='Network Type')
    site_class = fields.Selection([('critical', 'Critical'), ('normal', 'Normal')], string='Site Class', default='critical')
    msa_id = fields.Many2one('master.service.agreement', string='Master Service Agreement')  
    
    