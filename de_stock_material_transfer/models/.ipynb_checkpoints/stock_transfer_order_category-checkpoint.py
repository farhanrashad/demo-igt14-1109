# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date
from random import randint

CATEGORY_SELECTION = [
    ('required', 'Required'),
    ('optional', 'Optional'),
    ('no', 'None')]

class StockTransferOrderCategory(models.Model):
    _name = "stock.transfer.order.category"
    _description = "Transfer Order Category"

    def _get_picking_in(self):
        pick_in = self.env['stock.picking.type'].search([('code', '=', 'outgoing')],limit=1,)
        company = self.env.company
        if not pick_in or pick_in.sudo().warehouse_id.company_id.id != company.id:
            pick_in = self.env['stock.picking.type'].search(
                [('warehouse_id.company_id', '=', company.id), ('code', '=', 'outgoing')],
                limit=1,
            )
        return pick_in

    def _get_default_return_location(self):
        location_id = self.env['stock.location'].search([('return_location','=',True)],limit=1)
        return location_id
    
    name = fields.Char('Name', required=True)
    code = fields.Char(string='Code', required=True, size=2)
    active = fields.Boolean('Active', default=True, help="If unchecked, it will allow you to hide the transfer category without removing it.")
    transfer_order_type_id = fields.Many2one('stock.transfer.order.type', string="Transfer Type", required=True)
    
    action_type = fields.Selection([
        ('normal', 'Normal'),
        ('returnable', 'Returnable'),
        ('replacement', 'Replacement'),
        ], string='Action Type', required=True, readonly=False, default='normal')
    
    description = fields.Text("Requirements", help="Enter here the details of transfer category.")
    default_delivery_validity = fields.Integer('Delivery validity')
    delivery_lead_days = fields.Integer('Delivery lead time')
    default_return_validity = fields.Integer('Return validity')
    default_order_validity = fields.Integer('Order validity')
    
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse', domain="[('company_id', '=', company_id)]", )
    picking_type_id = fields.Many2one('stock.picking.type', 'Operation Type', required=True, )
    picking_type_code = fields.Selection(related='picking_type_id.code')
    return_picking_type_id = fields.Many2one('stock.picking.type',related='picking_type_id.return_picking_type_id')
    location_src_id = fields.Many2one('stock.location', string='Source Location',  required=True, )
    location_dest_id = fields.Many2one('stock.location', string='Destination Location', )
    return_location_id = fields.Many2one('stock.location', string='Return Location', domain="[('return_location','=',True)]")

    filter_products = fields.Boolean('Filter Products by Category')
    categ_control_ids = fields.Many2many('product.category', string="Product Categories", help="Select categories to allow for transfer")
    
    group_id = fields.Many2one('res.groups', string='Security Group')
    
    #required documents booleans
    health_check_form = fields.Boolean(string='Require Health Check Form')
    fir_report = fields.Boolean(string='Require FIR Report')
    accident_report = fields.Boolean(string='Require Accident Report')
    hoto_checklist = fields.Boolean(string='Require HOTO Checklist')
    proof_attachment = fields.Boolean(string='Require Proof Documents')
    
    
    #has_penalty = fields.Boolean(string="Allow Penalty", default=False)
    #has_closed = fields.Boolean(string="Forcefully Close", default=False)
    has_partner = fields.Selection(CATEGORY_SELECTION, string="Has Partner", default="no", required=True,)
    has_reference = fields.Selection(CATEGORY_SELECTION, string="Has Reference", default="no", required=True,)
    has_purchase_order = fields.Selection(CATEGORY_SELECTION, string="Has Purchase Order", default="no", required=True,)
    has_transfer_order = fields.Selection(CATEGORY_SELECTION, string="Has Transfer Order", default="no", required=True,)
    has_transporter = fields.Selection(CATEGORY_SELECTION, string="Has Transporter", default="no", required=True,)
    has_analytic_account = fields.Selection(CATEGORY_SELECTION, string="Has Analytic Account", default="no", required=True,)
    has_analytic_tags = fields.Selection(CATEGORY_SELECTION, string="Has Analytic Tags", default="no", required=True,)
    has_tower_info = fields.Selection(CATEGORY_SELECTION, string="Has Tower info", default="no", required=True,)
    has_supplier = fields.Selection(CATEGORY_SELECTION, string="Has Supplier", default="no", required=True,)
    
    partner_category_ids = fields.Many2many('res.partner.category', 'res_partner_category_rel', column1='partner_id', column2='category_id', string='Partner Tags')
    transporter_category_ids = fields.Many2many('res.partner.category', 'res_transporter_category_rel', column1='transporter_id', column2='category_id', string='Transporter Tags')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "type name already exists!"),
    ]
    
    @api.onchange('picking_type_id')
    def _onchange_picking_type(self):
        self.location_src_id = self.picking_type_id.default_location_src_id
        self.location_dest_id = self.picking_type_id.default_location_dest_id
        
        
