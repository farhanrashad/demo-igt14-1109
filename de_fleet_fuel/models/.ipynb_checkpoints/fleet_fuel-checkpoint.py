# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime

class FleetFuel(models.Model):
    
    _name = 'fleet.fuel'
    _description = 'this table is relevent to fleet fuel'
    _rec_name = 'name'
    
    
    name = fields.Char(string='Name')
    location = fields.Char(string='Location')
    last_clean_date = fields.Date(string='Last Clean Date')
    capacity = fields.Char(string='Capacity')
    liters = fields.Integer(string='Liters')
    average_price = fields.Float(string='Average Price', compute='average_price_fuel')
    last_filling_date = fields.Date(string='Last Filling Date')
    last_filling_amount = fields.Char(string='Last Filling Amount')
    last_filling_price = fields.Char(string='Last Filling Price')
    total_filling_fuel = fields.Char(string='Total Filling Fuel')
    last_added_fuel_date = fields.Date(string='Last Added Fuel Date')
    history_ids = fields.One2many('fuel.history', 'rel_id')
    
    @api.onchange('history_ids')
    def average_price_fuel(self):
        avg = 0
        if self.history_ids:
            sum = 0
            count = 0
            for rec in self.history_ids:
                count = count + 1
                sum = sum + rec.fuel_price
            avg = sum  / count
        self.average_price = avg
    
    
class VehicleFuelLog(models.Model):
    
    _name = 'vehicle.fuel.log'
    _description = 'this table is relevent to vehicle fuel logs'
    _rec_name = 'vehicle'
    
    
    vehicle = fields.Many2one('fleet.vehicle', string='Vehicle')
    employee = fields.Many2one('hr.employee', string='User')
    department_id = fields.Many2one('hr.department', related='employee.department_id')
    liter = fields.Integer(string='Liter')
    fuel = fields.Many2one('fleet.fuel', string='Fuel')
    price_per_liter = fields.Integer(string='Price Per Liter')
    total_price = fields.Integer(string='Total Price', compute='total_price_fuel', store=True)
    odometer_value = fields.Char(string='Odometer Value')
    previous_odometer_reading = fields.Char(string='Previous Odometer Reading')
    date = fields.Date(string='Date')
    invoice_reference = fields.Char(string='Invoice Reference')
    vendor = fields.Many2one('res.partner', string='Vendor')
    purchaser = fields.Many2one('res.partner', string='Purchaser')
    
    def total_price_fuel(self):
        m_liter = self.liter * self.price_per_liter
        self.total_price = m_liter
        
    @api.onchange('vehicle')
    def _get_employee(self):
        if self.vehicle:
            current_user = self.env['fleet.vehicle.user.log'].search([('vehicle_id','=',self.vehicle.id)],limit=1)
            if current_user:
                self.update({
                    'employee': current_user.user_id.id
                })
        
    
class FuelHistory(models.Model):
    
    _name = 'fuel.history'
    
    rel_id = fields.Many2one('fleet.fuel')
    fuel_date = fields.Date(string='Date')
    fuel_price = fields.Float(string='Price')
    fuel_liters = fields.Char(string='Liters')


class FleetVehicleModel(models.Model):
    
    _inherit = 'fleet.vehicle.model'
    
    vehicle_type = fields.Selection([
        ('1', 'PICKUP (4x4) (L) (DOUBLE CAB)'),
        ('2', 'PICKUP (4x4) (R) (DOUBLE CAB)'),
        ('3', 'PICKUP (4x4) (L) (KING CAB)'),
        ('4', 'PICKUP (4x4) (R) (KING CAB)'),
        ('5', 'SUV'),
        ('6', 'SALOON'),
        ('7', 'Car'),
        ('8', 'Bike'),
    ], string='Vehicle Type', index=True, copy=False, default='7')


class FleetVehicleUserLog(models.Model):
    _name = "fleet.vehicle.user.log"
    _description = "User history on a vehicle"
    _order = "create_date desc, date_start desc"

    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle", required=True)
    user_id = fields.Many2one('hr.employee', string="User", required=True)
    department_id = fields.Many2one('hr.department', related= "user_id.department_id", string= 'Department')
    date_start = fields.Date(string="Start Date")
    date_end = fields.Date(string="End Date")
    
    log_users = fields.One2many('fleet.vehicle.user.log', 'vehicle_id', string='User Logs')
    attachment_id = fields.Many2many('ir.attachment', relation="files_rel_user_log",
                                            column1="doc_id",
                                            column2="attachment_id",
                                            string="Attachment")
    
class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"   
    
    
    
    user_log_count = fields.Integer(compute="_compute_user_log", string="User History Count")
    fuel_log_count = fields.Integer(compute="_compute_fuel_log", string="Fuel Log Count")
    
    
    def open_user_logs(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'User Logs',
            'view_mode': 'tree',
            'res_model': 'fleet.vehicle.user.log',
            'domain': [('vehicle_id', '=', self.id)],
            'context': {'default_vehicle_id': self.id}
        }
    
    def _compute_user_log(self):
        UserLog = self.env['fleet.vehicle.user.log']
        for record in self:
            record.user_log_count = self.env['fleet.vehicle.user.log'].search_count([('vehicle_id', '=', record.id)])
            
            
            
    def open_fuel_logs(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Fuel Logs',
            'view_mode': 'tree',
            'res_model': 'vehicle.fuel.log',
            'domain': [('vehicle', '=', self.id)],
            'context': {'default_vehicle': self.id}
        }
    
    def _compute_fuel_log(self):
        FuelLog = self.env['vehicle.fuel.log']
        for record in self:
            record.fuel_log_count = self.env['vehicle.fuel.log'].search_count([('vehicle', '=', record.id)])