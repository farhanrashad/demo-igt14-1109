from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ReportInventoryValuationWizard(models.TransientModel):
    _name = "report.stock.move.wizard"
    _description = 'Stock Move Wizard Report'
    
    in_date =  fields.Datetime(string='Inventory Date')
    
    product_ids = fields.Many2many('product.product', 'report_stock_move_product_rel', 'report_stock_move_id',
        'product_id', 'Products')
    categ_ids = fields.Many2many('product.category', 'report_stock_move_categ_rel', 'report_stock_move_id',
        'categ_id', 'Categories')
    location_ids = fields.Many2many('stock.location', 'report_stock_move_location_rel', 'report_stock_move_id',
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
            return self.env.ref('de_report_stock_move.report_stock_move_report').report_action(self, data=data)
