import duckdb
import os
import pandas as pd

def convert_parquet_to_csv(input_folder, output_folder):
    """
    Convertit tous les fichiers .parquet d'un dossier en fichiers .csv et les enregistre dans un autre dossier.
    """
    # Vérifier que le dossier d'entrée existe
    if not os.path.exists(input_folder):
        raise FileNotFoundError(f"Le dossier spécifié n'existe pas : {input_folder}")

    # Créer le dossier de sortie s'il n'existe pas
    os.makedirs(output_folder, exist_ok=True)

    # Lister les fichiers .parquet dans le dossier d'entrée
    parquet_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith('.parquet')]
    
    if not parquet_files:
        raise ValueError("Aucun fichier .parquet trouvé dans le dossier spécifié.")
    
    print(f"Fichiers .parquet trouvés : {parquet_files}")
    
    # Connecter à DuckDB en mémoire
    con = duckdb.connect()

    # Traiter chaque fichier Parquet
    for parquet_file in parquet_files:
        # Charger les données dans un DataFrame
        df = con.execute(f"SELECT * FROM '{parquet_file}'").fetchdf()

        # Générer le chemin de sortie pour le fichier CSV
        base_name = os.path.basename(parquet_file).replace('.parquet', '.csv')
        output_path = os.path.join(output_folder, base_name)

        # Sauvegarder le DataFrame au format CSV
        df.to_csv(output_path, index=False)
        print(f"Fichier converti : {parquet_file} -> {output_path}")

if __name__ == "__main__":
    # Dossier contenant les fichiers .parquet
    input_folder = "data/product_eval"

    # Dossier de sortie pour les fichiers .csv
    output_folder = "data/product_eval"

    # Convertir les fichiers .parquet en .csv
    convert_parquet_to_csv(input_folder, output_folder)
