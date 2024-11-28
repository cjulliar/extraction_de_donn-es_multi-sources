
# Automatisation du Projet avec Cron

  

Ce projet automatise plusieurs scripts Python et Bash, tout en utilisant un environnement virtuel Python et un cron job pour leur exécution. Ce guide explique comment configurer les variables nécessaires dans le fichier `.env`, déployer le projet, et exécuter le cron job.

  

---

  

## Configuration du fichier `.env`

  

Le fichier `.env` contient toutes les variables nécessaires pour le bon fonctionnement des scripts. Voici les informations que vous devez inclure :

  

### 1. Informations sur la base de données

Ces variables permettent à vos scripts de se connecter à une base de données (par exemple, SQL Server ou Azure SQL) :

-  **`DB_SERVER`** : L'adresse ou le nom de votre serveur de base de données.

- Exemple : `monserveur.database.windows.net`

-  **`DB_DATABASE`** : Le nom de la base de données cible.

- Exemple : `ma_base_de_donnees`

-  **`DB_USERNAME`** : Le nom d'utilisateur pour accéder à la base de données.

- Exemple : `mon_utilisateur`

-  **`DB_PASSWORD`** : Le mot de passe associé à cet utilisateur.

- Exemple : `mot_de_passe_securise`



### 2. Répertoire du projet

Cette variable spécifie le chemin absolu du projet sur votre machine ou serveur :

-  **`PROJECT_DIR`** : Le chemin absolu vers le dossier racine du projet.

- Exemple : `/chemin/absolu/vers/votre/projet`


### 3. Connexion au stockage Azure

Ces variables permettent aux scripts de se connecter à un compte de stockage Azure :

-  **`STORAGE_CONNEXION`** : La chaîne de connexion complète pour votre compte de stockage Azure.

- Exemple : `'DefaultEndpointsProtocol=https;AccountName=moncompte;AccountKey=cle_de_connexion;EndpointSuffix=core.windows.net'`

-  **`STORAGE_ACCOUNT`** : Le nom du compte de stockage.

- Exemple : `moncompte`

-  **`STORAGE_CONTAINER`** : Le nom du conteneur dans votre compte de stockage Azure.

- Exemple : `mon_conteneur`

 

### 4. Jetons d'accès SAS

Ces variables permettent d'accéder aux ressources protégées avec un jeton SAS (Shared Access Signature) :

-  **`SAS_TOKEN`** : Le jeton SAS généré pour accéder à votre conteneur.

- Exemple : `'sp=r&st=2024-11-26T13:15:32Z&se=2024-11-26T21:15:32Z&...sig=signature'`


### 5. ID de l'abonnement Azure

Cette variable est utilisée pour identifier votre abonnement Azure :

-  **`SUBSCRIPTION_ID`** : L'ID unique de votre abonnement Azure.

- Exemple : `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

  

---

  

## Prérequis

  

1.  **Python 3** (avec `venv` supporté).

2.  **Bash** pour exécuter les scripts.

3.  **Accès au fichier `.env` correctement configuré**.

  

---

  

## Étapes d'installation

  

### 1. Configurer le fichier `.env`

Ajoutez toutes les variables mentionnées ci-dessus dans un fichier `.env` à la racine de votre projet.

  

### 2. Rendre le script Bash exécutable

À la racine du projet, rendez le script `install.sh` exécutable :

```bash

chmod  +x  install.sh

```

## Configuration du Cron Job sur le Serveur

  

### 1. Vérifier si cron est installé

Pour  vous  assurer  que  cron  est  disponible  sur  votre  serveur,  tapez  la  commande  suivante  :

  

```crontab  -l```

Si la commande renvoie une erreur ou si cron n'est pas installé, suivez les instructions ci-dessous pour l'installer.

  

Installer cron sur Debian/Ubuntu :

```
sudo  apt  update

sudo apt install cron
```

Installer cron sur Red Hat/CentOS :

```
sudo yum install cronie

sudo systemctl start crond

sudo systemctl enable crond
```

### 2. Ajouter le Cron Job

Pour exécuter le script Bash tous les jours à 3h du matin :

  

Ouvrez l'éditeur cron :

  
```
crontab -e
```
Ajoutez la ligne suivante dans l'éditeur, en remplaçant /chemin/absolu/vers/votre/projet par le chemin absolu de votre projet :

  
```
0  3  *  *  * /chemin/absolu/vers/votre/projet/install.sh >> /chemin/absolu/vers/votre/projet/cron_log.txt 2>&1
```



###  3. Sauvegarder et quitter

Si vous utilisez l'éditeur Nano :
```
Appuyez sur Ctrl+O pour sauvegarder.

Appuyez sur Entrée pour confirmer.

Appuyez sur Ctrl+X pour quitter l'éditeur.
```

## **Vérifications et Dépannage**

### **Vérifier les tâches Cron actives**

Pour lister toutes les tâches cron configurées :

Copier le code dans votre bash
```
crontab -l
```