

{
    'name': 'Mya Partner Advance',
    'version': '16.0.1.0.3',
    'summary': 'Adecuaciones Modulo de contact partner',
    'description': 'Nuevas funcionalidades en formulario de contactos',
    'category': 'Contact',
    'author': 'Myapps',
    'website': 'http://mya.com',
    'license': 'AGPL-3',
    'depends': ['web',
                'contacts',
                'trn_main_setting'],
    'external_dependencies': {
        'python': ['openupgradelib'],
    },
    'data': [
        'security/group_security.xml',
        'security/assistance/ir.model.access.csv',
        'security/supervisor/ir.model.access.csv',
        'security/ir.model.access.csv',
        'data/data_contacts.xml',
        'data/data_siat.xml',
        'data/data_mass_contacts.xml',
        'views/res_config.xml',
        'views/siat_base_catalog_views.xml',
        'views/siat_catalogs_dct_views.xml',
        'views/siat_catalogs_pym_views.xml',
        'views/siat_catalogs_country_views.xml',
        'views/siat_catalogs_cur_views.xml',
        'views/siat_catalogs_pos_type_views.xml',
        'views/res_partner_views.xml',
        'views/menu_items.xml'
    ],
    'demo': [''],
    'installable': True,
    'auto_install': False,

}