# -*- coding: utf-8 -*-

import time
from odoo import api, models
from dateutil.parser import parse
from odoo.exceptions import UserError
from datetime import datetime
from odoo import api, fields, models, _

        
class EmployeeDateReport(models.AbstractModel):
    _name = 'report.test_training.employee_report_templet'
    
    
    @api.model
    def _get_report_values(self, docids, data=None):
        print('------------------------------------------------------')
        self.model = self.env.context.get('active_model')
        rec = self.env[self.model].browse(self.env.context.get('active_id'))
        print('-----------------------------------------',rec)
#         docs = self.env['sales.team.target'].get_commission_report_values(rec.month, rec.year)

        
        return {
            'doc_ids': self.ids,
            'doc_model': 'test_training.test.training',
#             'docs': docs,
            'rec': rec,
        }
        