#!/usr/bin/env sh

# Librerias para correr odoo local y docker
pip install astor==0.8.1 \
cryptography==3.4.8 \
libsaas==0.4 \
libsass==0.20.1 \
openpyxl==3.1.5 \
paramiko==3.4.1 \
pdfkit==1.0.0 \
pysftp==0.2.9 \

# Librerias utilitarias
pip install bases==0.3.0 \
maya==0.6.1 \
numpy==2.0.1 \
pdfkit==1.0.0 \
pendulum==3.0.0 \
pandas==2.2.3 \
xmlschema==3.3.2 \
signxml==3.2.2 \
beautifultable \
excel-formulas-calculator \
tabulate

# Librerias para facturacion electronica
pip install xmlschema==3.3.2 \
signxml==3.2.2 \
pyqrcode \
pypng
