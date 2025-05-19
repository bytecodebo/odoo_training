#!/usr/bin/env bash
# El directorio donde se copie este archivo debe estar configurado como directorio global
# para que se pueda llamar desde cualquier parte
# otorgar permisos de ejecucion chmod +x

set -e

if [ "$(uname -s)" = "Darwin" ] && [ "$(uname -m)" = "x86_64" ]; then
    target="darwin_amd64"
elif [ "$(uname -s)" = "Linux" ] && [ "$(uname -m)" = "x86_64" ]; then
    target="linux_amd64"
elif [ "$(uname -s)" = "Linux" ] && ( uname -m | grep -q -e '^arm' -e '^aarch' ); then
    target="linux_arm64"
else
    echo "Unsupported OS or architecture"
    exit 1
fi

__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
__file="${__dir}/$(basename "${BASH_SOURCE[0]}")"
__base="$(basename ${__file} .sh)"
__source="$(pwd)"
__file_env="${__source}/.env"
__file_functions="${__dir}/odoo-mods.sh"

echo """Scripts for up instances"""
echo """***************** ****** **************"""

echo """ source path:: ${__source}"""
echo """ file name:: ${__base}"""
echo """ dir name :: ${__dir}"""

set -o allexport
source "${__file_env}"
source "${__file_functions}"

VAR_INSTANCE="${CONTEXT_INSTANCE:-}" # nombre de instancia por defecto bantic odoo 15
VAR_MODULE="${CONTEXT_MODS:-}" # sin levantar modulos
VAR_OPTION="${CONTEXT_OPTION:-u}" # por defecto update I instalar modulos
VAR_DB="${CONTEXT_DB:-}" # base de datos
VAR_DEV="${CONTEXT_EXEC:-0}" # reload 1 ,2 xml 3 reload,xml
VAR_SHELL="${CONTEXT_SHELL:-0}" # mode shell
VAR_FNPORT=""
VAR_REMOTE="0" # mode remote debugging
VAR_DEBUG="0" # mode remote debugging
VAR_ENVIRONMENT="${CONTEXT_ENV:-tst}" # 1= produccion , 2 testing
VAR_TRANSLATE="${CONTEXT_TRANS:-0}" # override translation 1 ok

set +o allexport

while [ -n "$1" ]; do # while loop starts
	case "$1" in
    -i) VAR_INSTANCE="$2"
        shift
        ;;
    -e) VAR_ENVIRONMENT="$2"
        shift
        ;;
    -d) VAR_DB="$2"
        shift
        ;;
    -o) VAR_OPTION="$2"
        shift
        ;;
    -m) VAR_MODULE="$2"
        shift
        ;;
    -b) VAR_DEBUG="$2"
        shift
        ;;
    -r) VAR_REMOTE="$2"
        shift
        ;;
    -x) VAR_DEV="$2"
      shift
      ;;
    -s) VAR_SHELL="$2"
      shift
      ;;
    -p) VAR_FNPORT="$2"
      shift
      ;;
    -t) VAR_TRANSLATE="$2"
      shift
      ;;
	esac
	shift
done
if [ "$VAR_INSTANCE" = "" ]; then
    echo "El nombre de la instancia es obligatoria -i"
    exit 1
fi
###
#### -----------
###  Conversion de los repositorios abreviados a los verdaderos
### -------------
convert_repo(){
    case "$1" in
        "con") github="tcp_connector" ;;        
        *) github="$1" ;;
    esac
}

REPO_CONF=" ${CONTEXT_SETTINGS}/${CONTEXT_PROJECT_TAG}/${CONTEXT_PROJECT_TAG}${CONTEXT_ODOO_VERSION}/conf"
ODOO_VER=" ${CONTEXT_ODOO_SOURCE}/odoo-repo${CONTEXT_ODOO_VERSION}"
instance_dep="od-${VAR_INSTANCE}.conf"
specific_db=""
modules_upd=""
active_shell=""
fn_port=""
params_dev=""
env_work="tst"
if [ "$VAR_MODULE" = "" ]; then
  VAR_OPTION=""
elif [ "$VAR_OPTION" = "u" ] || [ "$VAR_OPTION" = "m" ]; then
    mod_upd=""
    if [ "$VAR_MODULE" = "" ]; then
        echo "los modulos son requeridos -m"
        exit 1
    fi
    if [ "$VAR_MODULE" = "all" ]; then
        if [ "$VAR_DB" = "" ]; then
          echo "El nombre de la base de datos es requerida -d"
          exit 1
        fi
    fi
    rep=$VAR_MODULE
    oldIFS=$IFS;
    IFS=","
    for item in $rep;
    do
      convert_modules_${CONTEXT_FUNC_MODS} "$item"
      mod_upd+="${mod},"
    done;
    IFS=$oldIFS
    modules_upd=" -u ${mod_upd%,*}"
    if [ "$VAR_OPTION" = "m" ]; then
      echo """"
      echo """ **** Start migration ...."""
      echo """"
      modules_upd="${modules_upd} --stop-after-init"
      echo "$modules_upd"
    fi
