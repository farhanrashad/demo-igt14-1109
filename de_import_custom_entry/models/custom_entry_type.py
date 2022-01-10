# -*- coding: utf-8 -*-

import base64

from odoo import api, fields, models, tools, _
from odoo.modules.module import get_module_resource
from random import randint

class CustomEntryType(models.Model):
    _inherit = 'account.custom.entry.type'
    
    csv_import_template_id = fields.Many2many('ir.attachment', relation="files_rel_custom_entry_type_csv_import_template", column1="csv_import_doc_id", column2="attachment_id", string="CSV Import Template")
    excel_import_template_id = fields.Many2many('ir.attachment', relation="files_rel_custom_entry_type_excel_import_template", column1="excel_import_doc_id", column2="attachment_id", string="Excel Import Template")
    
    #csv_import_template_id = fields.Binary(string='CSV Import File')


