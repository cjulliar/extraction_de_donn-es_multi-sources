#!/bin/bash

# Charger les variables d'environnement depuis un fichier .env
export $(grep -v '^#' .env | xargs)

# Vérifier que les variables d'environnement nécessaires sont définies
if [[ -z "$STORAGE_ACCOUNT" || -z "$CONTAINER" ]]; then
    echo "Les variables STORAGE_ACCOUNT et CONTAINER doivent être définies dans le fichier .env"
    exit 1
fi

# Extraire la clé de stockage depuis les variables d'environnement
ACCOUNT_KEY=$(az storage account keys list --account-name "$STORAGE_ACCOUNT" --query "[0].value" --output tsv)

if [[ -z "$ACCOUNT_KEY" ]]; then
    echo "Erreur : impossible de récupérer la clé du compte de stockage."
    exit 1
fi

# Définir les paramètres de temps pour le SAS token
START_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
EXPIRY_TIME=$(date -u -v+1d +"%Y-%m-%dT%H:%M:%SZ") # Utilisation de -v pour ajouter un jour

# Générer le SAS token pour le conteneur
SAS_TOKEN=$(az storage container generate-sas \
    --account-name "$STORAGE_ACCOUNT" \
    --account-key "$ACCOUNT_KEY" \
    --name "$CONTAINER" \
    --permissions rl \
    --start "$START_TIME" \
    --expiry "$EXPIRY_TIME" \
    --output tsv)

# Vérifier si la génération du SAS a réussi
if [[ -z "$SAS_TOKEN" ]]; then
    echo "Erreur lors de la génération du SAS token"
    exit 1
fi

# Construire l'URL SAS
SAS_URL="https://${STORAGE_ACCOUNT}.blob.core.windows.net/${CONTAINER}?${SAS_TOKEN}"

# Afficher l'URL SAS 
echo "SAS URL générée : $SAS_URL"

# Fonction pour mettre à jour ou ajouter une variable dans le fichier .env
update_env_variable() {
    local key="$1"
    local value="$2"
    if grep -q "^${key}=" ".env"; then
        # Utilisation d'une syntaxe compatible pour sed
        sed -i.bak "s|^${key}=.*|${key}=${value}|" ".env"
        rm -f .env.bak # Supprimer le fichier de sauvegarde généré par sed
    else
        echo "${key}=${value}" >> ".env"
    fi
}

# Enregistrer l'URL SAS dans .env
update_env_variable "SAS_URL" "$SAS_URL"

echo "SAS URL enregistrée dans sas_url.txt et .env avec succès."
