#!/bin/bash

# Charger les variables d'environnement depuis le fichier .env
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo "Erreur : fichier .env introuvable."
    exit 1
fi

# Vérifier que PROJECT_DIR est défini
if [ -z "$PROJECT_DIR" ]; then
    echo "Erreur : PROJECT_DIR n'est pas défini dans le fichier .env."
    exit 1
fi

# Se déplacer dans le répertoire du projet
cd "$PROJECT_DIR" || exit 1

# Étape 1 : Créer un environnement virtuel
ENV_DIR="$PROJECT_DIR/env"

if [ ! -d "$ENV_DIR" ]; then
    echo "Création de l'environnement virtuel..."
    python3 -m venv "$ENV_DIR"
    echo "Environnement virtuel créé avec succès."
else
    echo "Environnement virtuel déjà existant."
fi

# Activer l'environnement virtuel
echo "Activation de l'environnement virtuel..."
source "$ENV_DIR/bin/activate"

# Étape 2 : Installer les dépendances
REQUIREMENTS_FILE="$PROJECT_DIR/requirements.txt"

if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Installation des dépendances depuis requirements.txt..."
    pip install --upgrade pip
    pip install -r "$REQUIREMENTS_FILE"
    echo "Dépendances installées avec succès."
else
    echo "Erreur : requirements.txt introuvable."
    deactivate
    exit 1
fi

# Étape 3 : Exécuter les scripts dans l'ordre spécifié
SCRIPTS=(
    "$PROJECT_DIR/scripts/01_execution.py"
    "$PROJECT_DIR/scripts/02generationSAStoken.sh"
    "$PROJECT_DIR/scripts/02downloadBlobs.py"
    "$PROJECT_DIR/scripts/03_extract_parquet.py"
    "$PROJECT_DIR/scripts/03_convertisseur_images.py"
    "$PROJECT_DIR/scripts/04_extract_zip.py"
)

echo "Exécution des scripts dans l'ordre spécifié..."

for script in "${SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        echo "Exécution de $script..."
        if [[ $script == *.py ]]; then
            python "$script"
        elif [[ $script == *.sh ]]; then
            bash "$script"
        else
            echo "Format non supporté pour le script : $script"
            deactivate
            exit 1
        fi
        
        if [ $? -ne 0 ]; then
            echo "Erreur lors de l'exécution de $script. Arrêt du processus."
            deactivate
            exit 1
        fi
    else
        echo "Erreur : Le fichier $script n'existe pas."
        deactivate
        exit 1
    fi
done

echo "Tous les scripts ont été exécutés avec succès."

# Suppression des fichiers .zip, .tgz, et .parquet après extraction
echo "Suppression des fichiers extraits..."

# Suppression des fichiers .zip
ZIP_FILES=$(find "$PROJECT_DIR" -type f -name "*.zip")
if [ -n "$ZIP_FILES" ]; then
    echo "Suppression des fichiers .zip..."
    find "$PROJECT_DIR" -type f -name "*.zip" -exec rm -f {} \;
else
    echo "Aucun fichier .zip trouvé à supprimer."
fi

# Suppression des fichiers .tgz
TGZ_FILES=$(find "$PROJECT_DIR" -type f -name "*.tgz")
if [ -n "$TGZ_FILES" ]; then
    echo "Suppression des fichiers .tgz..."
    find "$PROJECT_DIR" -type f -name "*.tgz" -exec rm -f {} \;
else
    echo "Aucun fichier .tgz trouvé à supprimer."
fi

# Suppression des fichiers .parquet
PARQUET_FILES=$(find "$PROJECT_DIR" -type f -name "*.parquet")
if [ -n "$PARQUET_FILES" ]; then
    echo "Suppression des fichiers .parquet..."
    find "$PROJECT_DIR" -type f -name "*.parquet" -exec rm -f {} \;
else
    echo "Aucun fichier .parquet trouvé à supprimer."
fi

# Désactiver l'environnement virtuel
deactivate
echo "Environnement virtuel désactivé."
