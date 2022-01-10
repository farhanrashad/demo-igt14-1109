# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class MrfTypeCOS(models.Model):
    _name = 'mrf.type.cos'
    
    name = fields.Char('MRF Type Name', required=True)
    cos_mrf_type_id = fields.Char('COS MRF Type ID')
    
    
    
class MrfMovingFromCOS(models.Model):
    _name = 'mrf.moving.from.cos'
     
    name = fields.Char('Moving From Name', required=True)
    cos_moving_from_id = fields.Char('COS Moving From ID')
    
    
class CosTeams(models.Model):
    _name = 'cos.team'
     
    name = fields.Char('Team Name', required=True)
    system_name = fields.Char('System Name')
    cos_team_id = fields.Char('COS Moving From ID')
    
