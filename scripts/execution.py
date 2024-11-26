import os
import subprocess
import shutil

# Définir le chemin du dossier à nettoyer
data_dir = "data"

# Nettoyage du dossier 'data/'
def clean_data_directory():
    if os.path.exists(data_dir):
        print(f"Nettoyage du dossier : {data_dir}")
        shutil.rmtree(data_dir)  # Supprime complètement le dossier
    os.makedirs(data_dir)  # Recrée un dossier vide
    print(f"Dossier '{data_dir}' nettoyé et recréé.")

# Exécution d'un script Python
def execute_script(script_path):
    try:
        print(f"Exécution du script : {script_path}")
        result = subprocess.run(["python", script_path], check=True, capture_output=True, text=True)
        print(f"--- Sortie du script {script_path} ---")
        print(result.stdout)
        print(f"--- Fin de sortie du script {script_path} ---\n")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution du script {script_path} : {e}")
        print(e.stderr)

# Liste des scripts à exécuter dans l'ordre
scripts = [
    "scripts/total_generation_CSV.py",
    "scripts/nombre_CSV.py"
]

# Nettoyer le dossier 'data/'
clean_data_directory()

# Exécuter les scripts
for script in scripts:
    execute_script(script)

print("Tous les scripts ont été exécutés.")
