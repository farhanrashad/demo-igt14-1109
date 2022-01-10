# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'

class ResUsers(models.Model):
    _inherit = 'res.users'


class ResPartner(models.Model):
    _inherit = 'res.partner'


class PurchaseRequisitionType(models.Model):
    _inherit = 'purchase.requisition.type'




