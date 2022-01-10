from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ReportSparePenaltyWizard(models.TransientModel):
    _name = "report.spare.penalty.wizard"
    _description = 'Spare Penalty Wizard Report'
    
    in_date =  fields.Datetime(string='Inventory Date')
    
    product_ids = fields.Many2many('product.product', 'report_spare_penalty_product_rel', 'report_spare_penalty_id',
        'product_id', 'Products')
    categ_ids = fields.Many2many('product.category', 'report_spare_penalty_categ_rel', 'report_spare_penalty_id',
        'categ_id', 'Categories')
    location_ids = fields.Many2many('stock.location', 'report_spare_penalty_location_rel', 'report_spare_penalty_id',
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
            return self.env.ref('de_report_spare_parts_penalty.report_spare_penalty_report').report_action(self, data=data)
