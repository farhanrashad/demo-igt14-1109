# -*- encoding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import date, datetime, timedelta
from odoo.exceptions import UserError

class master_service_agreement(models.Model):
    _name = 'master.service.agreement'
    _description = 'Master Service Agreement'
    
    def get_tower_type(self, site, period):
        id = None
        model = self.env['monthly.tower.model'].search([('msa_id','=',self.id),('site_id','=',site.id),('period','=',period)], order="id desc", limit=1)
            
        if model:
            id = model.tower_model.id
        return id
    
    def get_power_model(self, site, period):
        id = None
        model = self.env['monthly.power.model'].search([('msa_id','=',self.id),('site_id','=',site.id),('period','=',period)], order="id desc", limit=1)
        
        if model:
            id = model.power_model.id
        return id
    
    
    def tower_capex_rate(self, site, period):
        tower_capex_rate = 0
        if self.tower_without_power_ids:
            model = self.env['monthly.tower.model'].search([('msa_id','=',self.id),('site_id','=',site.id),('period','=',period)], order="id desc", limit=1)
            
            if model:
                id = model.tower_model.id
                
                for line in self.tower_without_power_ids:
                    if line.tower_type.id == id:
                        tower_capex_rate = line.ip_fee_capex
                    
        return tower_capex_rate
    
    
    def tower_opex_rate(self, site, period):
        tower_opex_rate = 0
        if self.tower_without_power_ids:
            model = self.env['monthly.tower.model'].search([('msa_id','=',self.id),('site_id','=',site.id),('period','=',period)], order="id desc", limit=1)
            
            if model:
                id = model.tower_model.id
                
                for line in self.tower_without_power_ids:
                    if line.tower_type.id == id:
                        tower_opex_rate = line.ip_fee_opex

        return tower_opex_rate
    
    def regional_factor(self, region):
        regional_factor = 0
        if self.location_factor_ids:
            for loc_fac in self.location_factor_ids:
                if loc_fac.state_id.id == region.id:
                    regional_factor = loc_fac.factor
        return regional_factor
        
    def wind_factor(self, site, period):        
        wind_factor = 0
        if self.wind_factor_ids:
            model = self.env['monthly.tower.model'].search([('msa_id','=',self.id),('site_id','=',site.id),('period','=',period)], order="id desc", limit=1)
            
            if model:
                id = model.tower_model.wind_factor.id
                
                if id:
                    for line in self.wind_factor_ids:
                        if line.name.id == id:
                            wind_factor = line.factor
            
        return wind_factor
    
    def sla_factor(self, site, period):        
        sla_factor = 0
        if self.sla_factor_ids:
            model = self.env['monthly.sla.factor'].search([('msa_id','=',self.id),('site_id','=',site.id),('period','=',period)], order="id desc", limit=1)
            
            if model:
                id = model.sla_factor.id
                
                if id:
                    for line in self.sla_factor_ids:
                        if line.name.id == id:
                            sla_factor = line.factor
        return sla_factor
        
    def collocation_discount_capex(self):
        collocation_discount = 0
        if self.collocation_capex_ids:
            for collocation_line in self.collocation_capex_ids:
                if int(collocation_line.year) == int(self.simulation_date_from.year):
                    collocation_discount = collocation_discount + collocation_line.factor_for_1 + collocation_line.factor_for_2 + collocation_line.factor_for_3 + collocation_line.factor_for_4 + collocation_line.factor_for_5 + collocation_line.factor_for_6
        return collocation_discount
    
    
    def collocation_discount_opex(self):
        collocation_discount = 0
        if self.collocation_opex_ids:
            for collocation_line in self.collocation_opex_ids:
                if int(collocation_line.year) == int(self.simulation_date_from.year):
                    collocation_discount = collocation_discount + collocation_line.factor_for_1 + collocation_line.factor_for_2 + collocation_line.factor_for_3 + collocation_line.factor_for_4 + collocation_line.factor_for_5 + collocation_line.factor_for_6
        return collocation_discount
    
    def capex_cpi(self):
        capex_cpi = 0
        if self.capex_escalation_ids:
            for capex_line in self.capex_escalation_ids:
                if int(capex_line.year) == int(self.simulation_date_from.year):
                    capex_cpi = capex_cpi + capex_line.cpi
        return capex_cpi
    
    def opex_cpi(self):
        opex_cpi = 0
        if self.opex_cpi_ids:
            for opex_line in self.opex_cpi_ids:
                if int(opex_line.year) == int(self.simulation_date_from.year):
                    opex_cpi = opex_cpi + opex_line.cpi
        return opex_cpi
    
    def power_price_capex(self, site, period):
        power_price_capex = 0
        
        if self.power_prices_ids:
            model = self.env['monthly.power.model'].search([('msa_id','=',self.id),('site_id','=',site.id),('period','=',period)], order="id desc", limit=1)
            
            if model:
                id = model.power_model.id
                
                for line in self.power_prices_ids:
                    if line.power_type.id == id:
                        power_price_capex = line.ip_fee_capex
        
        return power_price_capex
            
    
    def no_of_tenants(self):
        no_of_tenants = 0
        if self.collocation_capex_ids:
            for line in self.collocation_capex_ids:
                if int(line.year) == int(self.simulation_date_from.year):
                    if line.factor_for_1 > 0:
                        no_of_tenants = no_of_tenants+1
                    if line.factor_for_2 > 0:
                        no_of_tenants = no_of_tenants+1
                    if line.factor_for_3 > 0:
                        no_of_tenants = no_of_tenants+1
                    if line.factor_for_4 > 0:
                        no_of_tenants = no_of_tenants+1
                    if line.factor_for_5 > 0:
                        no_of_tenants = no_of_tenants+1
                    if line.factor_for_6 > 0:
                        no_of_tenants = no_of_tenants+1
        return no_of_tenants
    
    
    def refresh_simulation(self):
        for line in self.msa_simulation_ids:
            line.unlink()
            
        month_days = self.number_days_in_month
        invoicing_days = self.number_days_in_month
        
        #period from date
        month = self.simulation_date_from.month
        month = str(month).zfill(2)
        year = self.simulation_date_from.year
        period = month+'/'+str(year)

        
        for line in self.site_billing_info_ids:
            print('line.site_id',line.site_id.name)
            #region from site
            site_region = line.site_id.state_id
            site = line.site_id
