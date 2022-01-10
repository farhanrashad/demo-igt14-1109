# -*- coding: utf-8 -*-

{
    "name": "Lease Due Payment Report",
    'version': '14.0.0.4',
    "category": 'Purchase',
    "summary": ' Lease Due Payment Report',
    'sequence': 1,
    "description": """"Lease Due Payment Report """,
    "author": "Dynexcel",
    "website": "https://www.dynexcel.com",
    'depends': ['stock','report_xlsx','de_purchase_subscription_lease','de_operations'],
    'data': [
        'security/ir.model.access.csv',
        'reports/report_la_due.xml',
        'wizards/report_la_due_wizard_views.xml',
        #'views/view_stock_transfer_order.xml',
        
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}

