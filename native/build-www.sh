#!/bin/sh
# Copia la web app al bundle nativo (www/). Correr desde native/ antes de `npx cap sync ios`.
# No copia sw.js a propósito: dentro del wrapper el service worker no aplica
# (el registro en app.js ya trae .catch silencioso si el archivo no existe).
set -e
cd "$(dirname "$0")"
rm -rf www
mkdir -p www
cp ../index.html ../manifest.json ../legal.html www/ 2>/dev/null || cp ../index.html ../manifest.json www/
cp -R ../js ../css ../assets www/
echo "www/ listo:"
du -sh www
