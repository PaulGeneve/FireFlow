#  FireFlow API
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0+-green.svg)

**FireFlow** est une API REST développée en **Python / Flask**, permettant de gérer des *firewalls*, *policies* et *rules*.  
Elle intègre la documentation Swagger, une authentification **JWT**, et des tests unitaires avec **Pytest**.  

---

## 📦 Installation locale

### Cloner le projet
```bash
git clone https://github.com/PaulGeneve/FireFlow.git
cd FireFlow
```

### Créer un environnement virtuel
```bash
python3 -m venv venv

source venv/bin/activate  # Sur macOS/Linux

venv\Scripts\activate # Sur Windows
```
### Installer les dépendances
```bash
pip install -r requirements.txt
```
### Créer un fichier `.env` à la racine du projet 
Ce fichier contiendra la clé JWT utilisée pour signer les tokens :
```env
JWT_SECRET_KEY=votre_cle_secrete
```

### Populer la base de données initiale
la commande suivante va créer une base de données SQLite `instance/fireflow.db`  et y insérer des données initiales :
```bash
flask populate_db.py
```

### Lancer l'application
```bash
flask run
```

L'API sera accessible à l'adresse : `http://127.0.0.1:5000/`

La documentation Swagger est disponible à l'adresse : `http://127.0.0.1:5000/docs`

## 🐳 Exécution avec Docker
### Construire l'image Docker
```bash
docker build -t fireflow-api .
```

### Lancer le conteneur Docker
```bash
docker run -d -p 8080:8080 --name fireflow --env-file .env fireflow
```

L'API sera accessible à l'adresse : `http://localhost:8080/`

La documentation Swagger est disponible à l'adresse : `http://localhost:8080/docs`

## Lancer les tests 
Assurez-vous d'avoir installé les dépendances de test listées dans `requirements.txt`, puis exécutez la commande suivante depuis la racine du projet :
```bash
pytest -v
```
Lest Tests prennent en charge la création d'une base de données SQLite temporaire pour isoler les tests de l'environnement de développement.

## Authentification
Lors de votre premiere visiste dans l'API, vous devez créer un utilisateur administrateur en envoyant une requête POST à l'endpoint `/auth/register` avec un payload JSON contenant un `name` et un `password` ou utiliser un user existant dans la base de données si vous avez lancer la command `flask populate-db`.

Ensuite, pour obtenir un token JWT, envoyez une requête POST à l'endpoint `/auth/login` avec le même payload JSON.
Le token JWT doit être inclus dans l'en-tête `Authorization`, Depuis la documentation Swagger, cliquez sur "Authorize" et entrez votre token.


### Exemples d'utilisation

**1. Se connecter (avec utilisateur créer depuis `flask populate-bd.py`) :**
```bash
curl -X POST http://127.0.0.1:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"name": "paul", "password": "paul123"}'
```

**2. Lister les firewalls :**
```bash
curl -H "Authorization: Bearer " \
  http://127.0.0.1:5000/firewalls
```

## Structure du projet
```
firewall-manager/
├── app.py                     # App factory
├── extensions.py              # DB, JWT init
├── config.py                  # Configuration de l'application
├── instance/                  # Fichiers d'instance (ex: base de données SQLite
│   └── fireflow.db
├── tests/                     # Tests d'intégration et unitaires
│   ├── conftest.py            # Fixtures pour les tests
│   ├── test_base_service.py   # Tests généraux
├── ressources/
│   ├── auth/                  # Authentification
│   │
│   ├── firewalls/             # Entité Métier complete avec (routes, schémas, services)
│   ├── policies/
│   ├── rules/              
│   │
│   └── services               # Generic CRUD
├── models/                    # SQLAlchemy models
└── scripts/                   # Scripts utilitaires
    └── populate_db.py         # Populer la base de données
```

## Stack technique
- Python 3.8+
- Flask
- Flask-Smorest
- Flask-JWT-Extended
- SQLAlchemy
- Marshmallow
- Pytest
- Docker



