# -*- coding: utf-8 -*-
{
    'name': "Purchase Order Approvals",
    'summary': """
    Approvals integration for purcahse Order
        """,
    'description': """
Purchase Order Approvals
============================================
1 - Approvals
    """,

    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",
    'category': 'Purchase',
    'version': '14.0.0.1',
    'depends': ['approvals','purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_order_type_views.xml',
        'views/approval_request_views.xml',
        'views/approval_approver_views.xml',
        'views/purchase_order_views.xml',
    ],
}
