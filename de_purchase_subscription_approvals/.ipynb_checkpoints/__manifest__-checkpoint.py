# -*- coding: utf-8 -*-
{
    'name': "Purchase Subscription Approvals",

    'summary': """
        Purchase Subscription Approvals
        """,

    'description': """
        Purchase Subscription Approvals 
        1- Multi Level Approvals
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",
    'category': 'Purchase/Subscription',
    'version': '14.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','approvals','de_purchase_subscription'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/purchase_subscription_type_views.xml',
        'views/approval_approver_views.xml',
        'views/approval_request_views.xml',
        'views/purchase_subscription_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
