import os
import pyodbc
from dotenv import load_dotenv

# Charger les variables d'environnement depuis .env
load_dotenv()

# Vérifiez que les variables sont chargées
print("DB_SERVER:", os.environ.get("DB_SERVER"))
print("DB_DATABASE:", os.environ.get("DB_DATABASE"))
print("DB_USERNAME:", os.environ.get("DB_USERNAME"))
print("DB_PASSWORD:", os.environ.get("DB_PASSWORD"))

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
    print("Connexion à la base de données...")
    conn = pyodbc.connect(connectionString)
    print("Connexion réussie!")
except pyodbc.Error as e:
    print("Erreur de connexion :")
    print(e)
