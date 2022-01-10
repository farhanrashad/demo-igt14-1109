# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class FuelRefillingEntry(models.Model):
    _name = 'fuel.refilling.entry'
    _description = 'Fuel Refilling Entry'
    
    
    @api.model
    def create(self, vals):
        vals['name'] = (
            vals.get('name') or
            self.env.context.get('default_name') or
            self.env['ir.sequence'].with_company(vals.get('company_id')).next_by_code('fuel.refilling.entry') or
            'New'
        )
        if vals.get('name', 'New') == 'New':
            vals['name'] = vals['name']
       
        refill = super(FuelRefillingEntry, self).create(vals)
       
        return refill
   
    
    name = fields.Char(required=True, tracking=True, default="New")
    refill_date = fields.Datetime(string='Refill Date')
    company_id = fields.Many2one('res.company', store=True, default=lambda self: self.env.company)
    location_src_id = fields.Many2one('stock.location', string="Location", domain=[('is_filling','=',True)])
    owner_id = fields.Many2one('res.partner', string="Owner")
    state = fields.Selection(selection=[
            ('draft', 'Draft'),
            ('confirmed', 'In-Filling'),
            ('done', 'Refilled'),
        ], string='Status', required=True, readonly=True, copy=False, tracking=True,
        default='draft')
    refill_line_ids = fields.One2many('fuel.refilling.entry.line', 'refilling_id', string="Refilling Lines")
    
    
    class FuelRefillingEntryline(models.Model):
        _name = 'fuel.refilling.entry.line'
        _description = 'Fuel Refilling Entry Line'
        
        
        location_id = fields.Many2one('stock.location' , string="Location")
        refilling_id = fields.Many2one('fuel.refilling.entry' , string="Refilling Entry")
        product_id = fields.Many2one(related='location_id.product_id')
        current_quantity = fields.Float(string='Current Quantity')
        refill_quantity = fields.Float(string='Refill Quantity')
        closing_quantity = fields.Float(string='Closing Quantity')
        
        
        
        
    
    
    
    

