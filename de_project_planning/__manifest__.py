# -*- coding: utf-8 -*-
{
    'name': "Project Planning & Control",

    'summary': """
          Project Planning & Control
           """,

    'description': """
          Project Planning & Control
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",
    'category': 'project',
    'version': '14.0.5.2',

    'depends': ['base', 'mail', 'note','project','purchase','purchase_requisition','stock','account','de_base_address_extended'],

    # always loaded
    'data': [

        'security/ir.model.access.csv',
        'views/menu_item.xml',
        'views/product_views.xml',
        'views/note_views.xml',
        'views/stock_location_views.xml',
        #'views/stock_move_views.xml',
        #'views/purchase_requisition_views.xml',
        'views/project_views.xml',
        'views/job_order_views.xml',
        'views/purchase_views.xml',
        'views/account_views.xml',
        'views/purchase_agreement_views.xml',
        'views/stock_views.xml',
        
        
        #'views/con_materials_boq.xml',
        
        #'views/con_vendor.xml',
        #'views/con_project_notes.xml',
        #'views/con_boq.xml',
        #'views/con_job_order_notes.xml',
        

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
