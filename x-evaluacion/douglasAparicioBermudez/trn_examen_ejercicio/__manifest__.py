{
    'name': 'Contact Form',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Formulario de contacto personalizado',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/contact_form.xml',
    ],
    'installable': True,
    'application': True,
}