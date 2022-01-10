# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import requests
import json
from datetime import datetime,date


class CosMaster(models.Model):
    _name = 'cos.master'
    _description = 'Click on Site Master'
        
    cos_login_response = fields.Char(string='Cos Login Response')
    cos_logout_response = fields.Char(string='Cos Logout Response')
    token = fields.Char(string="Token")
    username = fields.Char(required=True)
    password = fields.Char(required=True)

    def action_get_login_token(self):
        url = "https://cos-uat.igt.com.mm/igt/cosapi/identity/login"

        payload = json.dumps({
          "loginName": self.username,
          "password": self.password
#           "loginName": "DYN_Moiz",
#           "password": "Dynexcel123"
        })
        headers = {
          'x-client-tenant': 'igt',
          'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        
        response = response.json()
        token = response.get('token')
        self.cos_login_response = response
        self.token = token
        return token
                
    
    def action_get_logout(self):
        url = "https://cos-uat.igt.com.mm/igt/cosapi/identity/logout"
        login_token = self.action_get_login_token()
        payload = ""
        headers = {
          'x-client-tenant': 'igt',
          'X-Auth-Token': login_token
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        self.cos_logout_response = response.text
    
    
    def fetch_update_terminologies(self):
        self.get_cos_product_categories()
        self.get_cos_product_manufecturers()
        self.get_cos_mrf_types()
        self.get_cos_mrf_moving_from()
        self.get_cos_teams()
    
    
    def action_get_cos_products(self):
        url = "https://cos-uat.igt.com.mm/igt/cosapi/entity/type/catalog/filter"

        payload = json.dumps({
          "entityType": "catalog",
          "pageSize": "350"
        })
        headers = {
          'X-Auth-Token': self.action_get_login_token(),
          'x-client-tenant': 'igt',
          'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        response = response.json()
        
        for res in response:
            print('res product--------------',res)
            product_exists = self.env['product.product'].search([('cos_entity_id','=',res['id'])])
            categ_id = self.env['product.category.cos'].search([('cos_category_id','=',res['data']['category'])])
            
            try:
                manufacturer_bis = res['data']['manufacturer_bis']
            except:
                manufacturer_bis = None
            print('manufacturer_bis---',manufacturer_bis)
            if manufacturer_bis != None:
                manufect_id = self.env['product.manufacturer.cos'].search([('cos_manufacturer_id','=',manufacturer_bis)])
                manufect_id = manufect_id.id
            else:
                manufect_id = self.env['product.manufacturer.cos'].search([('cos_manufacturer_id','=',11)])
                manufect_id = manufect_id.id
#                 manufect_id = 11 #fixme
                
            if not product_exists:
                product_rec = self.env['product.product'].create(
                    {
                        'cos_entity_id': res['id'],
                        'name': res['data']['designation'],
                        'default_code': res['data']['part_number'],
                        'is_cos_product': True,
                        'cos_categ_id': categ_id.id,
                        'cos_manufact_id': manufect_id,
                        })
                
                
    def action_get_relation(self, entity_id):
        url = "https://cos-uat.igt.com.mm/igt/cosapi/entity/"+entity_id+"/relation"
        
        payload={}
        headers = {
          'x-client-tenant': 'igt',
          'x-auth-token': self.action_get_login_token()
        }
        
        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()
        return response
        
            
    def action_get_mrf_records(self):
        url = "https://cos-uat.igt.com.mm/igt/cosapi/entity/type/equipment_request/filter"

        payload = json.dumps({
          "entityType": "equipment_request",
          "pageSize": "50"
        })
        headers = {
          'X-Auth-Token': self.action_get_login_token(),
          'x-client-tenant': 'igt',
          'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        response = response.json()
        
        for res in response:
            print('res--------------',res)
            request_id_dic = res['data']['equipment_request_id']
            equipment_request_id = str(request_id_dic['prefix'])+'-'+str(request_id_dic['number'])
            
            try:
                sp_mrf_id = res['data']['sp_mrf_id']
            except:
                sp_mrf_id = None
                
            try:
                mrf_type = res['data']['mrf_type']
                if mrf_type:
                    mrf_type = self.env['mrf.type.cos'].search([('cos_mrf_type_id','=',mrf_type)])
                    mrf_type = mrf_type.id
            except:
                mrf_type = None
                
            try:
                contractor = res['data']['contractor']
                if contractor:
                    contractor = self.env['cos.team'].search([('system_name','=',contractor)])
                    contractor = contractor.id
            except:
                contractor = None
                
            try:
                moving_from = res['data']['moving_from']
                if moving_from:
                    moving_from = self.env['mrf.moving.from.cos'].search([('cos_moving_from_id','=',moving_from)])
                    moving_from = moving_from.id
            except:
                moving_from = None
                
            try:
                delivery = res['data']['delivery']
            except:
                delivery = None
            
            try:
                unloading = res['data']['unloading']
            except:
                unloading = None
                
            try:
                lifting = res['data']['lifting']
            except:
                lifting = None
                
            try:
                return_explanations = res['data']['return_explanations']
            except:
                return_explanations = None
                
            try:
                requested_availability = res['data']['requested_availability']
            except:
                requested_availability = None
                
            print('found req aval date****',requested_availability)
            if requested_availability != None:
                requested_availability = self.json_to_date(str(requested_availability))
                print('coversion done>>>>',requested_availability)
                
                
                
            mrf_exists = self.env['material.request.form'].search([('cos_entity_id','=',res['id'])])
            if not mrf_exists:    
                mrf_rec = self.env['material.request.form'].create(
                    {
                        'cos_entity_id': res['id'],
                        'equipment_request_id': equipment_request_id,
                        'request_type': res['data']['request_type'],
                        'sp_mrf_id': sp_mrf_id,
                        'mrf_type': mrf_type,
                        'moving_from': moving_from,
                        'delivery': delivery,
                        'return_explanations': return_explanations,
                        'requested_availability': requested_availability,
                        'unloading': unloading,
                        'lifting': lifting,
                        'contractor': contractor,
                        'status': res['data']['status'],
                        'is_created_on_cos': True,
                        })
                print('mrf_rec.cos_entity_id====',mrf_rec.cos_entity_id)
                print('relation-----------',self.action_get_relation(mrf_rec.cos_entity_id))
                
                relation = self.action_get_relation(mrf_rec.cos_entity_id)
                                                    
                for rec in relation:
                    if rec['id'] == 718:
                        for r in rec['relations']:
                            print(r['targetId'])
                            print('get_mrf_product_lines---',self.get_mrf_product_lines(r['targetId']))
                            intermediate_prod = self.get_mrf_product_lines(r['targetId'])
                            
                            
                            mrf_line_rec = self.env['material.request.form.line'].create(
                                {
                                    'cos_intermediate_entity_id': intermediate_prod['id'],
                                    'product_id': self.get_product_obj(intermediate_prod['data']['reference']).id,
                                    'request_type': intermediate_prod['data']['request_type'],
                                    'quantity_requested': intermediate_prod['data']['quantity_requested'],
                                    'quantity_prepared': intermediate_prod['data']['quantity_prepared'],
                                    'comment': intermediate_prod['data']['comment'],
                                    'mrf_id': mrf_rec.id,
                                    })
                        

    
    def get_mrf_product_lines(self, intermediate_entity_id):
        #intermediate_entity_id -- is product lines relation id, with mrf record.
        url = "https://cos-uat.igt.com.mm/igt/cosapi/entity/type/intermediate_entity/"+intermediate_entity_id
        
        payload={}
        headers = {
          'x-client-tenant': 'igt',
          'x-auth-token': self.action_get_login_token()
        }
        
        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()
        return response
    
    
    def get_product_obj(self, reference):
        product = self.env['product.product'].search([('default_code','=',reference)], order="id desc", limit=1)
        return product
    
    
    def create_product_on_cos(self, part_number, designation, category, manufacturer_bis):
        url = "https://cos-uat.igt.com.mm/igt/cosapi/entity/type/catalog"
        
        payload = json.dumps({
          "version": 0,
          "form_fields": {
            "part_number": part_number,
            "designation": designation,
            "category": category,
            "manufacturer_bis": manufacturer_bis
          },
          "relations": [],
          "acl": [],
          "entityType": "catalog"
        })
        headers = {
          'x-auth-token': self.action_get_login_token(),
          'x-client-tenant': 'igt',
          'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        response = response.json()
        return response
    
    def create_equipment_request(self, data_dic):
        print('here in actual method---')
        url = "https://cos-uat.igt.com.mm/igt/cosapi/entity/type/equipment_request"
#         print('contractor',contractor)
        payload = json.dumps({
          "version": 0,
          "form_fields": data_dic,
          "relations": [],
          "acl": [],
          "entityType": "equipment_request"
        })
#         payload = json.dumps({
#             "version": 0,
#             "form_fields": {
#             "mrf_type": mrf_type,
#             "moving_from": moving_from,
#             "sp_mrf_id": sp_mrf_id,
#             "contractor": [contractor]
#             },
#             "relations": [],
#             "acl": [],
#             "entityType": "equipment_request"
#             })
        print('payload',payload)
        
        headers = {
          'x-client-tenant': 'igt',
          'x-auth-token': self.action_get_login_token(),
          'Content-Type': 'application/json'
        }
        print('headers',headers)

        response = requests.request("POST", url, headers=headers, data=payload)
        response = response.json()
        return response
    
    
    def create_intermediate_product(self, data_dic):
        url = "https://cos-uat.igt.com.mm/igt/cosapi/entity/type/intermediate_entity"

        payload = json.dumps({
          "version": 0,
          "form_fields": data_dic,
          "relations": [],
          "acl": [],
          "entityType": "intermediate_entity"
        })
        headers = {
          'x-auth-token': self.action_get_login_token(),
          'x-client-tenant': 'igt',
          'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        response = response.json()
        return response
    
    
    def create_intermediate_with_catalog_relation(self, source_id, target_id):
        url = "https://cos-uat.igt.com.mm/igt/cosapi/entity/type/intermediate_entity/"+str(source_id)

        payload = json.dumps({
          "version": 0,
          "form_fields": {},
          "relations": [
            {
              "id": 726,
              "data": [
                {
                  "id": 0,
                  "relationId": 726,
                  "sourceId": str(source_id),
                  "targetId": str(target_id),
                  "enabled": True,
                  "property": ""
                }
              ]
            }
          ],
          "id": str(source_id),
          "entityType": "intermediate_entity"
        })
        headers = {
          'x-client-tenant': 'igt',
          'x-auth-token': self.action_get_login_token(),
          'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        response = response.json()
        return response
    
    
    def get_equipment_existing_relation(self, entity_id):
        print('in equipemnt relation----')
        url = "https://cos-uat.igt.com.mm/igt/cosapi/entity/type/equipment_request/"+str(entity_id)+"?includeRelations=true"
        
        payload={}
        headers = {
          'x-client-tenant': 'igt',
          'x-auth-token': self.action_get_login_token()
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()
        print('response --- equ rel----',response["relations"])
        return response["relations"]
      
        
    def create_relation_mrf_lines(self, source_id, data_dic, version):
        url = "https://cos-uat.igt.com.mm/igt/cosapi/entity/type/equipment_request/"+str(source_id)
        
        payload = json.dumps({
          "version": version,
          "form_fields": {},
          "relations": [
            {
              "id": 718,
              "data": data_dic
            }
          ],
          "id": str(source_id),
          "entityType": "equipment_request"
        })
        headers = {
          'x-client-tenant': 'igt',
          'x-auth-token': self.action_get_login_token(),
          'Content-Type': 'application/json'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        
        print(response.json())

    
    
    def get_cos_product_categories(self):
        url = "https://cos-uat.igt.com.mm/igt/cosapi/terminology/name/product_category?includeItems=true"

        payload={}
        headers = {
          'x-client-tenant': 'igt',
          'x-auth-token': self.action_get_login_token()
        }
        
        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()
        print('response----',response)
        for re in response['list']:
            print('re---',re)
            title = re['title']
            print('re---nodes--',re['nodes'])
            print(title)
            for node in re['nodes']:
                id = None
                name = ''
                id = node['id']
                name = title+"-"+node['title']
                
                category_exsits = self.env['product.category.cos'].search([('cos_category_id','=',id)])
                if not category_exsits:
                    self.env['product.category.cos'].create({
                        'cos_category_id': id,
                        'name': name
                        })
                else:
                    category_exsits.write({
                        'name': title
                        })

    
    def get_cos_product_manufecturers(self):
        url = "https://cos-uat.igt.com.mm/igt/cosapi/terminology/name/manufacturer?includeItems=true"

        payload={}
        headers = {
          'x-client-tenant': 'igt',
          'x-auth-token': self.action_get_login_token()
        }
        
        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()
        print('response----',response)
        for re in response['list']:
            print('re---',re)
            id = None
            name = ''
            id = re['id']
            name = re['title']
                
            manufacturer_exsits = self.env['product.manufacturer.cos'].search([('cos_manufacturer_id','=',id)])
            if not manufacturer_exsits:
                self.env['product.manufacturer.cos'].create({
                    'cos_manufacturer_id': id,
                    'name': name
                    })
            else:
                manufacturer_exsits.write({
                    'name': name
                    })
                
                
                
    def get_cos_mrf_types(self):
        url = "https://cos-uat.igt.com.mm/igt/cosapi/terminology/name/asset_movement?includeItems=true"

        payload={}
        headers = {
          'x-client-tenant': 'igt',
          'x-auth-token': self.action_get_login_token()
        }
        
        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()
        
        for re in response['list']:
            title = re['title']

            for node in re['nodes']:
                id = None
                name = ''
                id = node['id']
                name = title+"-"+node['title']
                 
                mrf_type_exsits = self.env['mrf.type.cos'].search([('cos_mrf_type_id','=',id)])
                if not mrf_type_exsits:
                    self.env['mrf.type.cos'].create({
                        'cos_mrf_type_id': id,
                        'name': name
                        })
                else:
                    mrf_type_exsits.write({
                        'name': title
                        })
                    
    
    def get_cos_mrf_moving_from(self):
#         raise UserError(self.json_to_date("1618617600000"))
        url = "https://cos-uat.igt.com.mm/igt/cosapi/terminology/name/asset_movement_type?includeItems=true"
        
        payload={}
        headers = {
          'x-client-tenant': 'igt',
          'x-auth-token': self.action_get_login_token()
        }
        
        response = requests.request("GET", url, headers=headers, data=payload)
        response = response.json()
        print('response----',response)
        for re in response['list']:
            print('re---',re)
            id = None
            name = ''
            id = re['id']
            name = re['title']
                
            moving_from_exsits = self.env['mrf.moving.from.cos'].search([('cos_moving_from_id','=',id)])
            if not moving_from_exsits:
                self.env['mrf.moving.from.cos'].create({
                    'cos_moving_from_id': id,
                    'name': name
                    })
            else:
                moving_from_exsits.write({
                    'name': name
                    })
    
    
    def json_to_date(self, jdate):
#         d = "1618617600000"
        d = int(jdate[:10])
#         a = datetime.fromtimestamp(d).strftime('%Y-%m-%d %I:%M:%S %p')
        b = datetime.fromtimestamp(d).strftime('%Y-%m-%d')
        date_obj = datetime.strptime(b, '%Y-%m-%d').date()
        return date_obj
    
    
    def get_cos_teams(self):
        url = "https://cos-uat.igt.com.mm/igt/cosapi/entity/type/team/filter"
        
        payload = json.dumps({
          "entityType": "team",
          "pageSize": "100"
        })
        headers = {
          'x-client-tenant': 'igt',
          'Content-Type': 'application/json',
          'x-auth-token': self.action_get_login_token()
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        response = response.json()
        for res in response:
            print(res)
            id = res['id']
            name = res['data']['team_name']
            system_name = res['data']['system_name']
                        
            team_exsits = self.env['cos.team'].search([('cos_team_id','=',id)])
            if not team_exsits:
                self.env['cos.team'].create({
                    'cos_team_id': id,
                    'name': name,
                    'system_name':system_name,
                    })
            else:
                team_exsits.write({
                    'name': name
                    })
            
    
    
    