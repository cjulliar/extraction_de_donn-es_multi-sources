import os
import pandas as pd
import pyodbc
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

# Configuration de la chaîne de connexion
SERVER = os.environ.get("DB_SERVER")
DATABASE = os.environ.get("DB_DATABASE")
USERNAME = os.environ.get("DB_USERNAME")
PASSWORD = os.environ.get("DB_PASSWORD")

connectionString = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"UID={USERNAME};"
    f"PWD={PASSWORD};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
    f"Connection Timeout=30;"
)

try:
    # Liste des schémas à traiter
    schemas = ["Person", "Production", "Sales"]

    print("Connexion à la base de données...")
    conn = pyodbc.connect(connectionString)
    print("Connexion réussie!")
    
    cursor = conn.cursor()
    
    for schema in schemas:
        # Créer le dossier pour chaque schéma et le nettoyer
        output_dir = os.path.join("data", schema.lower())
        if os.path.exists(output_dir):
            for file in os.listdir(output_dir):
                os.remove(os.path.join(output_dir, file))  # Supprimer les fichiers existants
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"\nTraitement du schéma : {schema}")
        
        # Lister toutes les tables du schéma actuel (exclure les vues)
        cursor.execute(f"""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = '{schema}' AND TABLE_TYPE = 'BASE TABLE'
        """)
        tables = cursor.fetchall()
        
        if not tables:
            print(f"Aucune table trouvée dans le schéma '{schema}'.")
            continue
        
        print(f"Tables trouvées dans le schéma '{schema}':")
        
        for table in tables:
            table_name = table.TABLE_NAME
            try:
                print(f"\nLecture des données de la table : {table_name}")
                
                # Lire les données de la table
                query = f"SELECT * FROM {schema}.{table_name}"
                df = pd.read_sql(query, conn)
                
                # Vérifier si la table contient des données
                if df.empty:
                    print(f"La table '{table_name}' est vide. Aucun fichier généré.")
                    continue
                
                # Exporter les données de la table dans un fichier CSV
                output_file = os.path.join(output_dir, f"{table_name}.csv")
                df.to_csv(output_file, index=False)
                print(f"Les données de la table '{table_name}' ont été exportées dans le fichier '{output_file}'.")
            except Exception as e:
                print(f"Erreur lors de la lecture ou de l'exportation de la table {table_name} : {e}")
    
    # Fermer la connexion
    cursor.close()
    conn.close()
except pyodbc.Error as e:
    print("Erreur :")
    print(e)