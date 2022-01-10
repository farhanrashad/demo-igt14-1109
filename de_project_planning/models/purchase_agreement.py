# -*- coding: utf-8 -*-
from datetime import datetime, time
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date


class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'
    
    project_id = fields.Many2one('project.project', string='Project', domain="[('allow_site_planning','=',True)]")
    
class PurchaseRequisitionLine(models.Model):
    _inherit = 'purchase.requisition.line'
    
    project_id = fields.Many2one('project.project', string='Project', domain="[('allow_site_planning','=',True)]")
    state_id = fields.Many2one('res.country.state', compute='_compute_project_state')
    
    @api.depends('project_id')
    def _compute_project_state(self):
        for line in self:
            if line.project_id:
                line.state_id = line.project_id.address_id.state_id.id
            else:
                line.state_id = False
                
    @api.onchange('product_id')
    def onchange_product(self):
        if not self.project_id:
            self.project_id = self.requisition_id.project_id.id
    
    @api.onchange('project_id')
    def onchange_project_id(self):
        if not self.account_analytic_id:
            self.account_analytic_id = self.project_id.analytic_account_id.id
            
    def _prepare_purchase_order_line(self, name, product_qty=0.0, price_unit=0.0, taxes_ids=False):
        self.ensure_one()
        requisition = self.requisition_id
        if self.product_description_variants:
            name += '\n' + self.product_description_variants
        if requisition.schedule_date:
            date_planned = datetime.combine(requisition.schedule_date, time.min)
        else:
            date_planned = datetime.now()
        return {
            'name': name,
            'product_id': self.product_id.id,
            'product_uom': self.product_id.uom_po_id.id,
            'product_qty': product_qty,
            'price_unit': price_unit,
            'taxes_id': [(6, 0, taxes_ids)],
            'date_planned': date_planned,
            'project_id': self.project_id.id,
            'account_analytic_id': self.account_analytic_id.id,
            'analytic_tag_ids': self.analytic_tag_ids.ids,
        }