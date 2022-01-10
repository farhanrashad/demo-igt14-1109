from odoo import api, fields, models, _


class AppraisalProject(models.Model):
    _inherit = 'project.project'
    # foreign key concept
    is_appraisal = fields.Boolean(string='Appraisal')


class GoalAppraisal(models.Model):
    _inherit = 'project.task'
    goal_id = fields.Many2one('hr.appraisal.goal', string='Goal Appraisal')


class AppraisalKRA(models.Model):
    _name = "hr.appraisal.kra"
    _description = "Employee Performance KRA"

    name = fields.Char(string="Name", required=1)
    weightage = fields.Float(string="Weightage")

class AppraisalGoalTasks(models.Model):
    _name = "hr.appraisal.goal.tasks"
    _description = "Appraisal Goal Tasks"

    task_ids = fields.Integer(string='Tasks')

#     related
#     field
#     task_deadline = fields.

#     related
#     field
#     task
#     status

