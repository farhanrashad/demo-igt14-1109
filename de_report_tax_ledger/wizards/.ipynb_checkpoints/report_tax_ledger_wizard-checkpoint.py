from odoo import api, fields, models, _
from odoo.exceptions import UserError


class taxLedgerWizard(models.TransientModel):
    _name = "tax.ledger.wizard"
    _description = 'Tax Ledger Wizard'
    
    from_date =  fields.Date(string='From Date')
    to_date =  fields.Date(string='To Date')
    
    account_ids = fields.Many2many('account.account')
    state = fields.Selection(selection=[
            ('draft', 'All Draft Entries'),
            ('posted', 'All Posted Entries'),
            ('all', 'All'),
        ], string='Target Moves', default='draft')
    
    def print_report(self):
        data = {
            'from_date': self.from_date, 
            'to_date': self.to_date,
            'account_ids': self.account_ids.ids,
            'state': self.state,
        }
        
        return self.env.ref('de_report_tax_ledger.tax_ledger_report').report_action(self, data=data)
