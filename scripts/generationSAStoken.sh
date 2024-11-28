#!/bin/bash

# Charger les variables d'environnement depuis un fichier .env
export $(grep -v '^#' .env | xargs)

# Vérification des variables nécessaires
if [[ -z "$STORAGE_ACCOUNT" || -z "$STORAGE_CONTAINER" || -z "$STORAGE_CONNEXION" ]]; then
    echo "Erreur : Les variables STORAGE_ACCOUNT, STORAGE_CONTAINER, et STORAGE_CONNEXION doivent être définies dans le fichier .env."
    exit 1
fi

# Extraire la clé de stockage depuis STORAGE_CONNEXION
ACCOUNT_KEY=$(echo "$STORAGE_CONNEXION" | awk -F 'AccountKey=' '{print $2}' | awk -F ';' '{print $1}')

if [[ -z "$ACCOUNT_KEY" ]]; then
    echo "Erreur : Impossible d'extraire la clé d'accès depuis STORAGE_CONNEXION."
    exit 1
fi

# Définir les paramètres de temps pour le SAS token
START_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ") # Heure actuelle en UTC
EXPIRY_TIME=$(date -u -v+1d +"%Y-%m-%dT%H:%M:%SZ") # Ajout d'un jour

# Générer le SAS token
SAS_TOKEN=$(az storage container generate-sas \
    --account-name "$STORAGE_ACCOUNT" \
    --account-key "$ACCOUNT_KEY" \
    --name "$STORAGE_CONTAINER" \
    --permissions rl \
    --start "$START_TIME" \
    --expiry "$EXPIRY_TIME" \
    --output tsv)

if [[ -z "$SAS_TOKEN" ]]; then
    echo "Erreur : Impossible de générer le SAS token."
    exit 1
fi

# Construire l'URL SAS
SAS_URL="https://${STORAGE_ACCOUNT}.blob.core.windows.net/${STORAGE_CONTAINER}?${SAS_TOKEN}"

# Afficher l'URL SAS générée
echo "SAS URL générée : $SAS_URL"

# Sauvegarder l'URL SAS dans un fichier texte
echo "$SAS_URL" > sas_url.txt
echo "SAS URL enregistrée dans sas_url.txt."

# Remplacer ou ajouter SAS_URL dans le fichier .env
if grep -q "^SAS_URL=" ".env"; then
    # Remplacer la ligne existante
    sed -i.bak "/^SAS_URL=/c\SAS_URL=${SAS_URL}" .env
    rm -f .env.bak
    echo "SAS_URL existait déjà et a été remplacée dans le fichier .env."
else
    # Ajouter si la ligne n'existe pas
    echo "SAS_URL=${SAS_URL}" >> .env
    echo "SAS_URL a été ajoutée dans le fichier .env."
fi
