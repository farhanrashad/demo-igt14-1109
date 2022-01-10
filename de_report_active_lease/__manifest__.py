# -*- coding: utf-8 -*-

{
    "name": "Active Lease Report",
    'version': '14.0.0.2',
    "category": 'Inventory',
    "summary": ' Active Lease Report',
    'sequence': 1,
    "description": """"Active Lease Report """,
    "author": "Dynexcel",
    "website": "https://www.dynexcel.com",
    'depends': ['stock','report_xlsx','de_purchase_subscription_lease','project'],
    'data': [
        'security/ir.model.access.csv',
        'reports/report_active_lease.xml',
        'wizards/report_active_lease_wizard_views.xml',
        #'views/view_stock_transfer_order.xml',
        
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}

