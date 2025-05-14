#!/usr/bin/env bash

# Instalar git

sudo apt-get install git

# Verificar estado conexion github

ssh -T git@github.com


# Adicionar submodulo git

git submodule add -b $branch_name --depth=$depth_value git@github.com:account/repo.git path_to_module/module_folder

# Crear repositorio espejo
# ****———****
# COPIAR REPO DE OCA Y HACERLO ESPEJO DE REPO BANTIC
# ***———***
git clone --bare https://github.com/exampleuser/old-repository.git

cd old-repository
git push --mirror https://github.com/exampleuser/new-repository.git

git clone --mirror https://github.com/exampleuser/repository-to-mirror.git

$ cd repository-to-mirror
$ git remote set-url --push origin https://github.com/exampleuser/mirrored


# ***— para subir cambios al repo con submodulos —****
 git submodule foreach --recursive git checkout 14.0dev && git pull origin 14.0dev
