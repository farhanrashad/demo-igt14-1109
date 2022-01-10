# -*- coding: utf-8 -*-
{
    'name': "Partner Filter",

    'summary': """
    Purchase Partner Filter
        """,

    'description': """
        Purchase Partner Filter
    """,

    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",

    'category': 'Purchase',
    'version': '14.0.0.3',

    # any module necessary for this one to work correctly
    'depends': ['purchase','purchase_requisition'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        #'views/purchase_views.xml',
        'wizard/purchase_agreement_wizard_views.xml',
        'views/purchase_requisition_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
