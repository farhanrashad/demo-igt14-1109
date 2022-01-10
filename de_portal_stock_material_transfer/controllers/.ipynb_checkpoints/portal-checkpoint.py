# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import OrderedDict
from operator import itemgetter
from odoo.exceptions import UserError

from odoo import http, _, fields
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.tools import groupby as groupbyelem
import ast
from odoo.osv.expression import OR
import json
stock_transfer_list = []
stock_transfer_return_list = []


def stock_material_page_content(flag = 0):
    partners = request.env['res.users'].sudo().search([('id','=',http.request.env.context.get('uid'))])
    transfer_category = request.env['stock.transfer.order.category'].sudo().search([('website_published','=',True)])
    transfer_type = request.env['stock.transfer.order.type'].sudo().search([('website_published','=',True)])
    return {
        'partners': partners,
        'transfer_category': transfer_category,
        'transfer_type': transfer_type,
        'success_flag' : flag,
    }

def stock_material_submit_thanks(mrf):
    requisition = request.env['stock.transfer.order'].sudo().search([('id','=',mrf)])
    return {
        'requisition': requisition,
    }

def stock_material_type_page_content(flag = 0):
    transfer_types = request.env['stock.transfer.order.type'].sudo().search([('website_published','=',True)])
    transfer_type_list = []
    for transfer in transfer_types:
        for group in transfer.group_id.users:
            if group.id == http.request.env.context.get('uid'):
                transfer_type_list.append(transfer.id)

    transfer_type = request.env['stock.transfer.order.type'].search([('id', 'in', transfer_type_list)])
    transfer_categories = request.env['stock.transfer.order.category'].sudo().search([('website_published','=',True)])
    transfer_categ_list = []
    for categ in transfer_categories:
        for group in categ.group_id.users:
            if group.id == http.request.env.context.get('uid'):
                transfer_categ_list.append(categ.id)

    transfer_category = request.env['stock.transfer.order.category'].search([('id', 'in', transfer_categ_list)])

    return {
        'transfer_category': transfer_category,
        'transfer_type': transfer_type,
    }

def stock_material_category_page_content(transfer_category, transfer_type):
    transfer_types = transfer_type
    transfer_type_list = []
    for transfer in transfer_types:
        for group in transfer.group_id.users:
            if group.id == http.request.env.context.get('uid'):
                transfer_type_list.append(transfer.id)

    transfer_type = request.env['stock.transfer.order.type'].sudo().search([('id', 'in', transfer_type_list),('website_published','=',True)])
    transfer_categories = transfer_category
    transfer_category_list = []
    for categ in transfer_categories:
        for group in categ.group_id.users:
            if group.id == http.request.env.context.get('uid'):
                transfer_category_list.append(categ.id)
    transfer_category = request.env['stock.transfer.order.category'].sudo().search([('id', 'in', transfer_category_list),('website_published','=',True)])
    src_lists = request.env['stock.location'].sudo().search([])
    destination_lists = request.env['stock.location'].sudo().search([])
    
    return {
        'src_lists': src_lists,
        'destination_lists': destination_lists,
        'transfer_category': transfer_category,
        'transfer_type': transfer_type.id,
    }


