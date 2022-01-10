# -*- coding: utf-8 -*-
{
    'name': "Account Approvals",

    'summary': """
        Account Approvals
        """,

    'description': """
Account Approvals
====================================== 
        1- define Approvals on each journal type
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '14.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['de_multi_level_approvals','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_journal_views.xml',
        'views/approval_request_views.xml',
        'views/approval_approver_views.xml',
        'views/account_move_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
