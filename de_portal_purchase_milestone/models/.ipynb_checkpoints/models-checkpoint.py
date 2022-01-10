# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
       
class ProjectTask(models.Model):
    _inherit = 'project.task' 
    
    is_purchase_attachment = fields.Boolean(string='Purchase Attachment')
    
    
class ProjectProject(models.Model):
    _inherit = 'project.project'     
