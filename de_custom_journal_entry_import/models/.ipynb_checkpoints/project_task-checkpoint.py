# -*- coding: utf-8 -*-

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

MONTH_LIST = [('1', 'Jan'), ('2', 'Feb'), ('3', 'Mar'), ('4', 'Apr'), ('5', 'May'), ('6', 'Jun'), ('7', 'Jul'), ('8', 'Aug'), ('9', 'Sep'), ('10', 'Oct'), ('11', 'Nov'),('12', 'Dec')]

import logging
_logger = logging.getLogger(__name__)
import io
try:
    import xlrd
except ImportError:
    _logger.debug('Cannot `import xlrd`.')
try:
    import csv
except ImportError:
    _logger.debug('Cannot `import csv`.')
try:
    import xlwt
except ImportError:
    _logger.debug('Cannot `import xlwt`.')
try:
    import cStringIO
except ImportError:
    _logger.debug('Cannot `import cStringIO`.')
try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')


class ProjectProject(models.Model):
    _inherit = 'project.project'


class ProjectTask(models.Model):
    _inherit = 'project.task'


    entry_attachment_id = fields.Many2many('ir.attachment', relation="files_rel_project_task_entry",
                                            column1="doc_id",
                                            column2="attachment_id",
                                            string="Entry Attachment")


    custom_entry_type_id = fields.Many2one('account.custom.entry.type', string='Entry Type')
    entry_partner_id = fields.Many2one('res.partner', string='Contractor')
    custom_entry_id = fields.Many2one('account.custom.entry', string='Entry')
    is_entry_attachment = fields.Boolean(string='Is Entry Attachment')
    is_entry_processed = fields.Boolean(string='Entry Processed')
    un_processed_entry = fields.Boolean(string='Un-Processed Entry')
    reference = fields.Char(string='Reference')
    supplier_bill_ref = fields.Char(string='Supplier Bill Ref') 
    date_entry_year = fields.Char(string='Entry Year')
    date_entry_month = fields.Selection(MONTH_LIST, string='Month')

    f_duration_from = fields.Date(string='Duration From')
    f_duration_to = fields.Date(string='Duration To')
    customer_type = fields.Selection([('local', 'Local'), ('expat', 'Expat')], string='Customer Type')
    date_effective = fields.Date(string='Effective Date')
    date_subscription = fields.Date(string='Date of Subscription')
    currency_id = fields.Many2one('res.company', string='Currency')
    t_travel_by = fields.Selection([
        ('ticket', 'Flight Ticket'),
        ('Vehicle', 'Vehicle Rental')],
        string='Travel By', default='ticket') 
    

    @api.constrains('entry_attachment_id')
    def _check_attachment(self):
        if self.entry_attachment_id:
            self.is_entry_attachment = True
            self.un_processed_entry = True
        if self.is_entry_attachment == True:
            self.action_journal_entry_import()

	
    def action_journal_entry_import(self):
        keys = []
        ir_model_fields_obj = self.env['ir.model.fields']
        custom_entry_obj = self.env['account.custom.entry']
        custom_entry_obj_line = self.env['account.custom.entry.line']

        for custom in self:
            if custom.is_entry_processed == False:
                counter = 1
                try:
                    file = str(base64.decodebytes(custom.entry_attachment_id.datas).decode('utf-8'))
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
                attachment_vals = {
                     'name': custom.entry_attachment_id.name,
                     'type': 'binary',
                     'datas':  custom.entry_attachment_id.datas, 
                }
                attachment = self.env['ir.attachment'].create(attachment_vals)
                custom_entry_id_vals = self.custom_entry_id.id
                if self.custom_entry_id:
                    custom_entry_id_vals = self.custom_entry_id.id
                    entry = self.env['account.custom.entry'].search([('id','=', self.custom_entry_id.id)])
                    for entry_line in entry.custom_entry_line:
                        entry_line.unlink()
                    custom.custom_entry_id.is_custom_entry_import = False
                    custom.custom_entry_id.correction_reason = ' ' 
                    custom.custom_entry_id.update({
                           'entry_attachment_id'  : [[6, 0, attachment.ids]],
                           'ref': custom.reference,
                           'supplier_bill_ref': custom.supplier_bill_ref,
                           'date_entry_year': custom.date_entry_year,
                           'date_entry_month':  custom.date_entry_month,
                           'description': custom.description, 
                           })
                    if   custom.reference :
                        custom.custom_entry_id.update({       
                           'ref': custom.reference,
                           })
                    if   custom.supplier_bill_ref :
                        custom.custom_entry_id.update({  
                           'supplier_bill_ref': custom.supplier_bill_ref,
                           })
                    if   custom.date_entry_year :
                        custom.custom_entry_id.update({   
                           'date_entry_year': custom.date_entry_year,
                           })
                    if   custom.date_entry_month :
                        custom.custom_entry_id.update({   
                           'date_entry_month':  custom.date_entry_month,
                           }) 
                    if   custom.description :
                        custom.custom_entry_id.update({   
                           'description': custom.description, 
                           })
                    if   custom.customer_type :
                        custom.custom_entry_id.update({   
                           'customer_type': custom.customer_type, 
                           }) 
                    if   custom.t_travel_by :
                        custom.custom_entry_id.update({   
                           'description': custom.t_travel_by, 
                           }) 
                    if   custom.f_duration_from :
                        custom.custom_entry_id.update({   
                           'description': custom.f_duration_from, 
                           }) 
                    if   custom.f_duration_to :
                        custom.custom_entry_id.update({   
                           'description': custom.f_duration_to, 
                           }) 
                    if   custom.date_effective :
                        custom.custom_entry_id.update({   
                           'description': custom.date_effective, 
                           })     
                    if   custom.date_subscription :
                        custom.custom_entry_id.update({   
                           'description': custom.date_subscription, 
                           })     
                    
                    
                                              
                else:    
                    partner = custom.entry_partner_id.id
                    user = custom.user_id.id
                    entry_stage = self.env['account.custom.entry.stage'].search([('stage_category', '=', 'draft')])
                    entry_id = 0
                    entry_id = self.env['account.custom.entry.stage'].search([('stage_category', '=', 'draft')], limit=1).id
                    for entry in entry_stage:
                        if entry.custom_entry_type_ids:
                            if self.custom_entry_type_id.id in entry.custom_entry_type_ids.ids:
                                entry_id = entry.id
                            for group in entry.group_id.users:
                                if group.id == self.env.uid:
                                    entry_id = entry.id

                    name_seq = self.custom_entry_type_id.name 
                    if self.custom_entry_type_id.automated_sequence == True:
                        name_seq = self.custom_entry_type_id.sequence_id.next_by_id()         
                    custom_vals = {
                        'name':  name_seq, 
                        'date_entry': fields.datetime.now(),
                        'partner_id': partner,
                        'currency_id': custom.currency_id.id,
                        'company_id': self.env.company.id,
                        'entry_attachment_id': [[6, 0, attachment.ids]],
                        'ref': custom.reference,
                        'supplier_bill_ref': custom.supplier_bill_ref,
                        'date_entry_year': custom.date_entry_year,
                        'date_entry_month':  custom.date_entry_month,
                        'description': custom.description, 
                        'customer_type': custom.customer_type,
                        't_travel_by':  custom.t_travel_by,
                        'f_duration_from': custom.f_duration_from, 
                        'f_duration_to': custom.f_duration_to,
                        'date_effective':  custom.date_effective,
                        'date_subscription': custom.date_subscription,
                        'user_id': user,
                        'stage_id': entry_id,
                        'custom_entry_type_id': self.custom_entry_type_id.id,
                    }
                    custom_entry = self.env['account.custom.entry'].create(custom_vals)
                    custom_entry_id_vals = custom_entry.id
                for data_row in file_reader:
                    inner_vals = {}
                    index = 0
                    i = 0
                    for data_column in data_row:
