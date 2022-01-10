import base64
import hashlib
import itertools
import logging
import mimetypes
import os
import re
from collections import defaultdict
import uuid
from odoo import api, fields, models, tools, _
from odoo.exceptions import AccessError, ValidationError, MissingError, UserError
from odoo.tools import config, human_size, ustr, html_escape
from odoo.tools.mimetypes import guess_mimetype
import pandas as pd
from csv import DictReader
from csv import DictWriter
import csv

_logger = logging.getLogger(__name__)


class AccountCustomEntry(models.Model):
    _inherit = 'account.custom.entry'
    
    is_custom_entry_import = fields.Boolean(string='Update Entry')
    entry_attachment_id = fields.Many2many('ir.attachment', relation="files_rel_account_custom_entry",
                                            column1="doc_id",
                                            column2="entry_attachment_id",
                                            string="Entry Attachment")
    
    def action_generate_excel(self):
        for custom in self:
            filename = str(custom.name)+".csv"
            entry = open(filename + str(), 'w')
            entry.close()
            technical_fields = []
            fields_label = []
            header_fields = {}
            final_data = []
            fields = custom.custom_entry_type_id.entry_template_fields
            fields_list = ' '
            if fields:
                fields_str = str(fields)
                fields_list = fields_str.split('|')
            for field in fields_list:
                model_fields = self.env['ir.model.fields'].search([('field_description','=', field)], limit=1)
                if model_fields:
                    technical_fields.append(model_fields.name)
                    fields_label.append(model_fields.field_description)
            for head in fields_label:
                header_fields.update({
                    head: head
                }) 
            for entry_line in custom.custom_entry_line:
                line_vals_list = ' '
                if entry_line.line_vals:
                    line_vals_list = entry_line.line_vals.split('|')
                    index = 0
                    final_vals = {}
                    for entry_vals in line_vals_list:
                        final_vals.update({
                            fields_label[index] : entry_vals
                            })
                        index += 1
                    final_data.append(final_vals)  

            with open(filename, 'a') as file:

                writer = csv.DictWriter(file, fieldnames=fields_label)
                writer.writerow(header_fields)
                for line in final_data:
                    writer.writerow(line)

            with open(filename) as f:
                read_file = f.read()

                attachment_vals = {
                        'name': filename,
                        'type': 'binary',
                        'datas': base64.b64encode(read_file.encode('utf8')),
                }
                attach_file = self.env['ir.attachment'].create(attachment_vals)
                if attach_file:
                    custom.update({
                        'entry_attachment_id': [[6, 0, attach_file.ids]],
                    })


    
class AccountCustomEntryLine(models.Model):
    _inherit = 'account.custom.entry.line'  
    
    
    line_vals = fields.Char(string='Line Vals')
        