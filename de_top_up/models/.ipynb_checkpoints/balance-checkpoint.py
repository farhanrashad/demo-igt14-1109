from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import date, timedelta, datetime


class TopUpBalance(models.Model):
    _name = 'topup.balance'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Top Up Balance'

    def unlink(self):
        for r in self:
            if r.state == 'confirmed' or r.state == 'cancelled' or r.state == 'closed':
                raise UserError(
                    "TOPUP_Balance records which are set to Confirmed/Cancelled/Closed can't be deleted!")
        return super(TopUpBalance, self).unlink()

    @api.model
    def create(self, values):
        if values.get('topup_balance', _('New')) == _('New'):
            values['topup_balance'] = self.env['ir.sequence'].next_by_code('topup.balance.topup_balance') or _('New')
        return super(TopUpBalance, self).create(values)

    crnt_year = fields.Integer(string="Current Year", default=datetime.now().year)
    topup_balance = fields.Char(string='Topup Balance', required=True, copy=False, readonly=True, index=True,
                                default=lambda self: _('New'))
    name = fields.Char('Name')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ], string='State', index=True, copy=False, default='draft')

    topup_balance_lines = fields.One2many('topup.balance.line', 'balance_id')

    def action_confirm(self):
        self.state = 'confirmed'

    def action_close(self):
        self.state = 'closed'

    def action_cancel(self):
        self.state = 'cancelled'
        
        
    @api.onchange('topup_balance')
    def _check_name(self):
        
        line_data = []
        topup_balance = self.env['topup.balance'].search([], limit=1)
        if topup_balance:
            for  balanceline in topup_balance.topup_balance_lines:
                line_data.append((0,0,{
                'operator': balanceline.operator,
                'opening_balance': balanceline.balance,
                'remarks': ' ',
                }))
        else:
            line_data.append((0,0,{
                'operator': 'mytel',
                'opening_balance': 0.0,
                'purchase_qty': 0.0,
                'distributed_qty': 0.0,
                'balance': 0.0,
                'remarks': ' ',
                }))
            line_data.append((0,0,{
                'operator': 'mpt',
                'opening_balance': 0.0,
                'purchase_qty': 0.0,
                'distributed_qty': 0.0,
                'balance': 0.0,
                'remarks': ' ',
                }))
            line_data.append((0,0,{
                'operator': 'ooredoo',
                'opening_balance': 0.0,
                'purchase_qty': 0.0,
                'distributed_qty': 0.0,
                'balance': 0.0,
                'remarks': ' ',
                }))
            line_data.append((0,0,{
                'operator': 'telenor',
                'opening_balance': 0.0,
                'purchase_qty': 0.0,
                'distributed_qty': 0.0,
                'balance': 0.0,
                'remarks': ' ',
                }))
        self.topup_balance_lines = line_data

    

    date = fields.Date(string="Date", default=fields.date.today())
    pre_period = fields.Char(string="Previous Period", compute='_compute_previous_period')
    curr_period = fields.Char(string="Current Period",  compute='_compute_previous_period')
    is_populated = fields.Boolean(string='Is Populated')
    balance_month = fields.Char(string="Month Balance", compute='_compute_previous_period')
    
    #_sql_constraints = [
     #   ('balance_month_uniq', 'unique(balance_month)',
      #      'Balance can be requested once in a Month')       
    #]

    
    
    
#     @api.constrains('date')
#     def _check_date(self):
#         if self.date and self.id:
#             balance_search1 = self.env['topup.balance']
#             current_year = datetime.strptime(str(self.date), '%Y-%m-%d').date().month
#             count = 0
#             for each_advance in self.env['topup.balance'].search([('id','=',self.id)]):
#                 if count == 1:
#                     existing_year = datetime.strptime(str(each_advance.date), '%Y-%m-%d').date().month

#                     if current_year == existing_year:
#                         raise UserError(('Error!', 'Balance can be requested once in a Month'))
#                 count = count + 1
    
    def _compute_previous_period(self):
        curr_date = fields.date.today()
        pre_date = fields.date.today() - timedelta(days=30)
        for record in self:
        	record.pre_period = pre_date.strftime('%B-%Y')
        	record.curr_period = curr_date.strftime('%B-%Y')
        	record.balance_month = record.date.strftime('%B-%Y')


class TopUpBalanceLine(models.Model):
    _name = 'topup.balance.line'
    _description = 'Top Up Balance model'

    balance_id = fields.Many2one('topup.balance', string='Balance Ref')

    operator = fields.Selection([('mytel', 'Mytel'), ('mpt', 'MPT'), ('ooredoo', 'Ooredoo'), ('telenor', 'Telenor')],
                                string="Operator")
    opening_balance = fields.Float('Opening Balance')
    purchase_qty = fields.Integer('Purchase Qty')
    distributed_qty = fields.Integer('Distributed Qty')
    balance = fields.Float('Balance', compute='_compute_amount')
    remarks = fields.Char('Remarks')

    @api.depends('opening_balance', 'purchase_qty', 'distributed_qty')
    def _compute_amount(self):
        total_amount = 0
        for line in self:
            if line.opening_balance or line.purchase_qty or line.distributed_qty:
                total_amount = (line.opening_balance + line.purchase_qty) - line.distributed_qty
            line.update({
                'balance': total_amount
            })
