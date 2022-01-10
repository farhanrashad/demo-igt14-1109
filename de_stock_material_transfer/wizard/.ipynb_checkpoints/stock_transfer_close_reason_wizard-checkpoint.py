# -*- coding: utf-8 -*-
from odoo import api, fields, models


class StockTransferCloseReasonWizard(models.TransientModel):
    _name = "stock.transfer.close.reason.wizard"
    _description = 'Stock Transfer Close Reason Wizard'

    close_reason_id = fields.Many2one("stock.transfer.close.reason", string="Close Reason")
    close_reason_message = fields.Char(string='Message')

    def set_close(self):
        self.ensure_one()
        order = self.env['stock.transfer.order'].browse(self.env.context.get('active_id'))
        stage_id = self.env['stock.transfer.order.stage'].search([('transfer_order_type_ids','=',order.transfer_order_type_id.id),('stage_category','=','close')],limit=1)
        order.close_reason_id = self.close_reason_id
        order.close_reason_message = self.close_reason_message
        order.stage_id = order.close_reason_id.stage_id.id
        for picking in order.picking_ids.filtered(lambda p: p.picking_type_id.id in (order.transfer_order_category_id.picking_type_id.id, order.transfer_order_category_id.return_picking_type_id.id) and p.state not in ('done','cancel')):
                picking.sudo().action_cancel()
        #order.set_close(order.close_reason_id.reason_type)
