# -*- coding: utf-8 -*-
# from odoo import http


# class DePurchaseSubscriptionApprovals(http.Controller):
#     @http.route('/de_purchase_subscription_approvals/de_purchase_subscription_approvals/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_purchase_subscription_approvals/de_purchase_subscription_approvals/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_purchase_subscription_approvals.listing', {
#             'root': '/de_purchase_subscription_approvals/de_purchase_subscription_approvals',
#             'objects': http.request.env['de_purchase_subscription_approvals.de_purchase_subscription_approvals'].search([]),
#         })

#     @http.route('/de_purchase_subscription_approvals/de_purchase_subscription_approvals/objects/<model("de_purchase_subscription_approvals.de_purchase_subscription_approvals"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_purchase_subscription_approvals.object', {
#             'object': obj
#         })
