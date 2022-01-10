import json

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime
import base64



class PayslipBatch(models.TransientModel):
    _name = "pay.slip.batch"
    _description = "Payslip Batch Wizard"

    contract_type = fields.Selection([('local', 'Local'),('expats', 'Expats')], string='Contract Type')
    doe = fields.Date(string='Date of Execution')
    debit_ac_no = fields.Char(string='Debit A/C No.')
    currency = fields.Many2one('res.currency', string='Currency')
    batch_id = fields.Many2one('hr.payslip.run')
    date_today = fields.Date(default=datetime.today())
    
    def print_report(self):
        print('ID: ', self.id)
        datas = {
            'contract_type': self.contract_type,
            'doe': self.doe,
            'debit_ac_no': self.debit_ac_no,
            'currency': self.currency.id,
            'id': self.batch_id.id,
        }
        return self.env.ref('de_payslip_batch_report.payslip_batch_report').report_action(self, data=datas)
    
    
    
    def print_txt_report(self):
        data_val = ''
        vals = ''
        filename = "batch.txt"
        file_ = open(filename + str(), 'w')
        payslips = self.env['hr.payslip'].search([('payslip_run_id', '=', self.batch_id.id)])
        file_data = '' 
        for payslip in payslips:
            self.env.cr.execute("""select rpad(concat('',p.number),16,' '), rpad(concat('',ps.debit_ac_no),14,' '), rpad(concat('',c.name,ps.date_today),14,' '),rpad(concat('',p.normal_wage),15,' '), rpad(concat('NNOUR',bank.acc_number),40,' '),rpad(concat('',c.name,bank.acc_holder_name),38,' '),rpad(concat('',partner.street,partner.street2,partner.city),70,' '),rpad(concat('',country.name),35,' '),rpad(concat(bbank.name,bbank.street),105,' '),rpad(concat('',bcountry.name),186,' '),rpad(concat('',p.name),350,' '),rpad(concat('',emp.work_email),538,' '),rpad(concat('',bbank.bic),503,' ')
            from pay_slip_batch as ps 
            left join hr_payslip as p on ps.batch_id=p.payslip_run_id
            left join hr_employee as emp on p.employee_id=emp.id
            left join res_partner as partner on emp.address_home_id=partner.id
            left join res_country as country on partner.country_id=country.id
            left join res_partner_bank as bank on emp.bank_account_id=bank.id
            left join res_bank as bbank on bank.bank_id=bbank.id
            left join res_country as bcountry on bbank.country=bcountry.id
            left join res_currency as c on ps.currency=c.id
            where p.id=%s and ps.id=%s""" % (payslip.id, self.id))                         
            payslip_vals = self.env.cr.fetchall()
            count = 0
            for line_vals in  payslip_vals:
                slip_line = ''
                for payslip_line in line_vals:
                    slip_line += payslip_line    
                file_data += 'TT' + '  ' + str(slip_line) + "\n"
        data_val = str(file_data)
        file_.write(data_val)
        file_.write("\n")
        file_.close()
        
        with open('batch.txt') as f:
            read_file = f.read()
            attachment_vals = {
                    'name': filename,
                    'type': 'binary',
                    'datas': base64.b64encode(read_file.encode('utf8')),
                    'res_id': self.batch_id.id,
                    'res_name': self.batch_id.name,
                    'res_model': 'hr.payslip.run',
            }
            attach_file = self.env['ir.attachment'].create(attachment_vals)
            download_url = '/web/content/' + str(attach_file.id) + '?download=True'
#             Return so it will download in your system
            return {
                    "type": "ir.actions.act_url",
                    "url": str(download_url),
                    "target": "new",
            }
        
        

