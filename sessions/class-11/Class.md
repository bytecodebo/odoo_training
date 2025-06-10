# Tutorial de Desarrollo de Odoo 16.0

#### Clase 11
### Relaciones entre modelos (Many2one, One2many, Many2many)

#### Agenda

### Introducción

La relación entre modelos se establece principalmente mediante campos relacionales. Estos campos 
permiten vincular registros de diferentes modelos, creando una estructura jerárquica de datos. 
El sistema de relaciones en Odoo facilita la gestión de datos complejos y la creación de 
aplicaciones con lógica empresarial sofisticada. 

#### 1. Tipos de Relaciones


- **Many2one (Uno a muchos):**
Un registro de un modelo puede estar relacionado con muchos registros de otro modelo. Por ejemplo, una orden puede estar relacionada con muchos productos.
- **One2many (Uno a uno):**
Un registro de un modelo se relaciona con un único registro de otro modelo. Por ejemplo, un cliente puede tener una única dirección.
- **Many2many (Muchos a muchos):**
Un registro de un modelo puede estar relacionado con muchos registros de otro modelo, y viceversa. Por ejemplo, un producto puede estar relacionado con muchas categorías.
- **One2one (Uno a uno):**
Un registro de un modelo se relaciona con un único registro de otro modelo, y viceversa

```python
class Order(models.Model):
    _name = 'order.order'
    _description = "Order Order description"
    
    client_id = fields.Many2one('res.partner', string='Cliente')
    tax_ids = fields.Many2many("account.tax", string="Taxes")
    test_ids = fields.One2many("test_model", "partner_id", string="Tests")
    
    def _get_input_new_lines(self):
        if self.contract_id:
            input_line_values = self._input_new_line_values(self.date_from, self.date_to)
            input_manual_ids = self.input_line_ids.filtered(lambda x: not x.input_automatic)
            input_line_ids = self.input_line_ids.browse([])
            for r in input_line_values:
                r['payslip_id'] = self.id
                r['input_automatic'] = True
                input_line_ids |= input_line_ids.new(r)
            for im in input_manual_ids:
                vals = im._get_data_input_manuals()
                vals['payslip_id'] = self.id
                input_line_ids |= input_line_ids.new(vals)
            return input_line_values
        else:
            return [(5, False, False)]
        
    # Otros campos de la orden
    
    
    


```
