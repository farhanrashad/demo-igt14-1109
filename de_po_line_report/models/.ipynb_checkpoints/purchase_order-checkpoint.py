from odoo import models, api


class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    def print_report(self):
        print('ID: ', self.id)
        id = self.id
        data = {
            'id': id
        }
        return self.env.ref('de_po_line_report.po_line_report').report_action(self, data=data)