def stock_material_type_categ_page_content(transfer_category, transfer_type,location_src_id,location_dest_id,location_return_id):
    global stock_transfer_list
    global stock_transfer_return_list
    product_lists = request.env['product.product'].sudo().search([])
    project_lists = request.env['project.project'].sudo().search([])
    product_lists = request.env['product.product'].sudo().search([])
    transfer_lists = request.env['stock.transfer.order'].sudo().search([])
    purchase_lists = request.env['purchase.order'].sudo().search([])
    transporter_lists = request.env['res.partner'].sudo().search([])
    supplier_lists = request.env['res.partner'].sudo().search([])
    transfer_categ_list = []
    transfer_categories = transfer_category
    for categ in transfer_categories:
        for group in categ.group_id.users:
            if group.id == http.request.env.context.get('uid'):
                transfer_categ_list.append(categ.id)
    transfer_category = request.env['stock.transfer.order.category'].sudo().search([('id','in',transfer_categ_list)])
    has_reference = '0'
    if transfer_category.has_reference == 'optional':
        has_reference = '1'
    if transfer_category.has_reference == 'required':
        has_reference = '2'
    has_purchase_order = '0'
    if transfer_category.has_purchase_order == 'optional':
        has_purchase_order = '1'
    if transfer_category.has_purchase_order == 'required':
        has_purchase_order = '2'
    has_transfer_order = '0'
    if transfer_category.has_transfer_order == 'optional':
        has_transfer_order = '1'
    if transfer_category.has_transfer_order == 'required':
        has_transfer_order = '2'
    has_transporter = '0'
    if transfer_category.has_transporter == 'optional':
        has_transporter = '1'
    if transfer_category.has_transporter == 'required':
        has_transporter = '2'
    returnable = '0'
    if transfer_category.action_type == 'returnable':
        returnable = '1'
    src_lists = request.env['stock.location'].sudo().search([('id','=', location_src_id)])
    destination_lists = request.env['stock.location'].sudo().search([('id','=',location_dest_id)])
    return_src_lists = request.env['stock.location'].sudo().search([('id','=',location_dest_id)])
    return_destination_lists = request.env['stock.location'].sudo().search([('id','=',location_return_id)])
    parent_src_lists = request.env['stock.location'].sudo().search([('id','=', location_src_id)])
    parent_destination_lists = request.env['stock.location'].sudo().search([('id','=',location_dest_id)])
    parent_return_lists = request.env['stock.location'].sudo().search([('id','=',location_return_id)])


    return {
        'src_lists':  src_lists,
        'destination_lists': destination_lists, 
        'product_lists': product_lists,
        'returnable': returnable,
         'return_src_lists': return_src_lists,
         'return_destination_lists': return_destination_lists,
        'has_transporter': has_transporter,
        'has_purchase_order': has_purchase_order,
        'parent_src_lists': parent_src_lists,
        'parent_destination_lists': parent_destination_lists,
        'parent_return_lists': parent_return_lists,
        'has_reference': has_reference,
        'has_transfer_order': has_transfer_order,
        'purchase_lists': purchase_lists,
        'transfer_lists': transfer_lists,
        'project_lists': project_lists,
        'transporter_lists': transporter_lists,
        'stock_transfer_list': stock_transfer_list,
        'stock_transfer_return_list': stock_transfer_return_list,
        'supplier_lists': supplier_lists,
        'categ': transfer_category,
        'transfer_category': transfer_category.id,
        'transfer_type': transfer_type.id,
    }



