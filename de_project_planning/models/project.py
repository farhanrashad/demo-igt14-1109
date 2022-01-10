# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date

class ProjectSiteType(models.Model):
    _name = 'project.site.type'
    _description = 'Site Type'
    
    name = fields.Char('Site Type')

class ProjectProject(models.Model):
    _inherit = 'project.project'
    
    allow_site_planning = fields.Boolean(string='Site Planning')
    job_count = fields.Integer(compute='_compute_job_count', string="Task Count")
    project_notes_count = fields.Integer(compute='_compute_notes_count', string="Notes Count")
    
    requisition_count = fields.Integer(compute='_compute_requisition_count', string="Requisition Count")
    purchase_count = fields.Integer(compute='_compute_purchase_count', string="Purchase Count")
    bill_count = fields.Integer(compute='_compute_bill_count', string="Bill Count")
    invoice_count = fields.Integer(compute='_compute_invoice_count', string="Invoice Count")
    delivery_count = fields.Integer(compute='_compute_delivery_count', string="Delivery Count")
    stock_receipt_count = fields.Integer(compute='_compute_stock_receipt_count', string="Receipt Count")
    stock_transfer_count = fields.Integer(compute='_compute_stock_transfer_count', string="Transfer Count")
    
    site_type_id = fields.Many2one('project.site.type',string='Site Type', change_default=True,)
    address_id = fields.Many2one('res.partner',string='Address')
    state_id = fields.Many2one('res.country.state', related='address_id.state_id')
    location_id = fields.Many2one('stock.location',string='Stock Location', domain="[('site_location', '=', True)]")

    def _compute_requisition_count(self):
        Requisition = self.env['purchase.requisition']
        can_read = Requisition.check_access_rights('read', raise_exception=False)
        for project in self:
            project.requisition_count = can_read and Requisition.search_count([('line_ids.project_id', '=', project.id)]) or 0
            
    def action_project_requisition(self):
        self.ensure_one()
        requisitions = self.env['purchase.requisition'].search([('line_ids.project_id', 'in', self.ids)])
        action = self.env["ir.actions.actions"]._for_xml_id("purchase_requisition.action_purchase_requisition")
        action["context"] = {
            "create": False,
            #"default_move_type": "out_invoice"
        }
        if len(requisitions) > 1:
            action['domain'] = [('id', 'in', requisitions.ids)]
        elif len(requisitions) == 1:
            form_view = [(self.env.ref('purchase_requisition.view_purchase_requisition_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = requisitions.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
    
    def _compute_purchase_count(self):
        Purchase = self.env['purchase.order']
        can_read = Purchase.check_access_rights('read', raise_exception=False)
        for project in self:
            project.purchase_count = can_read and Purchase.search_count([('order_line.project_id', '=', project.id)]) or 0
            
    def action_project_purchase(self):
        self.ensure_one()
        purchases = self.env['purchase.order'].search([('order_line.project_id', 'in', self.ids)])
        action = self.env["ir.actions.actions"]._for_xml_id("purchase.purchase_form_action")
        action["context"] = {
            "create": False,
            #"default_move_type": "out_invoice"
        }
        if len(purchases) > 1:
            action['domain'] = [('id', 'in', purchases.ids)]
        elif len(purchases) == 1:
            form_view = [(self.env.ref('purchase.purchase_order_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = purchases.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
    
    def _compute_bill_count(self):
        Invoice = self.env['account.move']
        can_read = Invoice.check_access_rights('read', raise_exception=False)
        for project in self:
            project.bill_count = can_read and Invoice.search_count([('invoice_line_ids.project_id', '=', project.id),('move_type','in',['in_invoice','in_refund'])]) or 0
            
    def action_project_bill(self):
        self.ensure_one()
        invoices = self.env['account.move'].search([('invoice_line_ids.project_id', 'in', self.ids),('move_type','in',['in_invoice','in_refund'])])
        action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_in_invoice_type")
        action["context"] = {
            "create": False,
            "default_move_type": "in_invoice"
        }
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            form_view = [(self.env.ref('account.view_move_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = invoices.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
    
    def _compute_invoice_count(self):
        Invoice = self.env['account.move']
        can_read = Invoice.check_access_rights('read', raise_exception=False)
        for project in self:
            project.invoice_count = can_read and Invoice.search_count([('invoice_line_ids.project_id', '=', project.id),('move_type','in',['out_invoice','out_refund'])]) or 0
            
    def action_project_invoice(self):
        self.ensure_one()
        invoices = self.env['account.move'].search([('invoice_line_ids.project_id', 'in', self.ids),('move_type','in',['out_invoice','out_refund'])])
        action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_out_invoice_type")
        action["context"] = {
            "create": False,
            "default_move_type": "out_invoice"
        }
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            form_view = [(self.env.ref('account.view_move_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = invoices.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
    
    def _compute_delivery_count(self):
        Picking = self.env['stock.picking']
        can_read = Picking.check_access_rights('read', raise_exception=False)
        for project in self:
            project.delivery_count = can_read and Picking.search_count([('move_lines.project_id', '=', project.id),('picking_type_code','=','outgoing')]) or 0
            
    def action_project_delivery(self):
        self.ensure_one()
        pickings = self.env['stock.picking'].search([('move_ids_without_package.project_id', 'in', self.ids),('picking_type_code','=','outgoing')])
        action = self.env["ir.actions.actions"]._for_xml_id("stock.action_picking_form")
        action["context"] = {
            "create": False,
            "default_picking_type_code": "outgoing"
        }
        if len(pickings) > 1:
            action['domain'] = [('id', 'in', pickings.ids)]
        elif len(pickings) == 1:
            form_view = [(self.env.ref('stock.view_picking_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = pickings.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
    
    def _compute_stock_receipt_count(self):
        Picking = self.env['stock.picking']
        can_read = Picking.check_access_rights('read', raise_exception=False)
        for project in self:
            project.stock_receipt_count = can_read and Picking.search_count([('move_lines.project_id', '=', project.id),('picking_type_code','=','incoming')]) or 0
            
    def action_project_stock_receipt(self):
        self.ensure_one()
        pickings = self.env['stock.picking'].search([('move_lines.project_id', 'in', self.ids),('picking_type_code','=','incoming')])
        action = self.env["ir.actions.actions"]._for_xml_id("stock.action_picking_form")
        action["context"] = {
            "create": False,
            "default_picking_type_code": "incoming"
        }
        if len(pickings) > 1:
            action['domain'] = [('id', 'in', pickings.ids)]
        elif len(pickings) == 1:
            form_view = [(self.env.ref('stock.view_picking_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = pickings.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
    
    def _compute_stock_transfer_count(self):
        Picking = self.env['stock.picking']
        can_read = Picking.check_access_rights('read', raise_exception=False)
        for project in self:
            project.stock_transfer_count = can_read and Picking.search_count([('move_lines.project_id', '=', project.id),('picking_type_code','=','internal')]) or 0
            
    def action_project_stock_transfer(self):
        self.ensure_one()
        pickings = self.env['stock.picking'].search([('move_lines.project_id', 'in', self.ids),('picking_type_code','=','internal')])
        action = self.env["ir.actions.actions"]._for_xml_id("stock.action_picking_form")
        action["context"] = {
            "create": False,
            "default_picking_type_code": "internal"
        }
        if len(pickings) > 1:
            action['domain'] = [('id', 'in', pickings.ids)]
        elif len(pickings) == 1:
            form_view = [(self.env.ref('stock.view_picking_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = pickings.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
    
            
    def _compute_job_count(self):
        task_data = self.env['project.task'].read_group([('project_id', 'in', self.ids), '|', '&', '&', ('stage_id.is_closed', '=', False), ('stage_id.fold', '=', False), ('is_job_order', '=', True),('stage_id', '=', False)], ['project_id'], ['project_id'])
        result = dict((data['project_id'][0], data['project_id_count']) for data in task_data)
        for project in self:
            project.job_count = result.get(project.id, 0)
    
    def _compute_notes_count(self):
        task_data = self.env['note.note'].read_group([('project_id', 'in', self.ids), '|', '&',  ('stage_id.is_closed', '=', False), ('stage_id.fold', '=', False), ('stage_id', '=', False)], ['project_id'], ['project_id'])
        result = dict((data['project_id'][0], data['project_id_count']) for data in task_data)
        for project in self:
            project.project_notes_count = result.get(project.id, 0)
    
class ProjectTask(models.Model):
    _inherit = 'project.task'
    
    is_job_order = fields.Boolean(string='Is job order?')
    job_order_boq_line = fields.One2many('project.task.material.planning', 'task_id', string='boq Lines', copy=True, auto_join=True)
    location_id = fields.Many2one('stock.location',related='project_id.location_id', )
    #requisition_ids = fields.One2many('purchase.demand', 'task_id', string='Task', readonly=True, )
    #stock_move = fields.One2many('stock.move', 'task_id', string='Task', readonly=True, )
    
    task_notes_count = fields.Integer(compute='_compute_notes_count', string="Notes Count")
    #purchase_demand_count = fields.Integer(compute='_compute_purchase_demand_count', string="Requisition Count")
    
    #move_raw_ids = fields.One2many('stock.move', 'component_task_id', 'Components', copy=True, )

        
    def _compute_notes_count(self):
        task_data = self.env['note.note'].read_group([('task_id', 'in', self.ids)], ['task_id'], ['task_id'])
        result = dict((data['task_id'][0], data['task_id_count']) for data in task_data)
        for task in self:
            task.task_notes_count = result.get(task.id, 0)
            
    #def _compute_purchase_demand_count(self):
     #   task_data = self.env['purchase.demand'].read_group([('task_id', 'in', self.ids)], ['task_id'], ['task_id'])
      #  result = dict((data['task_id'][0], data['task_id_count']) for data in task_data)
       # for task in self:
        #    task.purchase_demand_count = result.get(task.id, 0)
