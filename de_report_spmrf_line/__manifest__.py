# -*- coding: utf-8 -*-

{
    "name": "SPMRF Line Report",
    'version': '14.0.0.2',
    "category": 'Inventory',
    "summary": ' SPMRF Line Report',
    'sequence': 1,
    "description": """"SPMRF Line Report """,
    "author": "Dynexcel",
    "website": "https://www.dynexcel.com",
    'depends': ['stock','report_xlsx','de_stock_material_transfer','project','de_secondary_currency'],
    'data': [
        'security/ir.model.access.csv',
        'reports/report_spmrf_line.xml',
        'wizards/report_spmrf_line_views.xml',
        #'views/view_stock_transfer_order.xml',
        
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}

