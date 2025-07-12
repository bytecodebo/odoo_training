from odoo import models, fields

class ContactForm(models.Model):
    _name = 'contact.form'
    _description = 'Contact Form'

    name = fields.Char(string='Nombre', required=True)
    email = fields.Char(string='Correo Electrónico')
    phone = fields.Char(string='Teléfono')
    message = fields.Text(string='Mensaje')