#             
#     #         ( (Tower Capex Rate*Regional Factor*Wind Factor*Collocation Discount)/No. of Days in Month)*Invoicing Days*Capex CPI
#             tower_without_power_capex = ((self.tower_capex_rate(site, period) * self.regional_factor(site_region) * self.wind_factor(site, period) * self.collocation_discount_capex()) / month_days) * invoicing_days * self.capex_cpi()
#     
#     #         ((Tower Opex Rate*Regional Factor*SLA Factor*Collocation Discount*Exchange Rate)/No. of Days in Month)* Invoicing Days
#     #         Power Opex Rate ==fixme
#             tower_without_power_opex = ((self.tower_opex_rate(site, period) * self.regional_factor(site_region) * self.collocation_discount_opex() * self.exchange_rate) / month_days) * invoicing_days
#     
#     #         ((Power Capex Rate*Regional Factor*Collocation Discount)/No. of Days in Month)*Invoicing Days*Capex CPI
#             power_capex =  ((self.power_price_capex(site, period) * self.regional_factor(site_region) * self.collocation_discount_capex()) / month_days) * invoicing_days * self.capex_cpi()
#             
#     #         (200-(Monthly Lease Amount/Exchange Rate))/(No.of Tenants+1)
#             lease_sharing = (200-(line.billable_lease_amount / self.exchange_rate)) / (self.no_of_tenants()+1)
#     
#     #         Tower w/o Power Capex + Power Capex
#             ip_fees_capex = tower_without_power_capex + power_capex
#             
#     #         ((Tower w/o Power Opex)+Lease Sharing)*Opex CPI
#             ip_fees_opex_tml =  (tower_without_power_opex + lease_sharing) * self.opex_cpi()
#             
#     #         (Tower w/o Power Opex)+((Tower w/o Power Opex-Lease Amount))*Opex CPI
#             ip_fees_opex_oml = tower_without_power_opex + (tower_without_power_opex - line.billable_lease_amount) * self.opex_cpi()
#             
            
            line = {
                'region_factor': self.regional_factor(site_region),
#                 'ip_fee_capex': ip_fees_capex,
#                 'ip_fee_opex': tower_without_power_opex,
                'opex_cpi': self.opex_cpi(),
                'capex_escalation': self.capex_cpi(),
                'collocation_capex': self.collocation_discount_capex(),
                'collocation_opex': self.collocation_discount_opex(),
#                 'power_fee_capex': power_capex,
                'gross_ip_fee_capex': self.tower_capex_rate(site, period),
                'gross_ip_fee_opex': self.tower_opex_rate(site, period),
                'wind_factor': self.wind_factor(site, period),
                'sla_factor': self.sla_factor(site, period),
                'num_of_tenant': self.no_of_tenants(),
                'invoicing_days': invoicing_days,
#                 'head_lease': lease_sharing,
                'simulation_date': self.simulation_date_from,
                'ip_start_date': line.ip_start_date,
                'site_id': site.id,
                'month_year': period,
                'inv_tower_type': self.get_tower_type(site, period),
                'inv_power_model': self.get_power_model(site, period),
                'month_days': month_days,
                'power_price_capex': self.power_price_capex(site, period),
                'monthly_lease_amount': line.billable_lease_amount,
                'no_of_tenants_capex': self.no_of_tenants(),
                'site_billing_info_id': line.id,
                'msa_id': self.id,
                
            }
            simulation_rec = self.msa_simulation_ids.create(line)
