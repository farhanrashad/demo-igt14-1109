from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ReportTransferPickingWizard(models.TransientModel):
    _name = "report.transfer.picking.wizard"
    _description = 'Transfer Picking Wizard Report'
    
    from_date =  fields.Datetime(string='From Date')
    to_date =  fields.Datetime(string='To Date')
    
    product_ids = fields.Many2many('product.product', 'report_transfer_picking_product_rel', 'report_transfer_picking_id',
        'product_id', 'Products')
    categ_ids = fields.Many2many('product.category', 'report_transfer_picking_categ_rel', 'report_transfer_picking_id',
        'categ_id', 'Categories')    
    
    def print_report(self):
        data = {
            'from_date': self.from_date, 
            'to_date': self.to_date, 
            'product_ids': self.product_ids.ids,
            'categ_ids': self.categ_ids.ids,
        }
        return self.env.ref('de_report_transfer_picking.report_transfer_picking_report').report_action(self, data=data)
