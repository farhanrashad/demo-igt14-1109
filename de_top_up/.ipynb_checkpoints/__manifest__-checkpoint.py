# -*- coding: utf-8 -*-
{
    'name': "Top Up",
    'summary': """Employee Training App Modification""",
    'description': """ """,
    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",
    'category': 'Human Resource',
    'version': '14.0.0.2',
    'depends': ['base', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/request_view.xml',
        'views/hr_employee_views.xml',
        'data/topup_data.xml',
        'views/balance_views.xml',
        'views/top_up_menu.xml',
        'views/reporting_balance.xml',
        'views/reporting_request.xml',

    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
