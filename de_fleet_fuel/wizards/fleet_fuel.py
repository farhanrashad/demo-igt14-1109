# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime


class AddFuel(models.TransientModel):
    _name = "add.fuel"
    _description = "Add Fuel"

    liters = fields.Integer(string="Liters")
    price_per_liters = fields.Char(string="Price Per Liters")

    def add_fuel_wizard(self):
        model = self.env.context.get('active_model')
        rec = self.env[model].browse(self.env.context.get('active_id'))
        rec.write({
            'liters': rec.liters + self.liters,
            
        })
        self.env['fuel.history'].create({
            'rel_id': rec.id,
            'fuel_date': datetime.today().date(),
            'fuel_price': self.liters,
            'fuel_liters': self.price_per_liters,
        })
        rec.write({
            'last_filling_date': datetime.today().date(),
            'last_filling_amount': self.price_per_liters,
            'last_filling_price': self.price_per_liters,
            'last_added_fuel_date':datetime.today().date(),
        })
        return rec
    
    