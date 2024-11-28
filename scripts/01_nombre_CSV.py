import os

def count_csv_files(directory):
    csv_count = 0
    for root, _, files in os.walk(directory):
        csv_count += sum(1 for file in files if file.endswith('.csv'))
    return csv_count

# Chemin du dossier data
data_dir = "data"

if os.path.exists(data_dir):
    total_csv = count_csv_files(data_dir)
    print(f"Le nombre total de fichiers CSV dans '{data_dir}' et ses sous-dossiers est : {total_csv}")
else:
    print(f"Le dossier '{data_dir}' n'existe pas.")
