# -*- coding: utf-8 -*-

{
    "name": "Lease Agreement Report",
    'version': '14.0.0.2',
    "category": 'Inventory',
    "summary": ' Lease Agreement Report',
    'sequence': 1,
    "description": """"Lease Agreement Report """,
    "author": "Dynexcel",
    "website": "https://www.dynexcel.com",
    'depends': ['stock','report_xlsx','de_purchase_subscription_lease','project'],
    'data': [
        'security/ir.model.access.csv',
        'reports/report_lease_agreement.xml',
        'wizards/report_lease_agreement_wizard_views.xml',
        #'views/view_stock_transfer_order.xml',
        
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}

