# -*- coding: utf-8 -*-

{
    "name": "MRF Report",
    'version': '14.0.0.0',
    "category": 'MRF REPORT FOR REQUISITION MODULE',
    "summary": ' MRF Report',
    'sequence': 1,
    "description": """"Generate MRF Report """,
    "author": "Dynexcel",
    "website": "http://www.dynexcel.co",
    'depends': ['base','stock','purchase','hr','de_stock_material_transfer'],
    'data': [
        'views/view_stock_transfer_order.xml',
        'reports/mrf_report.xml',
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}

