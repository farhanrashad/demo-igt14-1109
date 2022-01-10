# -*- coding: utf-8 -*-
{
    'name': "Master Service Agreement",

    'summary': """
        Master Service Agreement
        Telecom Billing
        """,

    'description': """
        Master Service Agreement
        - Telecom Billing
    """,

    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",
    'category': 'Sale',
    'version': '14.0.2.1',

    'depends': ['base','product','de_project_planning','account','contacts','account_asset','de_purchase_subscription_lease'],

    'data': [
        'security/msa_security.xml',
        'security/ir.model.access.csv',
        'views/master_service_agreement_view.xml',
        'views/billing_info_view.xml',
        'views/monthly_models_view.xml',
        'views/sla_factor_views.xml',
        'views/wind_factor_views.xml',
        'views/product_view.xml',
        'views/project_views.xml',
        'views/account_move_view.xml',
        'views/msa_menu.xml',
        'views/account_asset_views.xml',
        'views/purchase_subscription_views.xml',
#         'report/employee_report_pdf.xml',
    ],
    "price": 25,
    "currency": 'EUR',
    "installable": True,
    "application": True,
    "auto_install": False,
}
