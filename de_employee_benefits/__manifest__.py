# -*- coding: utf-8 -*-
{
    'name': "Employee Benefits",

    'summary': """
        Employee Benefits
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resource',
    'version': '14.0.0.2',

    # any module necessary for this one to work correctly
    'depends': ['base','hr', 'hr_payroll'],

    # always loaded
    'data': [
        'data/sequence.xml',
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/hr_payslip_views.xml',
        'views/hr_employee_views.xml',
        'views/hr_contract_views.xml',
        'views/contract_type_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
