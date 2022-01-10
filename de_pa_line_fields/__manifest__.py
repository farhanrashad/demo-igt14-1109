# -*- coding: utf-8 -*-
{
    'name': "PA Line Fields",
    'summary': """PA Line Fields""",
    'description': """
        PA Line Fields
    """,
    'author': "Dynexcel",
    'website': "https://www.dynexcel.co",
    'sequence':1,
    'category': 'Purchase',
    'version': '14.0.0.2',
    'depends': ['base','stock','purchase','sale','hr', 'product'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/view_pa_line_fields.xml',
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
