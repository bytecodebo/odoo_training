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

### Instalación en Linux de wkhtmltopdf

Ubuntu 22.04/20.04:
```
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb
sudo apt install ./wkhtmltox_0.12.6-1.focal_amd64.deb
```
Ubuntu 18.04:

```
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.bionic_amd64.deb
sudo apt install ./wkhtmltox_0.12.6-1.bionic_amd64.deb
```

Ubuntu 16.04:
```
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.xenial_amd64.deb
sudo apt install ./wkhtmltox_0.12.6-1.xenial_amd64.deb
```

### Instalación de Odoo

   ```bash
  
   # Instalar git
   
   sudo apt-get install git
   
   
   # Cambiarse al usuario creado para Odoo
   
   sudo su - odoo16 -s /bin/bash
   
   
   # Descargar odoo Comunitario version 16.0
   # Alternativa 01
   
   git clone https://www.github.com/odoo/odoo --depth=1 --branch=16.0 odoo16-repo
   
   # Alternativa 02
   # Se requiere llave ssh!!
   
   git clone --depth=1 --branch=16.0 git@ithub.com:odoo/odoo.git odoo16-repo
   
  
   ```

### Alternativa de Instalación de Odoo

```
https://github.com/Yenthe666/InstallScript

sudo wget https://raw.githubusercontent.com/Yenthe666/InstallScript/16.0/odoo_install.sh
sudo chmod +x odoo_install.sh
sudo ./odoo_install.sh
```