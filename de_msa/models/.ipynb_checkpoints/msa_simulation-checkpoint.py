from datetime import datetime
import math
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class msa_simulation(models.Model):
    _name = 'msa.simulation'
    _description = 'MSA Simulation'
    
    @api.depends('msa_id','site_billing_info_id','site_id')
    def compute_values(self):
        for rec in self:
            if rec.month_days > 0:
    #             ((Tower Capex Rate*Regional Factor*Wind Factor*Collocation Discount)/No. of Days in Month)*Invoicing Days*Capex CPI
                ip_fee_capex = ((rec.gross_ip_fee_capex * rec.region_factor * rec.wind_factor * rec.collocation_capex)/rec.month_days) * rec.invoicing_days * rec.capex_escalation
                
    #             ((Tower Opex Rate*Regional Factor*SLA Factor*Collocation Discount*Exchange Rate)/No. of Days in Month)* Invoicing Days
                rec.ip_fee_opex = ((rec.gross_ip_fee_opex * rec.region_factor * rec.collocation_opex * rec.msa_id.exchange_rate) / rec.month_days) * rec.invoicing_days
                
    #             ((Power Capex Rate*Regional Factor*Collocation Discount)/No. of Days in Month)*Invoicing Days*Capex CPI
                rec.power_fee_capex = ((rec.power_price_capex * rec.region_factor * rec.collocation_capex) / rec.month_days) * rec.invoicing_days * rec.capex_escalation
        
    #             (200-(Monthly Lease Amount/Exchange Rate))/(No.of Tenants+1)
                rec.head_lease = (200-(rec.monthly_lease_amount / rec.msa_id.exchange_rate)) / (rec.no_of_tenants_capex+1)
                
    #             Tower w/o Power Capex + Power Capex
                rec.ip_fee_capex = ip_fee_capex + rec.power_fee_capex
                
            else:
                rec.ip_fee_opex = 0
                rec.power_fee_capex = 0 
                rec.head_lease = 0
                rec.ip_fee_capex = 0 
    
    
    
    msa_id = fields.Many2one('master.service.agreement', string='Master Service Agreement')
    site_billing_info_id = fields.Many2one('site.billing.info', string='Site Billing Info')
    site_id = fields.Many2one('project.project', string='Site', readonly=True)
    region_factor = fields.Float(string='Region Factor')
    year = fields.Char(string='Year')
    head_lease_full_extra = fields.Boolean(string='Head Lease Full Extra', readonly=True)
    inv_tower_type = fields.Many2one('product.product', string='Tower Type', readonly=True)
    inv_power_model = fields.Many2one('product.product', string='Power Model', readonly=True)
    ip_fee_capex = fields.Float(string='Tower w/o Power CAPEX', )
    ip_fee_opex = fields.Float(string='Tower w/o Power OPEX')
    power_fee_capex = fields.Float(string='Power CAPEX', )
    opex_cpi = fields.Float(string='CPI OPEX')
    capex_escalation = fields.Float(string='CPI CAPEX')
    collocation_capex = fields.Float(string='Collocation Discount for Tower CAPEX')
    collocation_opex = fields.Float(string='Collocation Discount for Tower OPEX')
    head_lease = fields.Float(string='Lease Agreement', )
    head_lease_extra = fields.Float(string='Lease Agreement Extra')
    num_of_tenant = fields.Float(string='Number of Tenants')
    gross_ip_fee_capex = fields.Float(string='IP Fee CAPEX')
    gross_ip_fee_opex = fields.Float(string='IP Fee OPEX')
    gross_ip_fee = fields.Float(string='Gross IP Fee')
    ip_fee = fields.Float(string='IP Fee')
    wind_factor =  fields.Float(string='Wind Factor')
    sla_factor = fields.Float(string='SLA Factor')
    invl_fuel_total = fields.Float(string='Last Month Energy Bill Fuel')
    invl_enegry_total = fields.Float(string='Last Month Energy Bill Electricity')
    invoicing_days = fields.Integer(string='Invoicing Days')
    invoiced_rent_adjustment = fields.Float(string='Invoiced Rent Adjustment')
    mini_cluster = fields.Char(string='Mini Cluster')
    #cluster = fields.Many2one('site.cluster', 'Cluster')
    month_year = fields.Char(string='Month Year')
    ip_start_date = fields.Date(string='IP Fee Start Date', readonly=True)
    simulation_date = fields.Date(string='Simulation Date')
    ip_fee_capex_billed = fields.Float(string='IP Fee Capex Billed')
    diff_capex = fields.Float(string='Diff. Capex')
    ip_fee_opex_billed = fields.Float(string='IP fee Opex billed')
    diff_opex = fields.Float(string='Diff. Opex')
    month_days = fields.Integer(string='Month Days')
    power_price_capex = fields.Float(string='Power Price Capex')
    monthly_lease_amount = fields.Float(string='Montly Lease Amount')
    no_of_tenants_capex = fields.Integer(string='No. of Tenants Capex')
    rfu_date = fields.Date(string='RFU Date')
    lease_amount = fields.Float(string='Lease Amount')
    opex_after_cpi = fields.Float(string='Opex after CPI')
    capex = fields.Float(string='Capex')
    opex = fields.Float(string='Opex')
    lease_sharing = fields.Float(string='Lease Sharing')
    final_opex = fields.Float(string='Final Opex')
    
    
    