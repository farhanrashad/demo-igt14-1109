# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'
    
    requisition_template_id = fields.Many2one(
        'purchase.requisition.template', 'Requisition Template',
        readonly=True, check_company=True,
        states={'draft': [('readonly', False)], },
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    
    @api.onchange('requisition_template_id')
    def onchange_requisition_template_id(self):
        if not self.requisition_template_id:
            return

        self = self.with_company(self.company_id)
        template = self.requisition_template_id
        if template.note:
            self.note = template.note

        # Create Requisition lines if necessary
        order_lines = []
        for line in template.requisition_template_line_ids:
            # Compute quantity
            if line.product_uom_id != line.product_id.uom_po_id:
                product_qty = line.product_uom_id._compute_quantity(line.product_uom_qty, line.product_id.uom_po_id)
            else:
                product_qty = line.product_uom_qty
                
            # Create Requisition line
            order_line_values = line._prepare_purchase_requisition_line(product_qty=product_qty, )
            order_lines.append((0, 0, order_line_values))
        self.line_ids = order_lines
            
        # --- first, process the list of products from the template
        """
        requisition_lines = [(5, 0, 0)]
        data = {}
        for line in template.requisition_template_line_ids:
            #data = self._compute_line_data_for_template_change(line)

            if line.product_id:
                data.update({
                    'product_qty': line.product_uom_qty,
                    'product_id': line.product_id.id,
                    'product_uom_id': line.product_uom_id.id,
                })

                requisition_lines.append((0, 0, data))

        self.line_ids = requisition_lines
        """