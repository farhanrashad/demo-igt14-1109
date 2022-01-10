# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import requests
import json


class MaterialRequestForm(models.Model):
    _name = 'material.request.form'
    _description = 'Material Request Form'
    
    
    
    def pre_create(self):
        if not self.mrf_lines:
            raise UserError(('Please make sure you have added at least one line item.'))
        
        if self.cos_entity_id == False:
            data_dic = {
                "mrf_type": int(self.mrf_type.cos_mrf_type_id),
                "moving_from": int(self.moving_from.cos_moving_from_id),
                "sp_mrf_id": int(self.sp_mrf_id),
                "contractor": [
                  self.contractor.system_name
                ]
              }
            rec = self.env['cos.master'].create_equipment_request(data_dic)
            self.cos_entity_id = rec['id']
            print('self.cos_entity_id----',self.cos_entity_id)
            
            version = 0
            for line in self.mrf_lines:
                if line.cos_intermediate_entity_id == False:
                    line_data_dic = {
                        "reference": line.product_id.default_code,
                        "designation": line.product_id.name,
                        "category": line.product_id.cos_categ_id.cos_category_id,
                        "quantity_requested": line.quantity_requested,
                        "quantity_prepared": line.quantity_prepared,
                        "request_type": "2",
                        "comment": line.comment
                      }
                    print('line_data_dic---',line_data_dic)
                    rec_line = self.env['cos.master'].create_intermediate_product(line_data_dic)
                    line.cos_intermediate_entity_id = rec_line['id']
                    print('cos_intermediate_entity_id--',line.cos_intermediate_entity_id)
                    
                    
                    rec_catalog = self.env['cos.master'].create_intermediate_with_catalog_relation(line.cos_intermediate_entity_id, line.product_id.cos_entity_id)
                    print('rec_catalog',rec_catalog)
                    
                    source_id = self.cos_entity_id
                    target_id = line.cos_intermediate_entity_id
                    
                    relation_exists = self.env['cos.master'].get_equipment_existing_relation(source_id)
                    print('relation_exists',relation_exists)
                    print('-------------------------------------------')
                    
                    if relation_exists == []:
                        print('call if ---')
                        first_rel_dic = [{'id': 0, 'relationId': 718, 'sourceId': source_id, 'targetId': target_id, 'enabled': True, 'property': ''}]
                        print('first_rel_dic--',first_rel_dic)
                        rel_rec = self.env['cos.master'].create_relation_mrf_lines(source_id, first_rel_dic, version)
                        version = version + 1
                    else:
                        print('call else---')
                        new_rel_dic = {'id': 0, 'relationId': 718, 'sourceId': source_id, 'targetId': target_id, 'enabled': True, 'property': ''}
                        relation_exists.append(new_rel_dic)
                        print('relation_exists modified',relation_exists)
                        rel_rec = self.env['cos.master'].create_relation_mrf_lines(source_id, relation_exists, version)
                        version = version + 1
                    print(rel_rec)
            self.is_created_on_cos = True
    
    
    name = fields.Char('Name')
    cos_entity_id = fields.Char()
    equipment_request_id = fields.Char('Equipment Request ID')
    request_type =  fields.Selection([('1', 'MRF'), ('2', 'Reverse request'), ('3', 'Transfer request'), ('4', 'SP MRF')])
    sp_mrf_id =  fields.Char()
    status =  fields.Selection([('1', 'New'), ('2', 'Confirmed'), ('3', 'Rejected'), ('4', 'Cancelled'), 
                                ('5', 'Prepared'), ('6', 'Notified'), ('7', 'Delivered')], default='1')
    mrf_type =  fields.Many2one('mrf.type.cos', string='MRF Type')
    moving_from =  fields.Many2one('mrf.moving.from.cos', string='Moving From')
    er_date =  fields.Char()
    pick_up_date =  fields.Char()
    delivery =  fields.Selection([('1', 'At a warehouse'), ('2', 'On location / site'), ('3', 'To a contractor'), ('4', 'Pick up at warehouse')])
    delivery_place = fields.Char()
    return_explanations =  fields.Char()
    requested_availability =  fields.Date('Request Availability')
    last_change =  fields.Char()
    unloading =  fields.Selection([('1', 'None'), ('2', 'Manual'), ('3', 'Crane')], default='1')
    lifting =  fields.Selection([('1', 'None'), ('2', 'Manual'), ('3', 'Crane')], default='1')
    contractor =  fields.Many2one('cos.team', string="Team In-Charge")
    sp_mrf_validated =  fields.Char()
    mrf_lines = fields.One2many('material.request.form.line', 'mrf_id')
    is_created_on_cos = fields.Boolean('Is created on COS?')
    
    
    
    
    
    




