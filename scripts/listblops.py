import os
import datetime
from azure.storage.blob import (
    BlobServiceClient,
    ContainerClient,
    generate_container_sas,
    ContainerSasPermissions,
)
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

STORAGE_ACCOUNT = os.getenv("STORAGE_ACCOUNT")
CONTAINER = os.getenv("CONTAINER")
ACCESS_KEY = os.getenv("ACCESS_KEY")

if not STORAGE_ACCOUNT or not CONTAINER or not ACCESS_KEY:
    raise ValueError("STORAGE_ACCOUNT, CONTAINER, ou ACCESS_KEY manquant dans .env")

# Générer un SAS token pour le conteneur
def generate_sas_token(account_name, container_name, account_key, days_valid=1):
    start_time = datetime.datetime.utcnow()
    expiry_time = start_time + datetime.timedelta(days=days_valid)

    sas_token = generate_container_sas(
        account_name=account_name,
        container_name=container_name,
        account_key=account_key,
        permission=ContainerSasPermissions(read=True, list=True),
        expiry=expiry_time,
        start=start_time,
    )
    return sas_token

try:
    print("Génération du SAS token...")
    sas_token = generate_sas_token(STORAGE_ACCOUNT, CONTAINER, ACCESS_KEY)

    # Construire l'URL SAS du conteneur
    container_url = f"https://{STORAGE_ACCOUNT}.blob.core.windows.net/{CONTAINER}?{sas_token}"
    print(f"SAS URL généré : {container_url}")

    # Se connecter au conteneur avec l'URL SAS
    print("Connexion au conteneur...")
    container_client = ContainerClient.from_container_url(container_url)

    # Lister les blobs dans le conteneur
    print("Liste des blobs :")
    blobs = container_client.list_blobs()
    for blob in blobs:
        print(f"- {blob.name}")

    # Télécharger les blobs
    for blob in blobs:
        blob_client = container_client.get_blob_client(blob.name)
        file_name = os.path.basename(blob.name)
        print(f"Téléchargement du fichier : {file_name}")
        with open(file_name, "wb") as file:
            file.write(blob_client.download_blob().readall())
        print(f"Fichier téléchargé : {file_name}")

except Exception as e:
    print(f"Erreur : {e}")
