

{
    'name': 'Partner Advance Training',
    'version': '16.0.1.0.1',
    'summary': 'Adecuaciones Modulo de contact partner',
    'description': 'Nuevas funcionalidades en formulario de contactos',
    'category': 'Contact',
    'author': 'Myapps',
    'website': 'http://mya.com',
    'license': 'AGPL-3',
    'depends': ['web',
                'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'data/data_siat.xml',
        'views/siat_base_catalog_views.xml',
        'views/siat_catalogs_views.xml',
        'views/menu_items.xml'
    ],
    'demo': [''],
    'installable': True,
    'auto_install': False,

}