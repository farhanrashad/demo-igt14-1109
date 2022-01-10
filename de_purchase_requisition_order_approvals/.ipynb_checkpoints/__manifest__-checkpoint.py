# -*- coding: utf-8 -*-
{
    'name': "Purchase Agreement Approvals",
    'summary': """
    Approvals integration for purcahse agreement
        """,
    'description': """
Purchase Agreement Approvals
============================================
1 - Approvals
    """,

    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",
    'category': 'Purchase',
    'version': '14.0.0.2',
    'depends': ['approvals','de_purchase_requisition_type'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/purchase_requisition_type_views.xml',
        'views/approval_request_views.xml',
        'views/approval_approver_views.xml',
        'views/purchase_views.xml',
    ],
}
