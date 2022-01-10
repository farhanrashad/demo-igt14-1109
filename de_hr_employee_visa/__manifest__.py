# -*- coding: utf-8 -*-
{
    'name': "Employee Visa",

    'summary': """
        Employee passport and visa Information""",

    'description': """
        Employee visa
    """,

    'author': "Dynexcel",
    'website': "http://www.Dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resource',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base' , 'hr'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/hr_visa_seq.xml',
        'data/data.xml',
        'views/employee_visa_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
