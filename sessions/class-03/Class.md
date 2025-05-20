# Tutorial de Desarrollo de Odoo 16.0

#### Clase 03
### Consulta de documentación oficial y community

#### Agenda

**1.- Revisión de diferentes fuentes de consultas para desarrollo de aplicaciones
de odoo.**

  - Appstore de Odoo. [Enlace](https://apps.odoo.com/apps) 
  - CybroOdoo [Enlace](https://www.cybrosys.com/blog/) [Github](https://github.com/CybroOdoo/CybroAddons/tree/16.0)
    - Odoo Books by Cybrosys [Enlace](https://www.cybrosys.com/odoo/odoo-books)
  - OdooMates [Github](https://github.com/odoomates/odooapps/tree/16.0)
  - Open Synergy [Github](https://github.com/orgs/open-synergy/repositories?type=all)
  - Deltatech [Github](https://github.com/dhongu/deltatech/tree/16.0)
  - ByteCodeBo [Github](https://github.com/bytecodebo)
  - OCA [Github](https://github.com/orgs/OCA/repositories)
  - Awesome Odoo [Github](https://github.com/desdelinux/awesome-odoo)


**2.- Completar Ambiente de Desarrollo**

- Configuración de mani 
  - Instalar aplicacion [Github](https://github.com/bytecodebo/byc_tools)
    - Crear variables de entorno en ~/.bash_profile or ~/.bash_:
      
  ```bash
    
  export MANI_SCRIPTS=/path/to/byc_tools/mani
  eport MANI_SCRIPT_SHARE=/path/to/byc_tools/common_mani_sake
    ````
- Variable de entorno Pycharm

  ```bash
  export PYCHARM_TEMPLATES_FOLDER=/path/to/JetBrains/PyCharmCE2024.1/templates
  ```

**3.- Comandos mani**

```bash
# iniciar proyecto
# crea archivo cnf.env a configurar con datos de git y github

mani init

# finalizada la configuracion ejecutar nuevamente 
# crea archivo mani.yaml con valores de cnf.env

mani init

# modificar archivo mani.yaml adicionando los repositorios a utilizar
# repositories:
#  - sale-workflow
#  - purchase-workflow
#  - partner-contact
#  - account-invoicing
# guardar y ejecutar
# se generara archivo project.yaml con la configuracion de 
# todos los repositorios adicionados
mani sync
# ejecutar nuevamente 
# se clonaran los repositorios adicionados con la rama parametrizada en cnf.env
mani sync 

# Utilizacion

# Listar proyectos (repositorios)
mani list projects

# Listar tareas (acciones a ejecutar)
mani list tasks

# Estado de los repos
mani run g-st

# Pull a los repos
mani run g-pl -t mya16 branch=16.0|16.0dev

# Commit a todos los repos
mani run g-cm -t mya16 msg='update. Fix duplicate registers'

# push a todos los repos
mani run g-ph -t mya16

# crear rama en los repos
mani run g-cb -t mya16 branch=[NewBranch]

# merge en todos los repos
mani run g-mg -t mya16 branch=[CurrentBranch] brr=[SourceBranch]

# reconstruye archivo mani.yaml
mani init -f 

```
