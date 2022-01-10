# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from datetime import date

class SaleSubscription(models.Model):
    _inherit = 'sale.subscription.agreement'
    
    def _get_default_stage_id(self):
        subscription_type_id = self.env.context.get('default_subscription_type_id')
        if not subscription_type_id:
            return False
        return self.stage_find(subscription_type_id, [('fold', '=', False), ('is_closed', '=', False)])
    
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        search_domain = [('id', 'in', stages.ids)]
        if 'default_subscription_type_id' in self.env.context:
            search_domain = ['|', ('subscription_type_id', '=', self.env.context['default_subscription_type_id'])] + search_domain

        stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    
    subscription_type_id = fields.Many2one('sale.subscription.agreement.type', string='Subscription Type',
                                           required=True, help="The subscription type categories agreement.",)
    
    #stage_id = fields.Many2one('purchase.subscription.type', string='Stage', compute='_compute_stage_id',
     #                          store=True, readonly=False, ondelete='restrict', tracking=True, index=True,     
      #                         default=_get_default_stage_id, group_expand='_read_group_stage_ids',
       # domain="[('subscription_type_id', '=', subscription_type_id)]", copy=False)

    
    @api.depends('subscription_type_id')
    def _compute_stage_id(self):
        for subscription in self:
            if subscription.subscription_type_id:
                if subscription.subscription_type_id not in subscription.stage_id.subscription_type_id:
                    subscription.stage_id = subscription.stage_find(subscription.subscription_type_id.id, [
                        ('fold', '=', False), ('is_closed', '=', False)])
            else:
                stage_find.stage_id = False