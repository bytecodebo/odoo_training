# -*- coding: utf-8 -*-
{
    'name': "Mya Main Settings",

    'summary': """ Modulo Base modelos y herramientas para proyectos""",

    'description': """
        Modulo base para instalaciones de instancias del cual dependeran todos nuestros desarrollos
    """,

    'author': "Myapps",
    'website': "https://www.myapps.com.bo",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Hidden/Tools',
    'version': '16.0.1.0.2',

    # any module necessary for this one to work correctly
    'depends': ['base_setup',
                'server_action_mass_edit',
                'module_auto_update',
                'sequence_reset_period'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/res_config.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
