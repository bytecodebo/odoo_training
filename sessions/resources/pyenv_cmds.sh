#!/usr/bin/env sh

# Instalacion de Pyenv para manejo de multiples versiones de  python
# Instalacion automatica
# Fuente:   https://github.com/pyenv/pyenv

curl -fsSL https://pyenv.run | bash

# Configuracion de Variable de Entorno para pyenv

# touch ~/.bashrc  Crea archivo
# nano ~/.bashrc  Crea o abre archivo
# Shells interactivos
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init - bash)"' >> ~/.bashrc

# Shells logueados
# Verificar si se tiene creado bash_profile
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
echo 'eval "$(pyenv init - bash)"' >> ~/.bash_profile

# Reiniciar shell
exec "$SHELL"

# Comandos

pyenv install ${VersionPython}
pytenv install -l # listar versiones

# version local
pyenv local ${VersionPython}

# version global
pyenv global ${VersionPython}


# Instalar plugin pyenv-virtualenv para pyenv
# Fuente  https://github.com/pyenv/pyenv-virtualenv

# Configurar Git unix-style para prevenir errores en final de linea
# cuando utilice WSL
git config --global core.autocrlf input

# Descargar de repositorio
git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv

# Adicionar a Variables de Entorno
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc

# Reiniciar shell
exec "$SHELL"

# Comandos

pyenv virtualenv 2.7.10 my-virtual-env-2.7.10

# Entorno virtual para version
$ pyenv version
## 3.4.3 (set by /home/yyuu/.pyenv/version)
$ pyenv virtualenv venv34

# Listado de env virtuales
pyenv virtualenvs

pyenv activate <name>
pyenv deactivate

pyenv uninstall my-virtual-env

