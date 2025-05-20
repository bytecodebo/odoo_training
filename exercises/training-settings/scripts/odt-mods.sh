#!/bin/bash
# Este archivo debe  ser copiado en el mismo directorio que odt-run.sh
# otorgar permisos de ejecucion chmod +x odt-run.sh

echo """Scripts for up instances"""
echo """***************** ****** **************"""

#### -----------
###  Conversion de los modulos abreviados a los verdaderos
### -------------
convert_modules_mya(){
    case "$1" in
        "base") mod="contacts,account,sale" ;;
        'pust') mod="purchase_stock" ;;
        "jobq") mod="queue_job,queue_job_batch" ;;
        "quej") mod="queue_job" ;;
        *) mod="$1" ;;
    esac
}

convert_modules_tag2(){
    case "$1" in
        "poso") mod="point_of_sale" ;;
        *) mod="$1" ;;
    esac
}
