# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import UserError

class VehicleFleetWizard(models.TransientModel):
    _name = 'assigning.fleets'
    _description = 'Vehicle Fleet Selection'
    
    assign_fleet = fields.Many2one('fleet.vehicle', string="Vehicle")
    
    def action_create(self):
        model = self.env.context.get('active_model')
        rec = self.env[model].browse(self.env.context.get('active_id'))
        
        already_assigned = self.env['fleet.request'].search([('requested_model','=',self.assign_fleet.id),('state','=','assigned')])
        
        if already_assigned:
            raise UserError(('Selected vehical is already assigned! Please select another.'))
            
        rec.requested_model = self.assign_fleet.id
        rec.state ='assigned'
        rec.assign_by = self.env.user
        rec.assign_date = datetime.today()
        rec.image_fleet_request = self.assign_fleet.image_128
    
