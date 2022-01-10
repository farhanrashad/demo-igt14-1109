# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import UserError

class VehicleFleetWizard(models.TransientModel):
    _name = 'force.close.wizard'
    _description = 'Vehicle Fleet Selection'
    
    reason = fields.Char( string="Reason", required=True)
    
    
    
    def action_force_close(self):
        model = self.env.context.get('active_model')
        rec = self.env[model].browse(self.env.context.get('active_id'))
        
        rec.is_force_close = True
        
        rec.write({
            'state': 'done', 
        })
        rec.reason = self.reason
        
#         rec.requested_model = self.assign_fleet.id
#         rec.state ='assigned'
#         rec.assign_by = self.env.user
#         rec.assign_date = datetime.today()
#         rec.image_fleet_request = self.assign_fleet.image_128
# is_force_close