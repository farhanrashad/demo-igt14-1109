# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import fields, models, api, _
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    task_id = fields.Many2one('project.task', string='Milestone', domain="[('purchase_id', '=', purchase_id),('allow_picking', '=', allow_picking),('stage_id.is_closed','=',True),('delivery_assigned','!=',True)]", copy=False)
    allow_picking = fields.Boolean(string='Allow on Picking', compute="_compute_allow_picking")
    purchase_project_id = fields.Many2one(related='task_id.purchase_project_id')
    
    @api.depends('purchase_id')
    def _compute_allow_picking(self):
        ap = False
        for task in self.purchase_id.task_ids:
            if task.allow_picking:
                ap = task.allow_picking
        self.allow_picking = ap
        
    @api.onchange('task_id')
    def _onchange_task_id(self):
        for picking in self:
            if picking.task_id.completion_percent > 0:
                for line in picking.move_ids_without_package.filtered(lambda r: r.project_id.id == picking.project_id.id):
                    line.quantity_done = (picking.task_id.completion_percent / 100) * line.purchase_line_id.product_qty
    
    #@api.constrains('task_id')
    #def _check_completion_percent(self):
    #    for picking in self:
    #        task_ids = self.env['project.task'].search([('project_id','=',picking.task_id.project_id.id),('id','!=',picking.task_id.id),('delivery_assigned','=',False)])
     #       for task in task_ids:
      #          if task.task_sequence < picking.task_id.task_sequence:
       #             raise UserError(_('You cannot select %s before %s') % (picking.task_id.name, task.name))
                
    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        qty = 0
        if self.purchase_id.task_ids:
            if not self.task_id and self.is_return == False:
                raise UserError(_('There is no milestone'))
            for move in self.move_ids_without_package.filtered(lambda r: r.project_id.id == self.task_id.purchase_project_id.id):
                qty = (self.task_id.completion_percent / 100) * move.purchase_line_id.product_qty
                if round(move.quantity_done,3) != round(qty,3) or move.quantity_done == 0:
                    raise UserError(_('Milestone quantity is wrong'))
                    #raise UserError(_('Milestone Quantity is wrong %s and %s') % (str(round(int(qty),2)), str(round(int(move.quantity_done),2)) ))
                    
        task_id = self.env['project.task'].search([('id','=',self.task_id.id)])
        for task in task_id:
            task.update({
                'delivery_assigned': True
            })
        return res
    
    def action_assign_milestone(self):
        #task_id = self.env['project.task'].search([('id','=',self.task_id.id)])
        task = self.env['project.task']
        qty = 0
        #tasks = self.env['project.task'].search([('purchase_id', '=', picking.purchase_id.id),('allow_picking', '=', picking.allow_picking),('stage_id.stage_category','=','close'),('submission_type','=','0'),('delivery_assigned','!=',True)])
        #for task in tasks.sorted(key=lambda r: r.sequence):
            #task_id = task
            #break
            #if not task_id:
                #raise UserError(_('There is no milestone for assignment'))
        #self.task_id = task_id.id        
        for picking in self:
            task = self.env['project.task'].search([('purchase_id', '=', picking.purchase_id.id),('allow_picking', '=', picking.allow_picking),('stage_id.stage_category','=','close'),('submission_type','=','0'),('delivery_assigned','!=',True)],limit=1)
            picking.update({
                'task_id': task.id,
                'project_id': picking.task_id.purchase_project_id.id,
            })
            if not task:
                raise UserError(_('There is no milestone for assignment'))
            
            if picking.task_id.completion_percent > 0:
                picking.sudo().action_assign()
                for move in picking.move_ids_without_package.filtered(lambda r: r.project_id.id == picking.task_id.purchase_project_id.id):
                    qty = (picking.task_id.completion_percent / 100) * move.purchase_line_id.product_qty
                    move.update({
                    #    'quantity_done': qty,
                    #    'product_uom_qty': qty,
                    })
                    if move.move_line_ids:
                        move.move_line_ids.unlink()
                    self.env['stock.move.line'].create({
                        'qty_done': qty,
                        'location_dest_id': picking.location_dest_id.id,
                        'location_id': picking.location_id.id,
                        'picking_id': picking.id,
                        'move_id': move.id,
                        'product_id': move.product_id.id,
                        'product_uom_id': move.product_uom.id,
                    })
                    
            
            #for move in picking.move_ids_without_package:
                
        


