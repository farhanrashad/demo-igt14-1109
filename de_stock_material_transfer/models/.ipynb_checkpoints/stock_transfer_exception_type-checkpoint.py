# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class TransferOrderException(models.Model):
    _name = "stock.transfer.exception.type"
    _description = "Transfer Exception"
    _order = 'sequence, id'

    code = fields.Char(string='Code', size=3, copy=False)
    name = fields.Char(string='Name', )
    message_type = fields.Selection([
        ('none', 'None'),
        ('warning', 'Warning'),
        ('block', 'Block Message'),
    ], string='Message Type', default='none', )
    message = fields.Char(string='Message', )
    sequence = fields.Integer(default=1)
    
    transfer_order_type_ids = fields.Many2many('stock.transfer.order.type', 'transfer_order_type_exceptione_rel', 'transfer_order_stage_id', 'transfer_order_type_id', string='Transfer Types')
    
    transfer_order_category_ids = fields.Many2many('stock.transfer.order.category', 'transfer_order_category_exception_rel', 'transfer_order_stage_id', 'transfer_order_category_id', string='Transfer Categories', domain="[('transfer_order_type_id','=',transfer_order_type_ids)]")
    
    #transfer_order_type_id = fields.Many2one('stock.transfer.order.type', string='Transfer Type', )
    #transfer_order_category_id = fields.Many2one('stock.transfer.order.category', string='Transfer Category', domain="[('transfer_order_type_id','=',transfer_order_type_id)]")

    stage_id = fields.Many2one('stock.transfer.order.stage', string='Add Stage')
    next_stage_id = fields.Many2one('stock.transfer.order.stage', string='Next Stage')
    prv_stage_id = fields.Many2one('stock.transfer.order.stage', string='Previous Stage')
    

    apply_stage_id = fields.Many2one('stock.transfer.order.stage', string='Apply On')
    exec_stage_id = fields.Many2one('stock.transfer.order.stage', string='Execute On')
    stage_auto_apply = fields.Boolean(string='Stage Auto Apply')
    picking_type_id = fields.Many2one('stock.picking.type', 'Operation Type', )
    location_src_id = fields.Many2one('stock.location', string='Source Location',  )
    location_dest_id = fields.Many2one('stock.location', string='Destination Location', )
    return_picking_type_id = fields.Many2one('stock.picking.type',related='picking_type_id.return_picking_type_id')
    return_location_id = fields.Many2one('stock.location', string='Return Location', domain="[('return_location','=',True)]")
    active = fields.Boolean('Active', default=True,
        help="If unchecked, it will allow you to hide the exception without removing it.")
    
    
    _sql_constraints = [
        ('unique_exception', 'unique (code)', 'Exception already defined'),
    ]
