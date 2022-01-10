from odoo import models, api,fields


class StockTransferOrderInherit(models.Model):
    _inherit = 'stock.transfer.order'
    
    mobile_no = fields.Char(string = 'Mobile No', related='user_id.mobile_phone')
    