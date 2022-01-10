# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    stock_refill_id = fields.Many2one('stock.refill', string='Stock Refill', )
    
class StockMove(models.Model):
    _inherit = 'stock.move'
    
    stock_refill_line_id = fields.Many2one('stock.refill.line', string='Refill Line', )
    
    
    
    

