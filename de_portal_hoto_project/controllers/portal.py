# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import OrderedDict
from operator import itemgetter
from odoo.exceptions import UserError
from datetime import date, datetime, timedelta
from odoo import http, _, fields
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.tools import groupby as groupbyelem
import base64
from odoo.osv.expression import OR

def hoto_site_page_content(flag = 0):
    partners = request.env['res.users'].sudo().search([('id','=',http.request.env.context.get('uid'))])
    projects = request.env['project.project'].sudo().search([('name','=','HOTO')])
    sites = request.env['project.project'].sudo().search([('allow_site_planning','=',True)])
    return {
        'partners': partners,
        'projects': projects,
        'sites': sites,
        'success_flag' : flag,
    }



class CreateHotoTask(http.Controller):
    @http.route('/hoto/task/create/',type="http", website=True, auth='user')
    def hoto_task_create_template(self, **kw):
       return request.render("de_portal_hoto_project.hoto_site_task_Create", hoto_site_page_content())
    
    
    @http.route('/hoto/task/save', type="http", auth="public", website=True)
    def hoto_task_save(self, **kw):
        if not kw.get('project_id'):
            raise UserError('You Are Not Allow to access HOTO Project!')
        if not kw.get('site_id'):
            raise UserError('You Are Not Allow to access any Site Project!') 
        hotosite = request.env['project.project'].sudo().search([('id','=',int(kw.get('site_id')))], limit=1)
        if str(kw.get('date_handover')) < str(fields.date.today() - timedelta(3)):
            if kw.get('hoto_type') == 'new':
                raise UserError('you cannot submit the request!.Only Allow to submit Handover Date Between. '+str((fields.date.today() - timedelta(4)).strftime('%m/%d/%y'))+' to '+str((fields.date.today()).strftime('%m/%d/%y'))) 
        elif str(kw.get('date_handover')) > str(fields.date.today()):
            if kw.get('hoto_type') == 'new':
                raise UserError('you cannot submit the request!.Only Allow to submit Handover Date Between. '+str((fields.date.today() - timedelta(4)).strftime('%m/%d/%y'))+' to '+str((fields.date.today()).strftime('%m/%d/%y'))) 
            
        
        vals = {
            'name': 'HOTO',
            'partner_id': int(kw.get('partner_id')),
            'project_id': int(kw.get('project_id')),
            'site_id': int(kw.get('site_id')),
            'site_hoto': True,
            'hoto_type': kw.get('hoto_type'),
            'date_handover': kw.get('date_handover'),
        }
        task = request.env['project.task'].sudo().create(vals)
        if kw.get('attachment'):
            Attachments = request.env['ir.attachment']
            name = kw.get('attachment').filename
            file = kw.get('attachment')
            attachment_id = Attachments.sudo().create({
                'name': name,
                'res_id': task.id,
                'res_name': task.name,
                'res_model': 'project.task',
                'type': 'binary',
                'datas': base64.b64encode(file.read()),
            })
        return request.render('de_portal_hoto_project.hoto_submited', {})

class CustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'hoto_count' in counters:
            active_user = request.env['res.users'].sudo().search([('id','=',http.request.env.context.get('uid'))])    
            values['hoto_count'] = request.env['project.task'].sudo().search_count([('partner_id','=', active_user.partner_id.id)])
        return values

   
    # ------------------------------------------------------------
    # My Task
    # ------------------------------------------------------------
    def _hoto_site_task_get_page_view_values(self, hoto_task, access_token, **kwargs):
        values = {
            'page_name': 'hoto_task',
            'hoto_task': hoto_task,
            'user': request.env.user
        }
        return self._get_page_view_values(hoto_task, access_token, values, 'hoto_tasks_history', False, **kwargs)

    @http.route(['/hoto/tasks', '/hoto/tasks/page/<int:page>'], type='http', auth="user", website=True)
    def portal_hoto_tasks(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None, search=None, search_in='content', groupby=None, **kw):
        values = self._prepare_portal_layout_values()
        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Title'), 'order': 'name'},
            'stage': {'label': _('Stage'), 'order': 'stage_id, project_id'},
            'project': {'label': _('Project'), 'order': 'project_id, stage_id'},
            'update': {'label': _('Last Stage Update'), 'order': 'date_last_stage_update desc'},
        }
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
        }
        searchbar_inputs = {
            'content': {'input': 'content', 'label': _('Search <span class="nolabel"> (in Content)</span>')},
            'message': {'input': 'message', 'label': _('Search in Messages')},
            'customer': {'input': 'customer', 'label': _('Search in Customer')},
            'stage': {'input': 'stage', 'label': _('Search in Stages')},
            'project': {'input': 'project', 'label': _('Search in Project')},
            'all': {'input': 'all', 'label': _('Search in All')},
        }
        searchbar_groupby = {
            'none': {'input': 'none', 'label': _('None')},
            'project': {'input': 'project', 'label': _('Project')},
            'stage': {'input': 'stage', 'label': _('Stage')},
        }

        # extends filterby criteria with project the customer has access to
        projects = request.env['project.project'].sudo().search([('name','=','HOTO')])
        for project in projects:
            searchbar_filters.update({
                str(project.id): {'label': project.name, 'domain': [('project_id', '=', project.id)]}
            })

        # extends filterby criteria with project (criteria name is the project id)
        # Note: portal users can't view projects they don't follow
        project_groups = request.env['project.task'].read_group([('project_id', '!=', projects.id)],
                                                                ['project_id'], ['project_id'])
        for group in project_groups:
            proj_id = group['project_id'][0] if group['project_id'] else False
            proj_name = group['project_id'][1] if group['project_id'] else _('Others')
            searchbar_filters.update({
                str(proj_id): {'label': proj_name, 'domain': [('project_id', '=', proj_id)]}
            })

        # default sort by value
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        # default filter by value
        if not filterby:
            filterby = 'all'
        domain = searchbar_filters.get(filterby, searchbar_filters.get('all'))['domain']

        # default group by value
        if not groupby:
            groupby = 'project'

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
            if search_in in ('project', 'all'):
                search_domain = OR([search_domain, [('project_id', 'ilike', search)]])
            domain += search_domain
            
        active_user = request.env['res.users'].sudo().search([('id','=',http.request.env.context.get('uid'))])    
        domain += [('project_id.name','=','HOTO')]
        domain += [('partner_id', '=', active_user.partner_id.id)]
        # task count
        task_count = request.env['project.task'].sudo().search_count(domain)
        # pager
        pager = portal_pager(
            url="/hoto/tasks",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby, 'filterby': filterby, 'groupby': groupby, 'search_in': search_in, 'search': search},
            total=task_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        if groupby == 'project':
            order = "project_id, %s" % order  # force sort on project first to group by project in view
        elif groupby == 'stage':
            order = "stage_id, %s" % order  # force sort on stage first to group by stage in view

        tasks = request.env['project.task'].sudo().search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['hoto_tasks_history'] = tasks.ids[:100]

        
        grouped_tasks = [tasks]

        values.update({
            'date': date_begin,
            'date_end': date_end,
            'grouped_tasks': grouped_tasks,
            'page_name': 'Hoto Task',
            'default_url': '/hoto/tasks',
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
        return request.render("de_portal_hoto_project.portal_hoto_site_tasks", values)

    @http.route(['/hoto/task/<int:task_id>'], type='http', auth="public", website=True)
    def portal_hoto_task(self, task_id, access_token=None, **kw):
        try:
            task_sudo = request.env['project.task'].sudo().search([('id', '=', task_id)])
        except (AccessError, MissingError):
            return request.redirect('/my')

        # ensure attachment are accessible with access token inside template
        for attachment in task_sudo.attachment_ids:
            attachment.generate_access_token()
        values = self._hoto_site_task_get_page_view_values(task_sudo, access_token, **kw)
        return request.render("de_portal_hoto_project.portal_hoto_task", values)