elif [ "$VAR_OPTION" = "i" ]; then
    mod_upd=""
    if [ "$VAR_MODULE" = "" ]; then
        echo "los modulos son requeridos -m"
        exit 1
    fi
    if [ "$VAR_MODULE" = "all" ]; then
        echo "Debe especificar los modulos a instalar"
          exit 1
    fi
    rep=$VAR_MODULE
    oldIFS=$IFS;
    IFS=","
    for item in $rep;
    do
      convert_module "$item"
      mod_upd+="${mod},"
    done;
    IFS=$oldIFS
    modules_upd=" -i ${mod_upd%,*}"
    params_dev=" --stop-after-init"
fi
if [ "$VAR_OPTION" = "u" ] && [ "$VAR_MODULE" != "" ] && [ "$VAR_MODULE" != "all" ] && [ "$VAR_SHELL" = "0" ]; then

    if [ "$VAR_DEV" -eq 1 ]; then
      params_dev=" --dev=reload"
    fi
    if [ "$VAR_DEV" -eq 2 ]; then
        params_dev=" --dev=xml"
    fi
    if [ "$VAR_DEV" -eq 3 ]; then
        params_dev=" --dev=reload,xml"
    fi
    if [ "$VAR_DEV" -eq 4 ]; then
        params_dev=" --stop-after-init"
    fi
elif [ "$VAR_SHELL" != "0" ]; then
  active_shell=" shell"
fi
if [ "$VAR_FNPORT" != "" ]; then
  fn_port=" --http-port=${VAR_FNPORT}"
fi
if [ "$VAR_OPTION" = "up" ]; then
  mod_upd=""
    if [ "$VAR_MODULE" = "" ]; then
        echo "los modulos son requeridos -m"
        exit 1
    fi
     if [ "$VAR_DB" = "" ]; then
          echo "El nombre de la base de datos es requerida -d"
          exit 1
     fi
    if [ "$VAR_MODULE" != "all" ]; then
      rep=$VAR_MODULE
      oldIFS=$IFS;
      IFS=","
      for item in $rep;
      do
        convert_module "$item"
        mod_upd+="${mod},"
      done;
      IFS=$oldIFS
    else
      mod_upd="all"
    fi
    modules_upd=" -u ${mod_upd%,*}"
    params_dev=" --stop-after-init"
fi
if [ "$VAR_ENVIRONMENT" = "1" ] || [ "$VAR_ENVIRONMENT" = "prd" ]; then
   env_work="prd"
fi
if [ "$VAR_DB" != "" ]; then
    specific_db=" -d ${VAR_INSTANCE}_${env_work}_${VAR_DB}"
else
  specific_db=""
fi
remote_debug=""
override_trans=""
if [ "$VAR_TRANSLATE" = "1" ]; then
  override_trans=" --i18n-overwrite"
fi
if [ "$VAR_REMOTE" = "1" ]; then
   # remote_debug="--remote-debugging-port=9222 --user-data-dir=remote-debug-profile"
   #remote_debug="--remote-debugging-port=9222 --user-data-dir=remote-debug-profile /Users/robertsvx/Documents/OdooRepo/env3812/bin/python"
  # remote_debug="--port=9222 --client 127.0.0.1 /Users/robertsvx/Documents/OdooRepo/env3812/bin/python"
  remote_debug=" /Users/robertsvx27/.pyenv/versions/3.11.8/envs/envO17/bin/python -m ptvsd --host localhost --port 5678 --wait"
fi

local_debug=" ${CONTEXT_PYTHON_ENV:-}"
if [ "$local_debug" = ""]; then
  if [ "${CONTEXT_ODOO_VERSION}" = "16" ]; then
    local_debug="/Users/robertsvx27/.pyenv/versions/3.10.7/envs/envCop310/bin/python3"
  elif [ "${CONTEXT_ODOO_VERSION}" = "15" ]; then
    local_debug=" /Users/robertsvx27/.pyenv/versions/3.9.7/envs/env3915/bin/python3"
  elif [ "${CONTEXT_ODOO_VERSION}" = "14" ]; then
    local_debug="/Users/robertsvx27/.pyenv/versions/odoo38-14/bin/python3"
  fi
fi
if [ "$VAR_DEBUG" = "1" ]; then
  local_debug=" /Users/robertsvx27/.pyenv/versions/3.11.8/envs/envO17/bin/python /Applications/PyCharm\ CE.app/Contents/plugins/python-ce/helpers/pydev/pydevd.py --multiprocess"
  local_debug="""${local_debug}  --qt-support=auto --client 127.0.0.1 --port 51693 --file """
fi

str_val="""${local_debug}${remote_debug}${ODOO_VER}/odoo-bin${active_shell}${fn_port} -c ${REPO_CONF}/${instance_dep}${specific_db}${override_trans}${modules_upd}${params_dev}"""

# shellcheck disable=SC2028
eval """clear"""
echo "*****"
echo """Scripts for up instances"""
echo """***************** ****** **************"""

echo """ source path:: ${__source}"""
echo """ file name:: ${__base}"""
echo """ dir name :: ${__dir}"""
echo ""
echo """${str_val}"""
echo ""
echo "*****"
echo "*** updating..."
eval """${str_val}"""
