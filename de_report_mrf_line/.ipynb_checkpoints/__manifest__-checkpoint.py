# -*- coding: utf-8 -*-

{
    "name": "MRF Line Report",
    'version': '14.0.0.2',
    "category": 'Inventory',
    "summary": ' MRF Line Report',
    'sequence': 1,
    "description": """"MRF Line Report """,
    "author": "Dynexcel",
    "website": "https://www.dynexcel.com",
    'depends': ['stock','report_xlsx','de_stock_material_transfer','project','de_secondary_currency'],
    'data': [
        'security/ir.model.access.csv',
        'reports/report_mrf_line.xml',
        'wizards/report_mrf_line_views.xml',
        #'views/view_stock_transfer_order.xml',
        
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}

