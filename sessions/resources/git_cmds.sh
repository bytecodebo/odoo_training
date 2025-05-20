#!/usr/bin/env bash

# Instalar git

sudo apt-get install git

# Verificar estado conexion github

ssh -T git@github.com


# Adicionar submodulo git

git submodule add -b $branch_name --depth=$depth_value git@github.com:account/repo.git path_to_module/module_folder

# Crear repositorio espejo
# ****———****
# COPIAR REPO DE OCA Y HACERLO ESPEJO DE EMPRESA
# ***———***
git clone --bare https://github.com/exampleuser/old-repository.git

cd old-repository
git push --mirror https://github.com/exampleuser/new-repository.git

git clone --mirror https://github.com/exampleuser/repository-to-mirror.git

$ cd repository-to-mirror
$ git remote set-url --push origin https://github.com/exampleuser/mirrored


# ***— para subir cambios al repo con submodulos —****
 git submodule foreach --recursive git checkout $branch_name && git pull origin $branch_name


git checkout --orphan newBranch
git add -A  # Add all files and commit them
git commit
git branch -D master  # Deletes the master branch
git branch -m master  # Rename the current branch to master
git push -f origin master  # Force push master branch to github
git gc --aggressive --prune=all     # remove the old files

#!/bin/bash

default_branch=`basename $(git symbolic-ref --short refs/remotes/origin/HEAD)`

git checkout --orphan tmp
git add -A				# Add all files and commit them
git commit
git branch -D $default_branch		# Deletes the default branch
git branch -m $default_branch		# Rename the current branch to default
git push -f origin $default_branch	# Force push default branch to github
git gc --aggressive --prune=all		# remove the old files


# ^(?!.*(\\'license\\'|\\"license\\"))$

# Remover submodulos

git rm -r the_submodule
rm -rf .git/modules/the_submodule

