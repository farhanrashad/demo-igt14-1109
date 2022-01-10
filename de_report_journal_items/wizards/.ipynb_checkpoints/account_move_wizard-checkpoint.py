import json

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime
import base64

class AccountMoveWizard(models.TransientModel):
    _name = "account.move.line.wizard"
    _description = "Account Move Line Wizard"

    date_from =  fields.Date(string='Date From')
    date_to =  fields.Date(string='Date To')
    
    account_ids = fields.Many2many('account.account')
    state = fields.Selection(selection=[
            ('draft', 'All Draft Entries'),
            ('posted', 'All Posted Entries'),
            ('all', 'All'),
        ], string='Target Moves', default='draft')
    

    @api.depends('doe')
    def _compute_date(self):
        for line in self:
            if line.doe:
                line.update({
                  'date_today': line.doe.strftime("%Y%m%d")
                })
            else:
                line.update({
                  'date_today': datetime.today().strftime("%Y%m%d")
                })
            

    
    
    def print_txt_report(self):
        data_val = ''
        vals = ''
        filename = "journal_items.csv"
        file_ = open(filename + str(), 'w')
        account_move_lines = self.env['account.move.line']
        domain = [('date', '>=', self.date_from),('date','<=', self.date_to)]
        if self.account_ids:
            #domain += [('account_id','in',[self.account_ids.id])]
            account_ids = tuple([acc_id.id for acc_id in self.account_ids])
            domain += [('account_id','in',account_ids)]
            
        if self.state == 'all':
            domain += [('parent_state','in',['draft','posted'])]
        elif self.state == 'draft':
            domain += [('parent_state','=','draft')]
        elif self.state == 'posted':
            domain += [('parent_state','=','posted')]
            
        #if self.account_ids:
        #    account_move_lines = self.env['account.move.line'].search([('date', '>=', self.date_from),('date','<=', self.date_to),('account_id','in',self.account_ids)])
        account_move_lines = self.env['account.move.line'].search(domain)
        #file_data = 'ID,Reference,Name,Creation Date,Effective Date,Journal,Number,Period' + "\n"
        file_data = 'ID,Reference,Name,Creation Date,Effective Date,Journal/Name,Journal Entry/Number,Period/Name,Account/Code,Account Name,Account/Parent/Name,Account Type,Amount Currency,Debit,Credit,Analytic Account,Site,Partner,Employee,Status,Internal Notes,Invoice/ID,Invoice/Number,Invoice/Type,Invoice/Source Document,Invoice/Supplier,Invoice/Due Date,Reconcile No.' + "\n"
        file_.write(file_data)
        for line in account_move_lines:
            file_data = str(line.id)
            if line.ref:
                file_data += ',' + '"' + str(line.ref) + '"'
            else:
                file_data += ','
            if line.name:
                file_data += ',' + '"' + str(line.name) + '"'
            else:
                file_data += ','
            if line.create_date:
                file_data += ',' + line.create_date.strftime("%d/%m/%Y")
            else:
                file_data += ','
            if line.date:
                file_data += ',' + line.date.strftime("%d/%m/%Y")
            else:
                file_data += ','
            if line.journal_id.id:
                file_data += ',' + line.journal_id.name
            else:
                file_data += ','
            if line.move_id.name:
                file_data += ',' + line.move_id.name
            else:
                file_data += ','
            if line.account_period:
                file_data += ',' + line.account_period
            else:
                file_data += ','
            file_data += ',' + line.account_id.code + ',' + line.account_id.name
            if line.account_id.group_id:
                file_data += ',' + line.account_id.group_id.name
            else:
                file_data += ','
            if line.account_id.user_type_id:
                file_data += ',' + line.account_id.user_type_id.name
            else:
                file_data += ','
                
            file_data += ',' + str(line.amount_currency) + ',' + str(line.debit) + ',' + str(line.credit)
            if line.analytic_account_id.id:
                file_data += ',' + line.analytic_account_id.name
            else:
                file_data += ','
            if line.project_id.id:
                file_data += ',' + '"' + line.project_id.name + '"'
            else:
                file_data += ','
            if line.partner_id.id:
                file_data += ',' + '"' + line.partner_id.name + '"'
            else:
                file_data += ', '
            if line.employee_id.id:
                file_data += ',' + '"' + line.employee_id.name + '"'
            else:
                file_data += ', '
            
            file_data += ',' + str(line.parent_state) + ', '
            file_data += ',' + str(line.move_id.id) + ',' + str(line.move_id.name) + ',' + str(line.move_id.move_type)
            if line.move_id.invoice_origin:
                file_data += ',' + line.move_id.invoice_origin
            else:
                file_data += ','
            if line.move_id.partner_id.id:
                file_data += ',' + '"' + line.move_id.partner_id.name + '"'
            else:
                file_data += ','
            if line.move_id.invoice_date_due:
                file_data += ',' + line.move_id.invoice_date_due.strftime("%d/%m/%Y")
            else:
                file_data += ','
            if line.full_reconcile_id.id:
                file_data += ',' + line.full_reconcile_id.name
            else:
                file_data += ','
                
            #file_data = str(line.id) + ',' + str(line.ref) + ',' + str(line.create_date) + ',' + str(line.date) + ',' + str(line.journal_id.name) + "\n"

            data_val = str(file_data)
            file_.write(data_val)
            file_.write("\n")
        file_.close()
        
        with open('journal_items.csv') as f:
            read_file = f.read()
            attachment_vals = {
                    'name': filename,
                    'type': 'binary',
                    'datas': base64.b64encode(read_file.encode('utf8')),
                    'res_model': 'account.move.line',
            }
            attach_file = self.env['ir.attachment'].create(attachment_vals)
            download_url = '/web/content/' + str(attach_file.id) + '?download=True'
#             Return so it will download in your system
            return {
                    "type": "ir.actions.act_url",
                    "url": str(download_url),
                    "target": "new",
            }
        
        

