# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date
   
class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    project_id = fields.Many2one('project.project', string='Project')
    state_id = fields.Many2one('res.country.state', compute='_compute_project_state')
    
    @api.depends('project_id')
    def _compute_project_state(self):
        for line in self:
            if line.project_id:
                line.state_id = line.project_id.address_id.state_id.id
            else:
                line.state_id = False
 
    #task_id = fields.Many2one('project.task', related='purchase_demand_id.task_id')
    
class StockMove(models.Model):
    _inherit = 'stock.move'
    
    project_id = fields.Many2one('project.project', string='Project', store=True, compute='_compute_all_project')
    state_id = fields.Many2one('res.country.state', string='State', store=True, compute='_compute_all_project')
    
    @api.depends('picking_id')
    def _compute_all_project(self):
        for line in self:
            if line.purchase_line_id.project_id.id:
                line.state_id = line.purchase_line_id.project_id.address_id.state_id.id
                line.project_id = line.purchase_line_id.project_id.id
            else:
                line.state_id = False
                line.project_id = False     
    
class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'
    
    project_id = fields.Many2one('project.project', string='Project', store=True, compute='_compute_all_project')
    state_id = fields.Many2one('res.country.state', string='State', store=True, compute='_compute_all_project')
    
    @api.depends('picking_id')
    def _compute_all_project(self):
        for line in self:
            if line.move_id.project_id.id:
                line.state_id = line.move_id.project_id.address_id.state_id.id
                line.project_id = line.move_id.project_id.id
            else:
                line.state_id = False
                line.project_id = False
    #task_id = fields.Many2one('project.task', related='move_id.task_id')

