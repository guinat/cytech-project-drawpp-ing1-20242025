#!/bin/bash

# Obtient le chemin du répertoire racine du projet
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )"

# Ajoute le répertoire du projet au PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$PROJECT_ROOT

# Message de confirmation
echo "PYTHONPATH mis à jour : $PYTHONPATH"
echo "Vous pouvez maintenant exécuter le compilateur depuis le dossier compiler/"