# Tutorial de Desarrollo de Odoo 16.0

#### Clase 10
### Uso de decoradores @api.depends, @api.onchange, @api.model, @api.model_create_multi

#### Agenda

### Introducción

Los decoradores modifican el comportamiento de métodos dentro de modelos, controladores y otros componentes.

```python
@api.onchange('campo_a')
def _onchange_campo_a(self):
    # Código para actualizar otro campo basado en el cambio de 'campo_a'
    self.campo_b = self.campo_a * 2

@api.depends('campo_a')
def _compute_campo_b(self):
    # Código para calcular 'campo_b' basado en 'campo_a'
    self.campo_b = self.campo_a * 2



```

##### Ejemplos

```python
import os
import time

from decorator import decorator
from functools import wraps


@decorator
def clear_console(func, *args, **kw):

    os.system('cls' if os.name == 'nt' else 'clear')
    print('\n\nClean console from method %s' % func.__name__)
    # os.system('cls' if os.name == 'nt' else 'clear')
    return func(*args, **kw)


def print_me(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if len(kwargs) > 0:
            print("\n{}{}{} = {}".format(func.__name__, args, kwargs, result))
        else:
            print("\n{}{} = {}".format(func.__name__, args, result))
        return result
    return wrapper


@decorator
def check_arguments(func, *args, **kw):
    if kw is None:
        kw = {}
    if args is None:
        args = []
    return func(*args, **kw)


def with_synchro_cursor(autocommit=True):
    def decorator(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            for rec in self:
                if rec.enabled or self._context.get('ctx_force_run_synchro', False):
                    with registry(self.env.cr.dbname).cursor() as new_cr:
                        env = api.Environment(new_cr, SUPERUSER_ID, self.env.context)
                        new_cr._cnx.autocommit = autocommit
                        self = self.with_env(env).with_context(original_cr=self._cr)
                        return method(self, *args, **kwargs)
            raise UserError(
                _("Can't create %s because is not available.\n"
                  "Please contact your system administrator to enable this behaviour.") % self._name)
        return wrapper
    return decorator
```
