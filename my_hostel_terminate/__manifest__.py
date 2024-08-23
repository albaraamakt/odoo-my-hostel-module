# -*- coding: utf-8 -*-
{
    'name': "My Hostel Terminate",

    'summary': "Hostel Termination Management",

    'description': """
Long description of module's purpose
    """,

    'author': "Albaraa Maktabi",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['my_hostel'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/hostel_views.xml',
        'views/hostel_room_category_views.xml',
        # 'views/views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],

    'installable': True,
    'application': True,
}

