from odoo import models, api,fields


class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'
    reason = fields.Char(string='Reason')

    def generate_report(self):
        print('ID: ', self.id)
        id = self.id
        data = {
            'id': id
        }
        return self.env.ref('de_po_deviation_report.po_deviation_report').report_action(self, data=data)
