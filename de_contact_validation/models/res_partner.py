# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
import collections
import datetime
import hashlib
import pytz
import threading
import re

import requests
from lxml import etree
from random import randint
from werkzeug import urls

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.modules import get_module_resource
from odoo.osv.expression import get_unaccent_wrapper
from odoo.exceptions import UserError, ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _get_default_stage_id(self):
        """ Gives default stage_id """
        category_id = self.env.context.get('default_category_id')
        if not category_id:
            return False
        return self.stage_find(category_id, [('fold', '=', False)])
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_approve', 'To Approve'),
        ('approved', 'Approved'),
    ], string='Status', copy=False, index=True, default='draft')

    stage_id = fields.Many2one('res.partner.stage', string='Stage', readonly=False, ondelete='restrict', tracking=True, index=True, domain="[('category_ids', 'in', category_id)]", copy=False, store=True, compute="_compute_stage_id", default=_get_default_stage_id)
    next_stage_id = fields.Many2one('res.partner.stage',compute='_compute_order_stage')
    prv_stage_id = fields.Many2one('res.partner.stage',compute='_compute_order_stage')
    stage_category = fields.Selection(related='stage_id.stage_category')
    date_submit = fields.Datetime('Submission Date', readonly=False)
    date_approved = fields.Datetime('Approved Date', readonly=False)

    partner_stage_ids = fields.One2many('res.partner.stage.workflow', 'partner_id', string='Stage', copy=True)
    no_edit_mode = fields.Boolean(string='Edit Mode')

    @api.depends('category_id')
    def _compute_stage_id(self):
        for partner in self:
            if partner.category_id:
                if partner.category_id not in partner.stage_id.category_ids:
                    partner.stage_id = partner.stage_find(partner.category_id.ids, [
                        ('fold', '=', False)])
            else:
                partner.stage_id = False
    
    def stage_find(self, section_id, domain=[], order='sequence'):
        """ Override of the base.stage method
            Parameter of the stage search taken from the lead:
            - section_id: if set, stages must belong to this section or
              be a default stage; if not set, stages must be default
              stages
        """
        # collect all section_ids
        section_ids = []
        if section_id:
            section_ids.append(section_id)
        section_ids.extend(self.mapped('category_id').ids)
        search_domain = []
        if section_ids:
            search_domain = [('|')] * (len(section_ids) - 1)
            for section_id in section_ids:
                search_domain.append(('category_ids', '=', section_id))
        search_domain += list(domain)
        # perform search, return the first found
        return self.env['res.partner.stage'].search(search_domain, order=order, limit=1).id
    
    def button_submit(self):
        #self.ensure_one()
        stage_id = False
        for partner in self.sudo():
            group_id = partner.stage_id.group_id
            if group_id:
                if not (group_id & self.env.user.groups_id):
                    raise UserError(_("You are not authorize to submit '%s'.", partner.stage_id.name))
        
        self._compute_partner_stages()
        self.sudo().update({
            'date_submit' : fields.Datetime.now(),
            'stage_id' : self.next_stage_id.id,
            'no_edit_mode': True,
            #'state' : 'to_approve',
        })
        
    def button_confirm(self):
        stage_id = False
        for partner in self.sudo():
            group_id = partner.stage_id.group_id
            if group_id:
                if not (group_id & self.env.user.groups_id):
                    raise UserError(_("You are not authorize to approve '%s'.", partner.stage_id.name))
            
        self.update({
            'date_approved' : fields.Datetime.now(),
            'stage_id' : self.next_stage_id.id,
            #'state': 'approved',
        })
    def button_refuse(self):
        for partner in self.sudo():
            group_id = partner.stage_id.group_id
            if group_id:
                if not (group_id & self.env.user.groups_id):
                    raise UserError(_("You are not authorize to refuse '%s'.", partner.stage_id.name))
                    
        if self.prv_stage_id:
            self.update({
                'stage_id' : self.prv_stage_id.id,
            })
            
    
    def button_draft(self):
        for partner in self.sudo():
            group_id = partner.stage_id.group_id
            if group_id:
                if not (group_id & self.env.user.groups_id):
                    raise UserError(_("You are not authorize to set draft '%s'.", partner.stage_id.name))
                    
        stage_id = self.env['res.partner.stage'].search([('category_ids','in',self.category_id.ids),('stage_category','=','draft')],limit=1)
        self.update({
            'stage_id': stage_id.id,
            'state': 'draft',
        })
        
    def button_cancel(self):
        for partner in self.sudo():
            group_id = partner.stage_id.group_id
            if group_id:
                if not (group_id & self.env.user.groups_id):
                    raise UserError(_("You are not authorize to cancel '%s'.", partner.stage_id.name))
                    
        stage_id = self.env['res.partner.stage'].search([('category_ids','in',self.category_id.ids),('stage_category','=','cancel')],limit=1)
        self.update({
            'stage_id': stage_id.id,
            'state': 'draft',
        })


    def write1(self, vals):
        res = super(ResPartner, self).write(vals)
        raise UserError(_("You are not authorize to change record for approved contact '%s'.", self.stage_id.stage_category))
        #if self.stage_id.stage_category != 'draft':
            #if self.no_edit_mode == True:
                #raise UserError(_("You are not authorize to change record for approved contact '%s'.", self.stage_id.name))
        return res
    #@api.model
    #def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
    def _test(self):
        self = self.with_user(name_get_uid or self.env.uid)
        # as the implementation is in SQL, we force the recompute of fields if necessary
        self.recompute(['display_name'])
        self.flush()
        if args is None:
            args = []
        order_by_rank = self.env.context.get('res_partner_search_mode') 
        if (name or order_by_rank) and operator in ('=', 'ilike', '=ilike', 'like', '=like'):
            self.check_access_rights('read')
            where_query = self._where_calc(args)
            self._apply_ir_rules(where_query, 'read')
            from_clause, where_clause, where_clause_params = where_query.get_sql()
            from_str = from_clause if from_clause else 'res_partner'
            where_str = where_clause and (" WHERE %s AND " % where_clause) or ' WHERE '

            # search on the name of the contacts and of its company
            search_name = name
            if operator in ('ilike', 'like'):
                search_name = '%%%s%%' % name
            if operator in ('=ilike', '=like'):
                operator = operator[1:]

            unaccent = get_unaccent_wrapper(self.env.cr)

            fields = self._get_name_search_order_by_fields()

            query = """SELECT res_partner.id
                         FROM {from_str}
                      {where} ({email} {operator} {percent}
                           OR {display_name} {operator} {percent}
                           OR {reference} {operator} {percent}
                           OR {vat} {operator} {percent})
                           -- don't panic, trust postgres bitmap
                     ORDER BY {fields} {display_name} {operator} {percent} desc,
                              {display_name}
                    """.format(from_str=from_str,
                               fields=fields,
                               where=where_str,
                               operator=operator,
                               email=unaccent('res_partner.email'),
                               display_name=unaccent('res_partner.display_name'),
                               reference=unaccent('res_partner.ref'),
                               percent=unaccent('%s'),
                               vat=unaccent('res_partner.vat'),)

            where_clause_params += [search_name]*3  # for email / display_name, reference
            where_clause_params += [re.sub('[^a-zA-Z0-9]+', '', search_name) or None]  # for vat
            where_clause_params += [search_name]  # for order by
            if limit:
                query += ' limit %s'
                where_clause_params.append(limit)
            self.env.cr.execute(query, where_clause_params)
            
            rtn_ids = [row[0] for row in self.env.cr.fetchall()]
            stage_ids = self.env['res.partner'].search([('state','=','approved')])
            partner_ids = list(set(rtn_ids) & set(stage_ids.ids))
            return partner_ids
