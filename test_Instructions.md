
1. Seleccione una de las siguientes afirmaciones y explique la razon de su respuesta.
   - a) Puedo heredar campos de una clase abstracta para construir un modelo persistente
   - b) Puedo heredar campos de un modelo persistente para construir una clase abstracta.
   - c) No puedo realizar ninguna de las anteriores

    Resp.- la respuesta correcta es el inciso A, si se puede construir un modelo persistente desde una clase abstracta, pero la clase abstracta no puede generar un modelo persistente(que si se genera una tabla en la base de datos)




# Examen práctico de Odoo  
**Nombre:** Juan Carlos Mamani Rojas  
**Módulo:** `trn_exam_partner_contact`  
**Ruta:** `/mya-training-workflow/trn_exam_partner_contact`

## ¿Qué hace el módulo?

Permite agrupar contactos como **clientes padre e hijos**, asignando automáticamente un **código correlativo**:

- Ejemplo:
  - Padre: `CCP01000`
  - Hijos: `CCP01001`, `CCP01002`, etc.

## Cómo usarlo

1. **Instalar** el módulo desde el menú de Apps.
2. **Crear un cliente padre:**
   - Ir a Contactos → Crear.
   - Llenar los datos y marcar **¿Es cliente padre?**
   - Al guardar, se genera el código del cliente padre.

3. **Crear un cliente hijo:**
   - Ir a Contactos → Crear.
   - Llenar los datos y seleccionar el **Cliente padre**(por nombre).
   - No marcar el checkbox de padre.
   - Al guardar, se genera el código del hijo basado en el del padre.

4. **Ver los códigos:**
   - Ir a la vista lista de Contactos.
   - Revisar la columna **Código del cliente** para ver padres e hijos.

## Campos agregados

- `is_parent_customer`: ¿Es cliente padre?
- `parent_customer_id`: Cliente padre
- `partner_code`: Código del cliente

## Reglas

- Solo los clientes padre generan hijos.
- Un cliente padre no puede tener otro padre.
- Los códigos se asignan automáticamente.
