# -*- coding: utf-8 -*-
{
    'name': "Mya Sale Order Stock",

    'summary': """
       Advance Sale Order Stock
       """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Myapps",
    'website': "https://www.yourcompany.com",

    'category': 'Sales/Sales',
    'version': '16.0.1.0.1',

    # any module necessary for this one to work correctly
    'depends': ['trn_sale_order',
                'sale_stock'],
    # always loaded
    'data': [
        'views/product_template_views.xml',
    ],
    'auto_install': True,
    'application': False,
    'installable': True,
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
