# -*- coding: utf-8 -*-
{
    'name': "Training",

    'summary': """
        Employee Training
        1-provide employee training through sessions
        """,

    'description': """
        Employee Training
        1-provide employee training through sessions""",
    'sequence': 1,
    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resource',
    'version': '14.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','mail'],

    # always loaded
    'data': [
        'data/sessions_seq.xml',
        'data/course_seq.xml',
        'data/mail_template_data.xml',
        'security/ir.model.access.csv',
        'views/delivery_method_view.xml',
        'views/sessions_views.xml',
        'views/course_views.xml',
        'views/configuration_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
