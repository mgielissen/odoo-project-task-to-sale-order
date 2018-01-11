# -*- coding: utf-8 -*-
{
    'name': "Project Task Convert to Sale Order",

    'summary': """
        Project Task Convert to Sale Order
    """,

    'author': "Andreas Wyrobek",
    'website': "http://www.cytex.cc",

    'category': 'Administration',
    'version': '0.1',

    'license': 'OPL-1',

    #'images': ['images/main_screenshot.png'],

    # any module necessary for this one to work correctly
    'depends': ['base', 'project', 'sale'],

    # always loaded
    'data': [
        'views/templates.xml',
        'views/views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [],

    'installable': True,
    'application': True,
    'auto_install': False,
}
