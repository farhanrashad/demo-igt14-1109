from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ReportAccountAgingWizard(models.TransientModel):
    _name = "report.account.aging.wizard"
    _description = 'Account Aging Wizard Report'
    
    from_date =  fields.Date(string='From Date')
    to_date =  fields.Date(string='To Date')
    
    partner_ids = fields.Many2many('res.partner', 'report_account_aging_partner_rel', 'report_account_partner_id',
        'partner_id', 'Partners')
    
    def print_report(self):
        data = {
            'from_date': self.from_date, 
            'to_date': self.to_date, 
            'partner_ids': self.partner_ids.ids,
        }
        return self.env.ref('de_report_account_aging.report_account_aging_report').report_action(self, data=data)
