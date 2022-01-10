from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta


class TicketBalance(models.Model):
    _name = 'travel.balance'
    _description = 'Travel Balance'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']


#     def unlink(self):
#         for r in self:
#             raise UserError(
#                     "Ticket Balance can't be deleted!")
#         return super(TicketBalance, self).unlink()

    
    @api.model
    def create(self, values):
        if values.get('name', _('New')) == _('New'):
            values['name'] = self.env['ir.sequence'].next_by_code('ticket.balance.seq') or _('New')
        return super(TicketBalance, self).create(values)

    crnt_year = fields.Char(string="Current Year", default=datetime.now().year)
    name = fields.Char('Name', required=True, copy=False, readonly=True, index=True,
                                 default=lambda self: _('New'))

    

    balance_line_ids = fields.One2many('travel.balance.line', 'balance_id')

   

class TicketBalanceLine(models.Model):
    _name = 'travel.balance.line'
    _description = 'Travel Balance Line'

    balance_id = fields.Many2one('travel.balance')
    employee_id = fields.Many2one('hr.employee', string='Employee')
    allocated_balance = fields.Float(string="Allocated Balance")
    used_balance = fields.Float(string="Used Balance")
    remaining_balance = fields.Float(string="Remaining Balance")
