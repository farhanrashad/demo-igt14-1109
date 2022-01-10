from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ReportAccStatementWizard(models.TransientModel):
    _name = "report.acc.statement.wizard"
    _description = 'Account Statement Wizard Report'
    
    date_from =  fields.Date(string='Date From')
    date_to =  fields.Date(string='Date To')
    partner_ids = fields.Many2many('res.partner', 'report_acc_statement_partner_rel', 'report_acc_statement_id',
        'partner_id', 'Partners')
    
    def print_report(self):
        #order_ids = self.env['stock.transfer.order'].browse(self._context.get('active_ids',[]))
        data = {
            'date_from': self.date_from, 
            'date_to': self.date_to,
            'partner_ids': self.partner_ids.ids,
        }
        return self.env.ref('de_report_acc_statement.report_acc_statement_report').report_action(self, data=data)