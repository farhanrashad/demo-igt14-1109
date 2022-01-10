from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ReportActiveLeaseWizard(models.TransientModel):
    _name = "report.active.lease.wizard"
    _description = 'Active Lease Wizard Report'
    
    def print_report(self):
       
        return self.env.ref('de_report_active_lease.report_active_lease_report').report_action(self)
