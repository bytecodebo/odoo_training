# -*- coding: utf-8 -*-
{
    'name': "Mya Sale Order",

    'summary': """
       Advance Sale Order
       """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Myapps",
    'website': "https://www.yourcompany.com",

    'category': 'Sales/Sales',
    'version': '16.0.1.0.1',

    # any module necessary for this one to work correctly
    'depends': ['trn_partner_advance',
                'sale_management'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/data_sale_order.xml',
        'views/res_config_views.xml',
        'wizard/wizard_sale_order_demos.xml',
        'views/sale_order_views.xml',
        'views/templates.xml',
        'views/product_template_views.xml',
        'views/menu_items.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
