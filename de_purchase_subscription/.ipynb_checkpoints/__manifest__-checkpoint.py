# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": "Purchase Subscription",
    "category": 'Purchase',
    "summary": 'Purchase Subscription',
    "description": """
    Purchase Subscription
    """,
    "sequence": 1,
    "author": "Dynexcel",
    "website": "https://www.dynexcel.com",
    "version": '14.0.2.3',
    "depends": ['account'],
    "data": [
        'security/security.xml',
        'security/ir.model.access.csv',
        #'data/data.xml',
        'data/sequence.xml',
        'views/subscription_menus.xml',
        'views/product_views.xml',
        'views/account_move_views.xml',
        'views/purchase_subscription_stage_views.xml',
        'views/purchase_subscription_plan_views.xml',
        'views/purchase_subscription_type_views.xml',
        'views/purchase_subscription_views.xml',
        'report/purchase_subscription_report_views.xml',
    ],
    
    "price": 55,
    "currency": 'EUR',
    "installable": True,
    "application": False,
    "auto_install": False,
}
