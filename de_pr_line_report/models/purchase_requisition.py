from odoo import models, api


class PurchaseRequisitionInherit(models.Model):
    _inherit = 'purchase.requisition'

    def print_report(self):
        print('ID: ', self.id)
        id = self.id
        data = {
            'id': id
        }
        return self.env.ref('de_pr_line_report.pr_line_report').report_action(self, data=data)
