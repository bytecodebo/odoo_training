# Tutorial de Desarrollo de Odoo 16.0

#### Clase 09
### Herencia en modelos: _inherit, _inherits

#### Agenda

### Introducción

La herencia de modelos es un mecanismo para crear nuevos modelos a partir de modelos existentes. 
Se utiliza la propiedad `_inherit` para indicar que un modelo hereda de otro

#### 1. Tipos de herencia
- Herencia Clásica:
  - Extender modelo existente, creando, modificando, eliminando metodos de la clase padre.
  - Herencia total del modelo hijo
  - Se define el modelo hijo con `_inherit`

- Herencia por Delegacion:
  - Delega a la clase padre la gestion de ciertos procesos, metodos, variables.
  - Se define el modelo con `inherits`
  - Cambios en la logica del negocio, sin cambios en las vistas
  
```python
# Modelo padre
class ResPartner(models.Model):
    _name = 'res.partner'

# Modelo hijo que hereda del modelo padre
class MyPartner(models.Model):
    _name = 'my.partner'
    _inherit = 'res.partner'  # Indica que hereda de res.partner

    # Añadir un nuevo campo
    email_type = fields.Selection([('business', 'Negocios'), 
                                   ('personal', 'Personal')], string="Tipo de correo")

```

```python
# Modelo padre
class ResPartner(models.Model):
    _name = 'res.partner'

# Modelo hijo que hereda del modelo padre
class Users(models.Model):
    """ User class. A res.users record models an OpenERP user and is different
        from an employee.

        res.users class now inherits from res.partner. The partner model is
        used to store the data related to the partner: lang, name, address,
        avatar, ... The user model is now dedicated to technical data.
    """
    _name = "res.users"
    _description = 'User'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner', required=True, ondelete='restrict', auto_join=True, index=True,
        string='Related Partner', help='Partner-related data of the user')
    name = fields.Char(related='partner_id.name', inherited=True, readonly=False)
    email = fields.Char(related='partner_id.email', inherited=True, readonly=False)
```

#### 2. Beneficios de la utilizacion de herencia
- Reutilizacion de funcionalidades y estructura de los modelos padres.
- Evita duplicidad de codigo
- Practico para la modificacion y extension de funcionalidades
