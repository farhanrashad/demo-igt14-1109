from odoo import models, api,fields


class PurchaseOrderLineInherit(models.Model):
    _inherit = 'purchase.requisition.line'
    
    kpa = fields.Selection([('50',50),('100',100),('150',150)],string='KPA')
    tower_manufacture = fields.Many2one('res.partner', string="Tower Manufacture")
    tower = fields.Many2one('product.product', string="Tower")
    kmph = fields.Selection([('130',130),('160',160),('195',195),('225',225)],string='KMPH')
    candidate =  fields.Selection([('c1', 'C1'),('c2', 'C2'),('c3', 'C3'),('c4', 'C4'),
                                   ('c5', 'C5'),('c6', 'C6'),('c7', 'C7'), ('c8', 'C8'), 
                                   ('c9', 'C9'), ('c10', 'C10'), ('c11', 'C11'), ('c12', 'C12'), 
                                   ('c13', 'C13'), ('c14', 'C14'), ('c15', 'C15'), ('c16', 'C16'), 
                                   ('c17', 'C17'), ('c18', 'C18'), ('c19', 'C19'), ('c20', 'C20')],
                                    string='Candidate')
    tenant = fields.Many2one('res.partner',string="Tenant")