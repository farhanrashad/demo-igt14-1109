# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date
from dateutil.relativedelta import relativedelta

import json
from lxml import etree

class CustomEntry(models.Model):
    _inherit = 'account.custom.entry'
    
    has_spare_penalty = fields.Selection(related="custom_entry_type_id.has_spare_penalty")
    
    
    
class CustomEntryLine(models.Model):
    _inherit = 'account.custom.entry.line'
    
    sp_location_id = fields.Many2one('stock.location', string='Location')
    sp_asset_id = fields.Many2one('account.asset', string='Asset')
    sp_product_id = fields.Many2one('product.product', string='Product')
    sp_life_time = fields.Integer(string='Life Time')
    sp_date_onair = fields.Date(string='On Air Date')
    sp_date_delivery_deadline = fields.Date(string='Delivery Deadline')
    sp_date_return_deadline = fields.Date(string='Return Deadline')
    sp_date_delivered = fields.Date(string='Date Delivered')
    sp_date_returned = fields.Date(string='Date Returned')
    sp_used_life = fields.Integer(string='Used Life')
    sp_cost = fields.Float(string='Cost')
    sp_quantity = fields.Float(string='Quantity')
    sp_back_charges = fields.Float(string='Back Charges')
    sp_remarks = fields.Char(string='Remarks')
    