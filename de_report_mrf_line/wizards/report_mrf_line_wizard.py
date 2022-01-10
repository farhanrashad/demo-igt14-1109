from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ReportMRFLineWizard(models.TransientModel):
    _name = "report.mrf.line.wizard"
    _description = 'MRF Line Wizard Report'
    
    from_date =  fields.Datetime(string='From Date')
    to_date =  fields.Datetime(string='To Date')
    
    product_ids = fields.Many2many('product.product', 'report_mrf_line_product_rel', 'report_mrf_line_id',
        'product_id', 'Products')
    categ_ids = fields.Many2many('product.category', 'report_mrf_line_categ_rel', 'report_mrf_line_id',
        'categ_id', 'Categories')    
    
    def print_report(self):
        data = {
            'from_date': self.from_date, 
            'to_date': self.to_date, 
            'product_ids': self.product_ids.ids,
            'categ_ids': self.categ_ids.ids,
        }
        return self.env.ref('de_report_mrf_line.report_mrf_line_report').report_action(self, data=data)
