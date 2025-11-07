#  FireFlow API

**FireFlow** est une API REST développée en **Python / Flask**, permettant de gérer des *firewalls*, *policies* et *rules*.  
Elle intègre la documentation Swagger, une authentification **JWT**, et des tests unitaires avec **Pytest**.  

---

##  Installation locale

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

### Lancer l'application
```bash
flask run
```

L'API sera accessible à l'adresse : `http://127.0.0.1:5000/`

La documentation Swagger est disponible à l'adresse : `http://127.0.0.1:5000/docs`

## Exécution avec Docker
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

## Lancer les tests unitaires
```bash
pytest -v
```