#         raise UserError((tower_without_power_capex, tower_without_power_opex))
    
    def create_capax_invoice(self):
        line_vals = []
        
        if self.msa_simulation_ids:
            for line in self.msa_simulation_ids:
                line_vals.append((0, 0, {
#                     'product_id': line.site_id.name,
                    'name': line.site_id.name,
                    'quantity': 1,  
#                     'currency_id': line.currency_id.id,
                    'price_unit': line.ip_fee_capex,
                    'partner_id': self.partner_id.id,
#                     'product_uom_id': line.product_uom.id,
                }))
                line_vals.append(line_vals)
        
            vals = {
                'partner_id': self.partner_id.id,
#                 'invoice_date_due': self.end_date,
                'invoice_date': fields.Date.today(),
                'move_type': 'out_invoice',
#                 'type': 'out_invoice',
                'invoice_origin': self.name,
                'invoice_line_ids': line_vals,
            }
            move = self.env['account.move'].create(vals)
            move.msa_id = self.id
            move.category = 'Capex'

    
    def create_opex_invoice(self):
        line_vals = []
        
        if self.msa_simulation_ids:
            for line in self.msa_simulation_ids:
                line_vals.append((0, 0, {
#                     'product_id': line.site_id.name,
                    'name': line.site_id.name,
                    'quantity': 1,  
#                     'currency_id': line.currency_id.id,
                    'price_unit': line.ip_fee_opex,
                    'partner_id': self.partner_id.id,
#                     'product_uom_id': line.product_uom.id,
                }))
                line_vals.append(line_vals)
        
            vals = {
                'partner_id': self.partner_id.id,
#                 'invoice_date_due': self.end_date,
                'invoice_date': fields.Date.today(),
                'move_type': 'out_invoice',
#                 'type': 'out_invoice',
                'invoice_origin': self.name,
                'invoice_line_ids': line_vals,
            }
            move = self.env['account.move'].create(vals)
            move.msa_id = self.id
            move.category = 'Opex'
    


    def get_number_of_days(self):
        if self.simulation_date_from and self.simulation_date:
            delta = self.simulation_date_from - self.simulation_date
            self.number_days_in_month = abs(delta.days)+1
        else:
            self.number_days_in_month = None
    
    
    def compute_final_total_fees(self):
        total = 0
        for rec in self:
            if rec.msa_simulation_ids:
                for line in rec.msa_simulation_ids:
                    total = total + line.ip_fee_capex
            rec.total_gross_capex = total
    
    
    name = fields.Char('Reference', required=True)
    partner_id = fields.Many2one('res.partner', 'Customer', required=True)
    date_from = fields.Date('Date From', required=True)
    date_to = fields.Date('Date To', required=True)
    head_lease_invoicing_limit = fields.Float('Lease Agreement Invoicing Limit')
    la_extra_special_division = fields.Boolean('LA Extra Computation')
    oml_colo = fields.Boolean(string='OML Colo')
    
    site_billing_info_ids = fields.One2many('site.billing.info', 'msa_id', string='Site Billing Information')
    tower_currency_id = fields.Many2one('res.currency', string='Tower Currency', required=True)
    tower_without_power_ids = fields.One2many('tower.without.power', 'msa_id', string='Tower w/o Power')
    power_currency_id = fields.Many2one('res.currency', string='Power Currency', required=True)
    power_prices_ids = fields.One2many('power.prices', 'msa_id', string='Power Prices')
    location_factor_ids = fields.One2many('location.factor', 'msa_id', string='Location Factors')
    wind_factor_ids = fields.One2many('wind.factor', 'msa_id', string='Wind Factors')
    sla_factor_ids = fields.One2many('sla.factor', 'msa_id', string='SLA Factors')
    collocation_capex_ids = fields.One2many('collocation.discount.tower.capex', 'msa_id', string='Collocation Discount for Tower CAPEX')
    capex_comment = fields.Text('Comment for CAPEX')
    collocation_opex_ids = fields.One2many('collocation.discount.tower.opex', 'msa_id', string='Collocation Discount for Tower OPEX')
    opex_comment = fields.Text('Comment for OPEX')
    opex_cpi_ids = fields.One2many('opex.cpi', 'msa_id', string='Opex CPI')
    capex_escalation_ids = fields.One2many('capex.escalation', 'msa_id', string='CAPEX Escalation')
    penalty_ids = fields.One2many('msa.penalty', 'msa_id', string='Penalties')
    site_load_ids = fields.One2many('site.load', 'msa_id', string='Site Load')
    msa_simulation_ids = fields.One2many('msa.simulation', 'msa_id', string='Price Details')
    total_gross_capex = fields.Float(string='Total IP Fee CAPEX')
    total_gross_opex = fields.Float(string='Total IP Fee OPEX')
    number_days_in_month = fields.Float(string='Number Days In Month', compute='get_number_of_days')
    diff_billing = fields.Boolean('Differential Billing')
    simulation_date = fields.Date('Simulation Date To')
    simulation_date_from = fields.Date('Simulation Date From')
    exchange_rate = fields.Float(string='Exchange Rate (from USD to MMK)', default=1, help="1 USD = ? MMK. '?' is the Exchange Rate.")
    invoice_date = fields.Date(string='Invoice Date')
    gross_ip_fee = fields.Float(string='Total Gross IP Fee')
    ip_fee = fields.Float(string='Total IP Fee')
    account_invoice_ids = fields.One2many('msa.invoice.line', 'msa_id')
    invoice_ids = fields.One2many('account.move', 'msa_id')
    collocation_power_capex_ids = fields.One2many('collocation.discount.power.capex', 'msa_id', string='Collocation Discount for Power CAPEX')
    collocation_power_capex = fields.Text('Comment for Power CAPEX')
    target_pass_through_ids = fields.One2many('target.pass.through', 'msa_id', string='Target Pass-Through')
    
    opex_currency_id = fields.Many2one('res.currency', string='OPEX Currency')
    capex_currency_id = fields.Many2one('res.currency', string='CAPEX Currency')
