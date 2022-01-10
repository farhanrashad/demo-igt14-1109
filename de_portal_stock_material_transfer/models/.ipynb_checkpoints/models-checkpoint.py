# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ProjectProject(models.Model):
    _inherit = 'project.project'

    
class ProjectTask(models.Model):
    _inherit = 'project.task'
    
    
class ResPartner(models.Model):
    _inherit = 'res.partner'    
    
class ResUsers(models.Model):
    _inherit = 'res.users'     