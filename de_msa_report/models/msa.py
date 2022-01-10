from odoo import models, api


class MSAInherit(models.Model):
    _inherit = 'master.service.agreement'

    def print_msa_report(self):
        print('ID: ', self.id)
        data = {
            'id': self.id
        }
        return self.env.ref('de_msa_report.msa_report_xlsx_1').report_action(self, data=data)
