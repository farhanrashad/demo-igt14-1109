from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta


class TicketAllocation(models.Model):
    _name = 'ticket.allocation'
    _description = 'Ticket Allocation Line'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']


    def unlink(self):
        for r in self:
            if r.state == 'refuse' or r.state == 'approved':
                raise UserError(
                    "Ticket Allocation records which are set to Refuse/Approved can't be deleted!")
        return super(TravelRequest, self).unlink()

    @api.model
    def create(self, values):
        if values.get('name', _('New')) == _('New'):
            values['name'] = self.env['ir.sequence'].next_by_code('ticket.allocation.seq') or _('New')
        return super(TicketAllocation, self).create(values)

    date = fields.Date(string="Ticket Date", default=fields.date.today())
    name = fields.Char('Name', required=True, copy=False, readonly=True, index=True,
                                 default=lambda self: _('New'))

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('refuse', 'Refuse'),
        ('approved', 'Approved'),
    ], string='State', index=True, readonly=True, tracking=True, copy=False, default='draft')
    user_id = fields.Many2one('res.users', string='Allocate User', default=lambda self: self.env.user)
    

    def action_submit(self):
        self.state = 'submitted'

    def action_refuse(self):
        self.state = 'refuse'

    def action_approve(self):
        self.state = 'approved'
        year_balance = self.env['travel.balance'].search([('crnt_year', '=', datetime.now().year)], limit=1)
        if year_balance:
            for  inn_line in self.allocation_line_ids:
                balance_line = self.env['travel.balance.line'].search([('id','=', year_balance.id), ('employee_id','=', inn_line.employee_id.id)], limit=1)
                if balance_line:
                    for line in year_balance.balance_line_ids:
                        if line.employee_id.id == balance_line.employee_id.id:
                            allocated_balance = line.allocated_balance + inn_line.amount
                            remaining_balance = allocated_balance - line.used_balance
                            line.allocated_balance = allocated_balance
                            line.remaining_balance =  remaining_balance
                        
                else:                              
                    line_vals = {
                        'balance_id': year_balance.id,
                        'employee_id': inn_line.employee_id.id,
                        'allocated_balance': inn_line.amount,
                        'remaining_balance': inn_line.amount,
                    }
                    balance_line = self.env['travel.balance.line'].create(line_vals)

        else:        
            travel_balance_line = []
            for line in self.allocation_line_ids:
                travel_balance_line.append((0,0,{
                'employee_id': line.employee_id.id,
                'allocated_balance': line.amount,
                'used_balance': 0.0,
                'remaining_balance': line.amount,
                }))

            ticket_vals = {
                'crnt_year': datetime.now().year,
                'name': self.env['ir.sequence'].next_by_code('ticket.balance.seq') if self.env['ir.sequence'].next_by_code('ticket.balance.seq') else   _('New'),
            }
            travel_balance = self.env['travel.balance'].create(ticket_vals)
            travel_balance.balance_line_ids = travel_balance_line


    def action_set_to_draft(self):
        self.state = 'draft'

    allocation_line_ids = fields.One2many('ticket.allocation.line', 'allocation_id')

    

   

class TicketAllocationLine(models.Model):
    _name = 'ticket.allocation.line'
    _description = 'Ticket Allocation Line'

    allocation_id = fields.Many2one('ticket.allocation')
    employee_id = fields.Many2one('hr.employee', string='Employee')
    amount = fields.Float(string='Allocate Amount')