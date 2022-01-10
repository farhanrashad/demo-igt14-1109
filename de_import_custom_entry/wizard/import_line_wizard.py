# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models, api, _
from odoo.exceptions import UserError
import csv
import base64
import xlrd
from odoo.tools import ustr
import logging
import time
from datetime import datetime
import tempfile
import binascii
from datetime import date, datetime
from odoo.exceptions import Warning, UserError
from odoo import models, fields, exceptions, api, _
from dateutil import parser


import ast
from datetime import timedelta, datetime
from random import randint

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError, RedirectWarning
from odoo.tools.misc import format_date, get_lang
from odoo.osv.expression import OR

_logger = logging.getLogger(__name__)


class ImportLineWizard(models.TransientModel):
    _name = "custom.entry.line.import.wizard"
    _description = "Import custom entry lines wizard"

    import_type = fields.Selection([
        ('csv', 'CSV File'),
    ], default="csv", string="Import File Type", required=True)
    file = fields.Many2many('ir.attachment', relation="files_rel_import_entry_line",
                                            column1="doc_id",
                                            column2="attachment_id",
                                            string="File", required=True)
    custom_entry_id=fields.Many2one('account.custom.entry', string='Custom entry') 
    
    def import_custom_entry_line_sample(self):
        attach_file = self.custom_entry_id.custom_entry_type_id.attachment_id
        if not attach_file:
            attach_file = self.custom_entry_id.custom_entry_type_id.update_attachment_id
        download_url = '/web/content/' + str(attach_file.id) + '?download=True'
#             Return so it will download in your system
        return {
                "type": "ir.actions.act_url",
                "url": str(download_url),
                "target": "new",
        }
    

    
    def import_custom_entry_line(self):
        keys = []
        ir_model_fields_obj = self.env['ir.model.fields']
        custom_entry_obj = self.env['account.custom.entry']
        custom_entry_obj_line = self.env['account.custom.entry.line']

        try:
            file = str(base64.decodebytes(self.file.datas).decode('utf-8'))
            file_reader = csv.reader(file.splitlines())
            skip_header = True

        except:
            raise  UserError('Invalid File Format!')
        count = 0
        for row in file_reader:
            for row_val in  row:

                search_field = ir_model_fields_obj.sudo().search([
                    ("model", "=", "account.custom.entry.line"),
                    ("field_description", "=", row_val),
                ], limit=1)
                keys.append(search_field.name)

            break
        rowvals = []
        vals = []
        line_vals = {}
        for data_row in file_reader:
            inner_vals = {}
            index = 0
            i = 0
            for data_column in data_row:
#                         raise UserError(str(custom_entry.id))
                inner_vals.update({
                    'custom_entry_id': self.custom_entry_id.id
                })
                rowvals.append(data_row)
                search_field = ir_model_fields_obj.sudo().search([
                    ("model", "=", "account.custom.entry.line"),
                    ("name", "=", keys[i]),
                ], limit=1)
                if search_field.ttype == 'many2one' and search_field.name == 'car_details':

                    many2one_vals = self.env[str(search_field.relation)].search([('display_name','=',data_column)], limit=1)

                    inner_vals.update({
                        keys[i]: many2one_vals.id if many2one_vals.id else False
                    })
                    index = index + 1
                    i = i + 1
                elif search_field.ttype == 'many2one':

                    many2one_vals = self.env[str(search_field.relation)].search([('name','=',data_column)], limit=1)
                    if search_field.relation == 'res.partner':
                        many2one_vals = self.env[str(search_field.relation)].search([('ref','=',data_column)], limit=1)


                    inner_vals.update({
                        keys[i]: many2one_vals.id if many2one_vals.id else False
                    })
                    index = index + 1
                    i = i + 1
                elif search_field.ttype == 'date':
                    if  data_column:
                        date_parse = parser.parse(data_column)
                        date_vals = date_parse.strftime("%Y-%m-%d")
                        inner_vals.update({
                        keys[i]: date_vals
                        })
                    index = index + 1
                    i = i + 1
                elif search_field.ttype == 'datetime':
                    if data_column:
                        datetime_parse = parser.parse(data_column)
                        datetime_vals = datetime_parse.strftime("%Y-%m-%d %H:%M:%S")
                        inner_vals.update({
                        keys[i]: datetime_vals
                        })
                    index = index + 1
                    i = i + 1

                else:
                    if keys[i] != False:
                        inner_vals.update({
                                keys[i] : data_column
                            })
                    index = index + 1
                    i = i + 1
            vals.append(inner_vals)
        try:
            custom_entry_obj_line.create(vals)
        except Exception as e:
            raise UserError(e)
    
    