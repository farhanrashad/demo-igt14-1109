# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval


class StockTransferSchedulerWizard(models.TransientModel):
    _name = "stock.transfer.scheduler.wizard"
    _description = 'Stock Transfer Scheduler Wizard'

    def set_close(self):
        #order = self.env['stock.transfer.order'].browse(self.env.context.get('active_id'))
        today = fields.Datetime.now()
        domain = [('delivery_deadline', '<', today),('stage_category', 'not in', ['close','cancel'])]
        orders = self.env['stock.transfer.order'].search(domain)
        for order in orders:
            order.sudo().set_close('delivery')
