# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ProjectProject(models.Model):
    _inherit = 'project.project'
    
#     hoto_submission_date = fields.Date(string='Hoto Submission Date')

    
class ProjectTask(models.Model):
    _inherit = 'project.task'
    
    
class ResPartner(models.Model):
    _inherit = 'res.partner'    
    
class ResUsers(models.Model):
    _inherit = 'res.users'     