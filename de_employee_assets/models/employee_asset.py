from odoo import api, fields, models, _


class EmployeeAssets(models.Model):
    _name = 'employee.asset'
    _description = 'Employee Asset'

    name = fields.Char('Asset Name')
    code = fields.Char('Asset Code')
    serial = fields.Char('Serial Number')
    description = fields.Text('Description')
    
    
    
class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    asset_lines = fields.One2many('employee.asset.line', 'employee_id')
    tb_lines = fields.One2many('employee.teambuilding.line', 'employee_id')
    incident_lines = fields.One2many('employee.incident.line', 'employee_id')
    
class EmployeeAssetsLine(models.Model):
    _name = 'employee.asset.line'
    _description = 'Employee Asset Line'

    employee_id = fields.Many2one('hr.employee')
    asset_id = fields.Many2one('employee.asset')
    code = fields.Char('Asset Code', related='asset_id.code')
    serial = fields.Char('Serial Number', related='asset_id.serial')
    delivery_date = fields.Date('Delivery Date')
    return_date = fields.Date('Return Date')
    comment = fields.Text('Comment')
    
    
class EmployeeTeamBuilding(models.Model):
    _name = 'employee.teambuilding'
    _description = 'Employee Team Building'

    name = fields.Char('Activty Name')
    code = fields.Char('Activity Code')
    description = fields.Text('Description')
    


class EmployeeTeamBuildingLine(models.Model):
    _name = 'employee.teambuilding.line'
    _description = 'Employee Team Building Line'

    employee_id = fields.Many2one('hr.employee')
    tb_id = fields.Many2one('employee.teambuilding')
    code = fields.Char('Activity Code', related='tb_id.code')
    winner = fields.Selection([
        ('first', 'Winner'),
        ('runnerup', 'Runner-Up'),
        ], string='Position', index=True, copy=False, )
    comment = fields.Text('Comment')

    
class EmployeeIncident(models.Model):
    _name = 'employee.incident'
    _description = 'Employee Incident'

    name = fields.Char('Activty Name')
    description = fields.Text('Description')
    


class EmployeeIncidentLine(models.Model):
    _name = 'employee.incident.line'
    _description = 'Employee Incident Line'

    employee_id = fields.Many2one('hr.employee')
    incident_id = fields.Many2one('employee.incident')
    comment = fields.Text('Comment')
    date = fields.Date(string='Date')


