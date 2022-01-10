from odoo import api, fields, models, _


class AppraisalProject(models.Model):
    _inherit = 'project.project'
    is_appraisal = fields.Boolean(string='Appraisal')


class GoalAppraisal(models.Model):
    _inherit = 'project.task'
    goal_id = fields.Many2one('hr.appraisal.goal', string='Goal')


class AppraisalKRA(models.Model):
    _name = "hr.appraisal.kra"
    _description = "Employee Performance KRA"

    name = fields.Char(string="Name", required=True)
    weightage = fields.Float(string="Weightage")


class EnhanceGoalPage(models.Model):
    _inherit = 'hr.appraisal.goal'

    target = fields.Float(string='Target')
    kra_id = fields.Many2one('hr.appraisal.kra', string='KRA')
    appraisal_goal_tasks_lines = fields.One2many('hr.appraisal.goal.tasks', 'appraise')
    appraisal_id = fields.Many2one('hr.appraisal')


class AppraisalGoalTasks(models.Model):
    _name = "hr.appraisal.goal.tasks"
    _description = "Appraisal Goal Tasks"

    appraise = fields.Many2one('hr.appraisal.goal')

    task_id = fields.Many2one('project.task', string='Tasks')
    task_deadline = fields.Date(related='task_id.date_deadline')
    task_status = fields.Many2one(related='task_id.stage_id')


class EnhanceKRAPage(models.Model):
    _inherit = 'hr.appraisal'

    #     appraisal_kra_lines_ids = fields.One2many('hr.appraisal.goal', 'appraisal_id')
    appraisal_kra_goal_ids = fields.One2many('hr.appraisal.kra.goal', 'appraisal_kra_id')


class AppraisalTree(models.Model):
    _name = "hr.appraisal.kra.goal"
    _description = "Appraisal Goal and KRa"

    appraisal_kra_id = fields.Many2one('hr.appraisal', )
    goal_id = fields.Many2one('hr.appraisal.goal', string='Goal')
    kra_id = fields.Many2one(related='goal_id.kra_id')
    level_progress = fields.Selection(related='goal_id.progression')