class CreateStockMaterial(http.Controller):
    
    
    
    @http.route('/stock/material/edit/save',type="http", website=True, auth='user')
    def stockmaterial_line_template(self, **kw):
        materialline = request.env['stock.transfer.order'].search([('id', '=', int(kw.get('stock_transfer_id')))])
        material_list = ast.literal_eval(kw.get('stockmaterial_vals'))
        obj_count = 0
        for obj_line in material_list:
            obj_count += 1
            if obj_count > 1 :               
                materila_line = request.env['stock.transfer.return.line'].search([('id', '=', obj_line['col4'])])
                if materila_line:
                    materila_line.update({
                        'product_id': obj_line['col1'],
                        'igt_barcode': obj_line['col2'],
                        'oem_barcode':  obj_line['col3'],
                    })
        return request.redirect('/stock/material/%s'%(materialline.id))    

    @http.route('/stock/material/type/',type="http", website=True, auth='user')
    def stock_material_type_template(self, **kw):
       return request.render("de_portal_stock_material_transfer.stock_transfer_type", stock_material_type_page_content())

    @http.route('/stock/material/type/categ/', type="http", website=True, auth='user')
    def stock_material_type_categ_template(self, **kw):
        id = int(kw.get('transfer_type_id'))
        transfer_type = request.env['stock.transfer.order.type'].sudo().search([('id','=',id)])
        transfer_category = request.env['stock.transfer.order.category'].sudo().search([('transfer_order_type_id','=',id)])
        
        return request.render("de_portal_stock_material_transfer.stock_transfer_type_categ_Create",
                              stock_material_category_page_content(transfer_category, transfer_type))

    @http.route('/stock/material/transfer/categ/', type="http", website=True, auth='user')
    def stock_material_transfer_categ_template(self, **kw):
        global stock_transfer_list
        global stock_transfer_return_list
        stock_transfer_return_list = []
        stock_transfer_list = []
        id = int(kw.get('transfer_type_id'))
        location_src_id = int(kw.get('location_src_id')) 
        location_dest_id = int(kw.get('location_dest_id'))
        location_return_id = int(kw.get('location_return_id'))
        transfer_type = request.env['stock.transfer.order.type'].sudo().search([('id','=',id)])
        transfer_category = request.env['stock.transfer.order.category'].sudo().search([('id','=',int(kw.get('categ_id')))])

        return request.render("de_portal_stock_material_transfer.portal_create_stock_material_transfer",
                              stock_material_type_categ_page_content(transfer_category, transfer_type,location_src_id, location_dest_id,location_return_id))

    @http.route('/stock/material/save', type="http", auth="public", website=True , methods=['GET', 'POST'])
    def create_stock_material(self, **kw):
        list = []
        stock_transfer_lista = []
        stock_transfer_return_listb = []
        if kw.get('product_req_setting_vals'):
            stock_transfer_lista = ast.literal_eval(kw.get('product_req_setting_vals'))
        if  kw.get('return_req_setting_vals'):    
            stock_transfer_return_listb = ast.literal_eval(kw.get('return_req_setting_vals'))
        has_purchase = False
        has_transfer = False
        has_transporter = False
        if kw.get('purchase_id'):
            has_purchase = int(kw.get('purchase_id'))
        if kw.get('transfer_id'):
            if kw.get('transfer_id')!='blank': 
                has_transfer = int(kw.get('transfer_id'))
        if kw.get('transporter_id'):
            has_transporter = int(kw.get('transporter_id'))
        transfer_categ = request.env['stock.transfer.order.category'].sudo().search([('id','=',int(kw.get('transfer_category_id')))])
        sequence = request.env['ir.sequence'].sudo().search([('prefix','=', transfer_categ.code)])
        if not sequence:
            seq_vals = {
                'name': transfer_categ.name,
                'implementation': 'standard',
                'padding': 1,
                'number_next_actual': 1,
                'prefix': transfer_categ.code,
            }
            sequence = request.env['ir.sequence'].sudo().create(seq_vals)
        material_val = {
            'name': sequence.next_by_id(),
            'sequence_code': transfer_categ.code,
            'location_src_id': int(kw.get('location_src_id')),
            'location_dest_id': int(kw.get('location_dest_id')) ,
            'return_location_id': int(kw.get('location_return_id')),
            'sequence_id': sequence.id,
            'purchase_id': has_purchase,
            'stock_transfer_order_id': has_transfer,
            'transfer_order_type_id': int(kw.get('transfer_type_id')),
            'stage_id': request.env['stock.transfer.order.stage'].sudo().search([('stage_category','=','draft')], limit=1).id,
            'transfer_order_category_id': int(kw.get('transfer_category_id')),
            'partner_id':request.env['res.users'].sudo().search([('id','=',http.request.env.context.get('uid'))]).partner_id.id,
            'transporter_id': has_transporter,
            'reference': kw.get('reference'),
        }
        record = request.env['stock.transfer.order'].sudo().create(material_val)
        line_product_count = 0
        for stock in stock_transfer_lista:
            line_product_count += 1
            if line_product_count > 1:
                line_product =request.env['product.product'].sudo().search([('name','=',stock['col1'])], limit=1)
                line_src_loc =request.env['stock.location'].sudo().search([('name','=',stock['col6'])], limit=1)
                line_dest_loc =request.env['stock.location'].sudo().search([('name','=',stock['col5'])], limit=1)
                line_supplier =request.env['res.partner'].sudo().search([('name','=',stock['col5'])], limit=1)
                line_project =request.env['project.project'].sudo().search([('name','=',stock['col4'])], limit=1)
                line_vals = {
                    'stock_transfer_order_id': record.id,
                    'product_id': line_product.id,
                    'name': stock['col2'],
                    'product_uom_qty': stock['col3'],
                    'project_id': line_project.id,
                    'date_scheduled': fields.date.today(),
                    'location_dest_id': line_src_loc.id if line_src_loc else False, 
                    'location_src_id': line_dest_loc.id if line_dest_loc else False, 
                    'supplier_id': line_supplier.id,
                }
                record_lines = request.env['stock.transfer.order.line'].sudo().create(line_vals)
        return_line_count = 0
        for stockline in stock_transfer_return_listb:
            return_line_count += 1
            if return_line_count > 1:
                return_line_product =request.env['product.product'].sudo().search([('name','=',stockline['col1'])], limit=1)
                return_line_src_loc =request.env['stock.location'].sudo().search([('name','=',stockline['col7'])], limit=1)
                return_line_dest_loc =request.env['stock.location'].sudo().search([('name','=',stockline['col8'])], limit=1)
                return_line_project =request.env['project.project'].sudo().search([('name','=',stockline['col6'])], limit=1)
                return_line_vals = {
                    'stock_transfer_order_id': record.id,
                    'product_id': return_line_product.id,
                    'igt_barcode': stockline['col2'],
                    'oem_barcode':stockline['col3'],
                    'name': stockline['col4'],
                    'product_uom_qty': stockline['col5'],
                    'project_id': return_line_project.id,
                    'date_scheduled': fields.date.today(),
                    'location_src_id': return_line_src_loc.id if return_line_src_loc else False,
                    'location_dest_id': return_line_dest_loc.id if return_line_dest_loc else False,
                }
                record_lines = request.env['stock.transfer.return.line'].sudo().create(return_line_vals)
        return request.render("de_portal_stock_material_transfer.stock_material_submited", stock_material_submit_thanks(record.id))
    
    

    @http.route('/stock/material/line/save', type="http", auth="public", website=True)
    def create_stock_material_line(self, **kw):
        global stock_transfer_list
        if kw.get('product_uom_qty') <= '0':
            raise UserError('Please Select Quantity Greater than 0!')
        line_vals = {
            'product_id': int(kw.get('product_id')),
            'name': kw.get('name'),
            'product_uom_qty': kw.get('product_uom_qty'),
            'project_id': int(kw.get('project_id')),
            'date_scheduled': fields.date.today(),
            'supplier_id': int(kw.get('supplier_id')),
            'location_dest_id': int(kw.get('location_dest_id')) if kw.get('location_dest_id') else False,
            'location_src_id': int(kw.get('location_src_id')) if kw.get('location_src_id') else False,
        }
        stock_transfer_list.append(line_vals)
        transfer_type = request.env['stock.transfer.order.type'].sudo().search([('id', '=', int(kw.get('transfer_type_id_line')))])
        transfer_category = request.env['stock.transfer.order.category'].sudo().search([('id', '=', int(kw.get('transfer_category_id_line')))])
        location_src_id_line = int(kw.get('location_src_id_line'))
        location_dest_id_line = int(kw.get('location_dest_id_line'))
        location_return_id_line = int(kw.get('location_return_id_line'))
        return request.render("de_portal_stock_material_transfer.portal_create_stock_material_transfer", stock_material_type_categ_page_content(transfer_category, transfer_type,location_dest_id=location_dest_id_line,location_src_id=location_src_id_line,location_return_id=location_return_id_line))

    @http.route('/stock/material/return/line/save', type="http", auth="public", website=True)
    def create_stock_material_return_line(self, **kw):
        global stock_transfer_return_list
        if kw.get('product_uom_qty') <= '0':
            raise UserError('Please Select Quantity Greater than 0!')
        line_vals = {
            'product_id': int(kw.get('product_id')),
            'igt_barcode': kw.get('igt_barcode'),
            'oem_barcode': kw.get('oem_barcode'),
            'name': kw.get('name'),
            'product_uom_qty': kw.get('product_uom_qty'),
            'project_id': int(kw.get('project_id')),
            'date_scheduled': fields.date.today(),
            'location_src_id': int(kw.get('location_src_id')) if kw.get('location_src_id') else False,
            'location_dest_id': int(kw.get('location_dest_id')) if kw.get('location_dest_id') else False,
        }
        stock_transfer_return_list.append(line_vals)
        transfer_type = request.env['stock.transfer.order.type'].sudo().search([('id', '=', int(kw.get('transfer_type_id_line')))])
        transfer_category = request.env['stock.transfer.order.category'].sudo().search([('id', '=', int(kw.get('transfer_category_id_line')))])
        location_src_id_line = int(kw.get('location_src_id_line'))
        location_dest_id_line = int(kw.get('location_dest_id_line'))
        location_return_id_line = int(kw.get('location_return_id_line'))
        return request.render("de_portal_stock_material_transfer.portal_create_stock_material_transfer", stock_material_type_categ_page_content(transfer_category, transfer_type,location_dest_id=location_dest_id_line,location_src_id=location_src_id_line,location_return_id=location_return_id_line))


class CustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'material_count' in counters:
            active_user = request.env['res.users'].sudo().search([('id','=',http.request.env.context.get('uid'))])    
            values['material_count'] = request.env['stock.transfer.order'].sudo().search_count([('partner_id','=', active_user.partner_id.id)])
        return values

   
    # ------------------------------------------------------------
    # Stock Transfer
    # ------------------------------------------------------------
    def _stock_material_get_page_view_values(self, stock_material, access_token, **kwargs):
        returnable = '0'
        product_lists = request.env['product.product'].sudo().search([])
        if stock_material.transfer_order_category_id.action_type == 'returnable':
            returnable = '1'
        values = {
            'edit_material': False,
            'product_lists': product_lists,
            'returnable': returnable,
            'page_name': 'stock_material',
            'stock_material': stock_material,
            'user': request.env.user
        }
        return self._get_page_view_values(stock_material, access_token, values, 'stock_material_history', False, **kwargs)

    @http.route(['/stock/materials', '/stock/materials/page/<int:page>'], type='http', auth="user", website=True)
    def portal_stock_materials(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, search=None, search_in='content', groupby=None, **kw):
        values = self._prepare_portal_layout_values()
        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Title'), 'order': 'name'},
            'stage': {'label': _('Stage'), 'order': 'stage_id'},
            'update': {'label': _('Last Stage Update'), 'order': 'date_last_stage_update desc'},
        }
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
        }
        searchbar_inputs = {
            'message': {'input': 'message', 'label': _('Search in Messages')},
            'customer': {'input': 'customer', 'label': _('Search in Customer')},
            'stage': {'input': 'stage', 'label': _('Search in Stages')},
            'all': {'input': 'all', 'label': _('Search in All')},
        }
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'stage': {'input': 'stage', 'label': _('Stage')},
        }

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        # default filter by value
        if not filterby:
            filterby = 'all'
        domain = searchbar_filters.get(filterby, searchbar_filters.get('all'))['domain']
        if not groupby:
            groupby = 'stage'

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # search
        if search and search_in:
            search_domain = []
            if search_in in ('content', 'all'):
                search_domain = OR([search_domain, ['|', ('name', 'ilike', search), ('description', 'ilike', search)]])
            if search_in in ('customer', 'all'):
                search_domain = OR([search_domain, [('partner_id', 'ilike', search)]])
            if search_in in ('message', 'all'):
                search_domain = OR([search_domain, [('message_ids.body', 'ilike', search)]])
            if search_in in ('stage', 'all'):
                search_domain = OR([search_domain, [('stage_id', 'ilike', search)]])

            domain += search_domain
            
        active_user = request.env['res.users'].sudo().search([('id','=',http.request.env.context.get('uid'))])    
        domain += [('partner_id', '=', active_user.partner_id.id)]
        # task count
        stock_material_count = request.env['stock.transfer.order'].sudo().search_count(domain)
        # pager
        pager = portal_pager(
            url="/stock/materials",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'filterby': filterby, 'groupby': groupby, 'search_in': search_in, 'search': search},
            total=stock_material_count,
            page=page,
            step=self._items_per_page
        )

        materials = request.env['stock.transfer.order'].sudo().search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['stock_material_history'] = materials.ids[:100]

        
        grouped_materials = [materials]

        values.update({
            'date': date_begin,
            'date_end': date_end,
            'grouped_materials': grouped_materials,
            'page_name': 'stock_material',
            'default_url': '/stock/materials',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'searchbar_groupby': searchbar_groupby,
            'searchbar_inputs': searchbar_inputs,
            'search_in': search_in,
            'search': search,
            'sortby': sortby,
            'groupby': groupby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
        })
        return request.render("de_portal_stock_material_transfer.portal_stock_materials", values)

    @http.route(['/stock/material/<int:material_id>'], type='http', auth="public", website=True)
    def portal_stock_material(self, material_id, access_token=None, **kw):
        try:
            task_sudo = request.env['stock.transfer.order'].sudo().search([('id', '=', material_id)])
        except (AccessError, MissingError):
            return request.redirect('/my')


        values = self._stock_material_get_page_view_values(task_sudo, access_token, **kw)
        return request.render("de_portal_stock_material_transfer.portal_stock_material", values)
    
    
    def _stock_material_get_page_view_values_edit(self, stock_material, access_token, **kwargs):
        returnable = '0'
        product_lists = request.env['product.product'].sudo().search([])
        if stock_material.transfer_order_category_id.action_type == 'returnable':
            returnable = '1'
        values = {
            'edit_material': True,
            'product_lists': product_lists,
            'returnable': returnable,
            'page_name': 'stock_material',
            'stock_material': stock_material,
            'user': request.env.user
        }
        return self._get_page_view_values(stock_material, access_token, values, 'stock_material_history', False, **kwargs)
    
    @http.route(['/stock/material/edit/<int:material_id>'], type='http', auth="public", website=True)
    def portal_stock_material_edit(self, material_id, access_token=None, **kw):
        try:
            task_sudo = request.env['stock.transfer.order'].sudo().search([('id', '=', material_id)])
        except (AccessError, MissingError):
            return request.redirect('/my')


        values = self._stock_material_get_page_view_values_edit(task_sudo, access_token, **kw)
        return request.render("de_portal_stock_material_transfer.portal_stock_material", values)
