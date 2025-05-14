# Tutorial de Desarrollo de Odoo 16.0

## Clase 01

## Preparación de ambiente de desarrollo

### Ubuntu Desktop 20 o superior
    
   ```bash
   
   # Actualizar paquetes
   
   sudo apt update && sudo apt upgrade
   
   # Crear usuario de Sistema odoo16
   
   sudo useradd -m -d /opt/odoo16 -U -r -s /bin/bash odoo16
   
   # Instalar dependencias para Odoo
   
   sudo apt install build-essential wget git python3-pip python3-dev python3-venv python3-wheel libfreetype6-dev libxml2-dev libzip-dev libsasl2-dev python3-setuptools libjpeg-dev zlib1g-dev libpq-dev libxslt1-dev libldap2-dev libtiff5-dev libopenjp2-7-dev
   
   # Instalar y configurar PostgreSQL
   
   sudo apt-get install postgresql
   
   # Crear usuario postgres
   sudo -u postgres createuser --createdb --username postgres --no-createrole --no-superuser --pwprompt odoo16
   
   
   ```

Consola de PostgresSQL

```bash
sudo su postgres
psql
ALTER USER odoo16 WITH SUPERUSER;

\q
exit
   ```

   ```bash
   
   # Instalar paquete de impresión de pdf
   
   sudo apt install wkhtmltopdf
   
  
   
   ```