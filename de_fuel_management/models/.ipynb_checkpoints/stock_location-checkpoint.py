from odoo import models, fields, api, _


class StockLocation(models.Model):
    _inherit = 'stock.location'
    
    is_refilling = fields.Boolean(string="Refilling Point")
    location_type = fields.Selection(selection=[
            ('normal', 'Normal'),
            ('refill', 'Refilling Storage/Tank'),
        ], string='Location Type', index=True, 
        default="normal", change_default=True)
    product_id = fields.Many2one('product.product', string="Product")
    uom_id = fields.Many2one('uom.uom', related='product_id.uom_id')
    storage_capacity = fields.Float(string="Storage Capacity")
    
    
    

