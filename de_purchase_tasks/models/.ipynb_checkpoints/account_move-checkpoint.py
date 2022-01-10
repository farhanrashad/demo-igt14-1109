# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import fields, models, api, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    milestone_purchase_id = fields.Many2one('purchase.order', readonly=True, compute="_compute_allow_picking", stroe=True)
    allow_picking = fields.Boolean(string='Allow on Picking', compute="_compute_allow_picking")

    task_id = fields.Many2one('project.task', string='Milestone',store=True, compute="_compute_milestone")
    
    @api.depends('milestone_purchase_id')
    def _compute_milestone(self):
        picking = self.env['stock.picking']
        for move in self:
            picking = self.env['stock.picking'].search([('move_id','=',move.id)],limit=1)
            move.task_id = picking.task_id.id
            
    @api.depends('purchase_id')
    def _compute_allow_picking(self):
        ap = False
        purchase = self.env['purchase.order']
        for task in self.invoice_line_ids.purchase_order_id.task_ids:
            if task.allow_picking:
                ap = task.allow_picking
                purchase = task.purchase_id
        self.allow_picking = ap
        self.milestone_purchase_id = purchase.id
