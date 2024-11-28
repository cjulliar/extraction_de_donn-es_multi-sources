import pandas as pd
from PIL import Image
import os
import io
from tqdm import tqdm

def process_images_and_update_csv(csv_path, base_output_folder, image_column="image", id_column="item_ID", output_format="jpeg"):
    """
    Lit un fichier CSV, extrait toutes les images, les sauvegarde dans un dossier,
    et met à jour le fichier CSV en remplaçant la colonne 'image' par les noms des fichiers image.
    """
    # Charger le fichier CSV
    df = pd.read_csv(csv_path)
    
    if image_column not in df.columns:
        raise ValueError(f"La colonne '{image_column}' n'existe pas dans le fichier CSV.")
    
    if id_column not in df.columns:
        raise ValueError(f"La colonne '{id_column}' n'existe pas dans le fichier CSV.")
    
    # Déterminer le nom du sous-dossier à partir du nom du fichier CSV
    csv_name = os.path.splitext(os.path.basename(csv_path))[0]
    output_folder = os.path.join(base_output_folder, csv_name)
    os.makedirs(output_folder, exist_ok=True)

    # Compteurs pour le rapport
    total_images = 0
    invalid_rows = 0

    # Parcourir toutes les lignes du CSV pour extraire et sauvegarder les images
    for index, row in tqdm(df.iterrows(), total=len(df), desc=f"Traitement {csv_name}"):
        if isinstance(row[image_column], str) and row[image_column].startswith("{'bytes': b"):
            # Extraire les données brutes (bytes) de la chaîne
            try:
                image_data = eval(row[image_column])['bytes']
            except Exception as e:
                print(f"Erreur lors de l'extraction des bytes à l'indice {index}: {e}")
                invalid_rows += 1
                continue
            
            # Utiliser item_ID comme nom du fichier
            item_id = row[id_column]
            if not isinstance(item_id, str) or not item_id.startswith("id-"):
                print(f"item_ID invalide à l'indice {index}: {item_id}")
                invalid_rows += 1
                continue
            
            image_name = f"{item_id}.{output_format}"
            
            # Sauvegarder l'image
            try:
                image = Image.open(io.BytesIO(image_data))
                image = image.convert('RGB')
                output_path = os.path.join(output_folder, image_name)
                image.save(output_path, format=output_format.upper())
                
                # Remplacer la valeur de la colonne 'image' par le nom du fichier image
                df.at[index, image_column] = image_name
                total_images += 1
            except Exception as e:
                print(f"Erreur lors de la conversion de l'image pour item_ID {item_id} à l'indice {index}: {e}")
                invalid_rows += 1
        else:
            invalid_rows += 1

    # Mettre à jour le fichier CSV avec les nouveaux noms dans la colonne 'image'
    df.to_csv(csv_path, index=False)
    print(f"Fichier CSV mis à jour : {csv_path}")
    print(f"Résumé pour {csv_name} : {total_images} images générées, {invalid_rows} lignes invalides.")

def process_all_csvs_in_folder(input_folder, base_output_folder, image_column="image", id_column="item_ID", output_format="jpeg"):
    """
    Parcourt tous les fichiers CSV dans un dossier, traite les images et met à jour les fichiers CSV.
    """
    if not os.path.exists(input_folder):
        raise FileNotFoundError(f"Le dossier spécifié n'existe pas : {input_folder}")
    
    # Lister tous les fichiers CSV dans le dossier
    csv_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.csv')]
    
    if not csv_files:
        print("Aucun fichier CSV trouvé dans le dossier spécifié.")
        return
    
    # Traiter chaque fichier CSV
    for csv_file in csv_files:
        print(f"Traitement du fichier : {csv_file}")
        process_images_and_update_csv(csv_file, base_output_folder, image_column, id_column, output_format)

if __name__ == "__main__":
    # Dossier contenant les fichiers CSV
    input_folder = "analyse_data/product_eval"

    # Dossier de base pour stocker les images
    base_output_folder = "analyse_data/product_eval/image"

    # Traiter tous les fichiers CSV dans le dossier
    process_all_csvs_in_folder(input_folder, base_output_folder, image_column="image", id_column="item_ID", output_format="jpeg")
