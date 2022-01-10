# -*- coding: utf-8 -*-
{
    'name': "PO Line Fields",
    'summary': """PO Line Fields""",
    'description': """
        PO Line Fields
    """,
    'author': "Dynexcel",
    'website': "https://www.dynexcel.co",
    'sequence':1,
    'category': 'Purchase',
    'version': '14.0.0.2',
    'depends': ['base','stock','purchase','sale','hr', 'product'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/view_po_line_fields.xml',
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
