#!/usr/bin/env bash




# Generar llave ssh aceptada por github

ssh-keygen -t ed25519 -C "useremail@mail.com"

# Copiar llave ssh

pbcopy < ~/.ssh/id_ed25519.pub

cat ~/.ssh/id_ed25519.pub