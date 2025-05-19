#!/usr/bin/env sh

## #!/usr/bin/env zsh

# Script para generar llave ssh para conexion con github

## SSH

ssh-keygen -t ed25519 -C "useremail@mail.com"

# Copiar llave ssh
# Comando 1 para copia llave publica y pegarla en SSH key Menu de Github
pbcopy < ~/.ssh/id_ed25519.pub
# Comando 2
cat ~/.ssh/id_ed25519.pub


