from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ReportInventoryValuationWizard(models.TransientModel):
    _name = "report.inventory.valuation.wizard"
    _description = 'Inventory Valuation Wizard Report'
    
    in_date =  fields.Datetime(string='Inventory Date')
    
    product_ids = fields.Many2many('product.product', 'report_inventory_valuation_product_rel', 'report_inventory_valuation_id',
        'product_id', 'Products')
    categ_ids = fields.Many2many('product.category', 'report_inventory_valuation_categ_rel', 'report_inventory_valuation_id',
        'categ_id', 'Categories')
    location_ids = fields.Many2many('stock.location', 'report_inventory_valuation_location_rel', 'report_inventory_valuation_id',
        'location_id', 'Locations')
    
    
    def print_report(self):
        #order_ids = self.env['stock.transfer.order'].browse(self._context.get('active_ids',[]))
        data = {
            'in_date': self.in_date, 
            'product_ids': self.product_ids.ids,
            'categ_ids': self.categ_ids.ids,
            'location_ids': self.location_ids.ids,
        }
        if self.in_date:
            return self.env.ref('de_report_inventory_valuation.report_inventory_valuation_report').report_action(self, data=data)
