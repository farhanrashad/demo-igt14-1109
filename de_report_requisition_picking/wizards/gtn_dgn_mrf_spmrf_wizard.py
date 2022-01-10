from odoo import api, fields, models, _
from odoo.exceptions import UserError


class GtnDgnMrfSpmrfWizard(models.TransientModel):
    _name = "gtn.dgn.mrf.spmrf.wizard"
    _description = 'Stock Transfer Material Wizard'
    
    src =  fields.Datetime(string='From',required=True)
    dest =  fields.Datetime(string='To',required=True)
    
    def generate_report(self):
        #order_ids = self.env['stock.transfer.order'].browse(self._context.get('active_ids',[]))
        data = {'start_date': self.src, 'end_date': self.dest}
        if self.src < self.dest:
            return self.env.ref('de_requisition_line_report.mrf_spmrf_report').report_action(self, data=data)