#             raise UserError((type(k)))
        return super(ResPartner, self)._name_search(name, args, operator=operator, limit=limit, name_get_uid=name_get_uid)

    def _compute_order_stage(self):
        for partner in self:
            next_stage = prv_stage = False
            for stage in partner.partner_stage_ids.filtered(lambda t: t.stage_id.id == partner.stage_id.id):
                    next_stage = stage.next_stage_id.id
                    prv_stage = stage.prv_stage_id.id
            partner.next_stage_id = next_stage
            partner.prv_stage_id = prv_stage
            
    def _compute_partner_stages(self):
        vals = {}
        stages_list = []
        next_stage = prv_stage = False
        for partner in self:
            stage_ids = self.env['res.partner.stage'].search([('category_ids', '=', partner.category_id.id)])
            for stage in stage_ids:
                vals = {
                    'partner_id': partner.id,
                    'stage_id': stage.id,
                }
                stages_list.append({
                    'partner_id': partner.id,
                    'stage_id': stage.id, 
                    'sequence': stage.sequence,
                })
            
            partner.partner_stage_ids.create(stages_list)
            #order.order_stage_ids = lines_data
            #===================================
            #++++++++Assign Next Stage++++++++++++++
            stages = self.env['res.partner.stage.workflow'].search([('partner_id','=', partner.id)], order="sequence desc")
            for stage in stages:
                stage.update({
                    'next_stage_id': next_stage,
                })
                next_stage = stage.stage_id.id
            #++++++++++++++++++++++++++++++++++++++++
            #+++++++++++Assign Previous Stage++++++++++
            stages = self.env['res.partner.stage.workflow'].search([('partner_id','=', partner.id)], order="sequence asc")
            for stage in stages:
                stage.update({
                    'prv_stage_id': prv_stage,
                })
                prv_stage = stage.stage_id.id
            #for order in order.order_stage_ids.sorted(key=lambda r: r.sequence):
                
class PartnerStage(models.Model):
    _name = 'res.partner.stage.workflow'
    _description = 'Partner Stage Workflows'
    _order = 'sequence'
    
    partner_id = fields.Many2one('res.partner', string='Partner', index=True, required=True, ondelete='cascade')
    
    stage_id = fields.Many2one('res.partner.stage', string='Stage', readonly=False, ondelete='restrict', tracking=True, index=True, copy=False)
    sequence = fields.Integer(string='Sequence')
    next_stage_id = fields.Many2one('res.partner.stage', string='Next Stage', readonly=False, ondelete='restrict', tracking=True, index=True, copy=False)
    prv_stage_id = fields.Many2one('res.partner.stage', string='Previous Stage', readonly=False, ondelete='restrict', tracking=True, index=True, copy=False)