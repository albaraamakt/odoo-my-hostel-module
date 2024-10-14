# -*- coding: utf-8 -*-
{
    'name': "My Hostel",  # Module title
    'summary': "Manage Hostel easily",  # Module subtitle phrase
    'description': """
Manage Library
==============
Description related to Hostel.
    """,  # Supports reStructuredText(RST) format
    "version": "17.0.2.0.0",
    "author": "Serpent Consulting Services Pvt. Ltd.",
    "category": "Tools",
    "website": "http://www.serpentcs.com",
    "depends": ['base'],
    "license": "AGPL-3",
    'data': [
        'data/data.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/hostel_room.xml',
        'views/hostel_room_category_view.xml',
        'views/hostel_student_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'demo': [
        'data/demo.xml',
    ]
}
