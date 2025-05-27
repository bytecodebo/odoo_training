# -*- coding: utf-8 -*-
{
    'name': "Mya Sale Order",

    'summary': """
       Advance Sale Order
       """,

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    'category': 'Sales/Sales',
    'version': '16.0.1.0.1',

    # any module necessary for this one to work correctly
    'depends': ['trn_partner_advance',
                'sale_management'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
