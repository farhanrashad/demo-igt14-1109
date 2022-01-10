# -*- coding: utf-8 -*-
{
    'name': "Employee Data",

    'summary': """
        Modification of Employee Form.""",

    'description': """
        Modification of Employee Form.
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",

    'category': 'Employee',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'hr_attendance'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/employee_ext.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
