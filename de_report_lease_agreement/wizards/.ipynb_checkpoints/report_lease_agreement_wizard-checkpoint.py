from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ReportSparePenaltyWizard(models.TransientModel):
    _name = "report.lease.agreement.wizard"
    _description = 'Lease Agreement Wizard Report'
    
    date_from =  fields.Date(string='Date From')
    date_to =  fields.Date(string='Date To')
        
    
    def print_report(self):
        #order_ids = self.env['stock.transfer.order'].browse(self._context.get('active_ids',[]))
        data = {
            'date_from': self.date_from, 
            'date_to': self.date_to,
        }
        return self.env.ref('de_report_lease_agreement.report_lease_agreement_report').report_action(self, data=data)
