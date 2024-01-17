# SER-APP Documentation

SERAPP est une applcation qui permet de détecter les émotions en se basant sur la voix sans la sémantique.

## Installations et déploiement
Pour déployer ce projet, vous aurez besoin de faire quelques installations:
- Python (la version 3.10 de python serait idéale) https://www.python.org/downloads/.
- Node: Assurez-vous d'avoir Node.js et npm installés

### 1. Installations
Une fois python installé, ouvrez le projet dans votre éditeur et installer les packages nécessaires. Nous vous recommandons de créer un environnement virtuel pour votre projet.

#### Commande de création et d'utilisation d'un environnement virtuel:
    - python3 -m venv .venv
    - source .venv/bin/activate

La  première commande permet de créer l'environnement et la seconde vous permet d'activer votre environnement.

#### Les installations de bibliothèques python à installer

    - pip install flask
    - pip install flask_cors
    - pip install joblib
    - pip install librosa
Ces installations peuvent se faire en étant dans la racine du projet.

Nous allons maintenant faire les installations nécessaires pour le projet NodeJS (démonstrateur). Pour cela, rendez vous dans le dossier `demonstrateur`.

Installez les Dépendances

    - npm install

Si vous avez des erreur à ce niveau, vous pouvez utiliser la commande
npm audit fix --force, pour forcer la mise à jour des packages.

Installez React et React-DOM avec les commandes:
    
    - npm install react react-dom

Installez axios avec la commande:
   
    - npm install axios

Installez React-Bootstrap et Bootstrap : 

    - npm install react-bootstrap bootstrap
    - npm install react-icons

Et c'est bon 👍🏼 !!! Vous êtes maintenant prêt à déployer votre application.

### 2. Déploiement
#### Déploiement de l'API
Ouvrez un premier terminal dans le dossier `api`

    - python main.py

#### Déploielent du démonstrateur
Ouvrez un second terminal dans le dossier `demonstrateur`

    -  npm start

