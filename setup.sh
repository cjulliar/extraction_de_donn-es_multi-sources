#!/bin/bash

echo "Début de l'installation de l'environnement..."

# Vérification des privilèges
if [[ "$EUID" -ne 0 ]]; then
  echo "Veuillez exécuter ce script avec sudo."
  exit 1
fi

# Installer les dépendances système si nécessaire
echo "Installation des dépendances système..."
brew install python3 unixodbc
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
ACCEPT_EULA=Y brew install msodbcsql17

# Vérifier que le pilote ODBC est installé
if [[ ! -f "/usr/local/lib/libmsodbcsql.17.dylib" ]]; then
  echo "Erreur : Le pilote ODBC pour SQL Server n'a pas été correctement installé."
  exit 1
fi

echo "Pilote ODBC installé avec succès."

# Configuration des fichiers ODBC
echo "Configuration de odbcinst.ini..."
ODBC_INST_FILE="/usr/local/etc/odbcinst.ini"
if [[ ! -f "$ODBC_INST_FILE" ]]; then
  echo "Création de $ODBC_INST_FILE..."
  cat <<EOL > "$ODBC_INST_FILE"
[ODBC Driver 17 for SQL Server]
Description=Microsoft ODBC Driver 17 for SQL Server
Driver=/usr/local/lib/libmsodbcsql.17.dylib
UsageCount=1
EOL
else
  echo "$ODBC_INST_FILE existe déjà."
fi

# Créer un environnement virtuel Python
echo "Création de l'environnement virtuel Python..."
python3 -m venv env
source env/bin/activate

# Installer les dépendances Python
echo "Installation des dépendances Python depuis requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Environnement prêt. Pour activer l'environnement, exécutez :"
echo "source env/bin/activate"
