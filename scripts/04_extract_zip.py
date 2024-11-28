import zipfile
import tarfile
import os

def extract_zip_file(zip_path, output_folder=None):
    """
    Extrait le contenu d'un fichier .zip dans un dossier spécifié ou à côté du fichier .zip.
    """
    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"Le fichier .zip spécifié n'existe pas : {zip_path}")
    
    if output_folder is None:
        output_folder = os.path.splitext(zip_path)[0]
    
    os.makedirs(output_folder, exist_ok=True)
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(output_folder)
        print(f"Fichiers extraits du .zip dans : {output_folder}")
    
    return output_folder

def extract_tgz_file(tgz_path, output_folder=None):
    """
    Extrait le contenu d'un fichier .tgz dans un dossier spécifié ou à côté du fichier .tgz.
    """
    if not os.path.exists(tgz_path):
        raise FileNotFoundError(f"Le fichier .tgz spécifié n'existe pas : {tgz_path}")
    
    if output_folder is None:
        output_folder = os.path.splitext(tgz_path)[0]
    
    os.makedirs(output_folder, exist_ok=True)
    
    with tarfile.open(tgz_path, 'r:gz') as tar_ref:
        tar_ref.extractall(output_folder)
        print(f"Fichiers extraits du .tgz dans : {output_folder}")
    
    return output_folder

def process_files(zip_path):
    """
    Gère l'extraction d'un fichier .zip, puis d'un fichier .tgz s'il est présent dans le contenu extrait.
    """
    # Étape 1 : Extraire le fichier .zip
    zip_output_folder = extract_zip_file(zip_path)
    
    # Étape 2 : Chercher un fichier .tgz dans le dossier extrait
    for root, _, files in os.walk(zip_output_folder):
        for file in files:
            if file.endswith('.tgz'):
                tgz_path = os.path.join(root, file)
                print(f"Fichier .tgz trouvé : {tgz_path}")
                
                # Extraire le fichier .tgz
                extract_tgz_file(tgz_path, root)
                print(f"Extraction terminée pour : {tgz_path}")

if __name__ == "__main__":
    # Chemin vers le fichier .zip initial
    zip_path = "data/machine_learning/reviews.zip"

    # Lancer le processus
    process_files(zip_path)
