# -*- coding: utf-8 -*-
{
    'name': "Real Estate",

    'summary': """
        Real Estate module for handling apartments 
        and buildings rental contracts.
        """,

    'description': """
        Real Estate module for handling apartments and buildings 
        rental contracts.
    """,

    'author': "Grand City",
    'website': "https://www.grandcityproperty.de/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/contract.xml',
        'views/building.xml',
        'views/apartment.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}