from azure.storage.blob import ContainerClient
from dotenv import load_dotenv
import os

def print_blob_hierarchy(container_client):
    """
    Affiche l'arborescence des blobs dans le conteneur.
    """
    print("Arborescence des blobs dans le conteneur :")
    blob_names = [blob.name for blob in container_client.list_blobs()]
    
    # Organiser les blobs en une arborescence
    file_tree = {}
    for blob_name in blob_names:
        print(blob_name)
        parts = blob_name.split('/')
        current_level = file_tree
        for part in parts:
            current_level = current_level.setdefault(part, {})
    
    # Afficher l'arborescence
    def print_tree(tree, indent=""):
        for key, subtree in tree.items():
            print(f"{indent}{key}")
            if isinstance(subtree, dict):
                print_tree(subtree, indent + "  ")

    print_tree(file_tree)

def download_blob(container_client, blob_name, local_folder):
    """
    Télécharge un fichier blob spécifique depuis Azure et le sauvegarde localement.
    """
    local_path = os.path.join(local_folder, blob_name)  # Construire le chemin local correspondant
    os.makedirs(os.path.dirname(local_path), exist_ok=True)  # Créer le dossier local si nécessaire

    # Télécharger le fichier
    print(f"Téléchargement du fichier : {blob_name}")
    with open(local_path, "wb") as file:
        blob_data = container_client.get_blob_client(blob_name).download_blob()
        file.write(blob_data.readall())

def download_blobs_from_sas_url(sas_url, local_folder):
    # Créer un client ContainerClient à partir de l'URL SAS
    container_client = ContainerClient.from_container_url(container_url=sas_url)

    # Créer le dossier local racine si nécessaire
    os.makedirs(local_folder, exist_ok=True)

    # Lister tous les blobs et traiter chaque chemin
    print("Liste des blobs dans le conteneur :")
    
    # Lister tous les blobs
    blobs = container_client.list_blobs()

    # Télécharger récursivement les blobs et créer des dossiers le cas échéant
    for blob in blobs:
        blob_name = blob.name
        if '.' in os.path.basename(blob_name):  # Vérifier si c'est un fichier
            download_blob(container_client, blob_name, local_folder)
        else:
            print(f"Création du dossier : {blob_name}")
            # Créer le dossier correspondant localement sans télécharger de fichier
            os.makedirs(os.path.join(local_folder, blob_name), exist_ok=True)

    print("Tous les blobs ont été téléchargés.")

if __name__ == '__main__':
    # Charger les variables d'environnement depuis le fichier .env
    load_dotenv()

    # Charger l'URL SAS depuis le fichier .env
    sas_url = os.getenv("SAS_URL")

    if not sas_url:
        raise ValueError("Erreur : SAS_URL n'est pas défini dans le fichier .env")
    
    # Dossier où télécharger les blobs
    local_folder = "data"

    # Afficher l'arborescence des blobs dans le conteneur
    container_client = ContainerClient.from_container_url(container_url=sas_url)
    print_blob_hierarchy(container_client)

    # Demander confirmation avant de commencer le téléchargement
    input("Appuyez sur Entrée pour commencer le téléchargement...")

    # Télécharger tous les blobs récursivement
    download_blobs_from_sas_url(sas_url, local_folder)