#                         raise UserError(str(custom_entry.id))
                        inner_vals.update({
                            'custom_entry_id': custom_entry_id_vals
                        })
                        rowvals.append(data_row)
                        search_field = ir_model_fields_obj.sudo().search([
                            ("model", "=", "account.custom.entry.line"),
                            ("name", "=", keys[i]),
                        ], limit=1)
                        if search_field.ttype == 'many2one' and search_field.name == 'car_details':

                            many2one_vals = self.env[str(search_field.relation)].search([('display_name','=',data_column)], limit=1)

                            inner_vals.update({
                                keys[i]: many2one_vals.id
                            })
                            index = index + 1
                            i = i + 1
                        elif search_field.ttype == 'many2one':

                            many2one_vals = self.env[str(search_field.relation)].search([('name','=',data_column)], limit=1)

                            inner_vals.update({
                                keys[i]: many2one_vals.id
                            })
                            index = index + 1
                            i = i + 1
                        elif search_field.ttype == 'date':
                            date_parse = parser.parse(data_column)
                            date_vals = date_parse.strftime("%Y-%m-%d")
                            inner_vals.update({
                                keys[i]: date_vals
                            })
                            index = index + 1
                            i = i + 1
                        elif search_field.ttype == 'datetime':
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
                custom.is_entry_processed = True
                custom.un_processed_entry = False
                custom.user_id = self.env.user.id


class CustomEntryType(models.Model):
    _inherit = 'account.custom.entry.type'
    
class IrAttachment(models.Model):
    _inherit = 'ir.attachment'   
    
    
class ResGroups(models.Model):
    _inherit = 'res.groups' 
    
class ResCurrency(models.Model):
    _inherit = 'res.currency'     

