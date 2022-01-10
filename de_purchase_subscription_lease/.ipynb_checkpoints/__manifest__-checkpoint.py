# -*- coding: utf-8 -*-
{
    'name': "Purchase Subscription (Lease)",

    'summary': """
        Purchase Subscription Lease
        """,

    'description': """
        Purchae Subscription
    """,

    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Purchase',
    'version': '14.0.0.9',

    # any module necessary for this one to work correctly
    'depends': ['de_purchase_subscription','project'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/purchase_subscription_plan_wizard_views.xml',
        'views/purchase_subscription_views.xml',
        'views/res_partner_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
