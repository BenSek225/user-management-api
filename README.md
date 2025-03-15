# Système de Gestion d'Utilisateurs avec API et Base de Données

Ce projet a été développé dans un but d'apprentissage pour explorer et comparer différentes technologies de développement backend en Python. Il implémente un système complet de gestion d'utilisateurs avec API RESTful en utilisant deux stacks technologiques distinctes.

## 🎯 Objectif du Projet

L'objectif principal était de créer le même système avec deux approches différentes pour mieux comprendre les avantages, inconvénients et particularités de chaque stack technologique :

- **Version Flask/SQLite** : Solution légère et simple à déployer
- **Version FastAPI/PostgreSQL** : Solution robuste et performante pour des applications à plus grande échelle

## 🛠️ Fonctionnalités Implémentées

- Gestion complète des utilisateurs (CRUD)
- Authentification sécurisée avec JWT
- Protection des routes par middleware d'authentification
- Tests automatisés avec Pytest
- Validation des données

## 📚 Structure du Projet

```
📂 user-management-api/
│── 📂 flask_version/              # Implémentation avec Flask + SQLite
│    ├── app.py                    # Point d'entrée Flask
│    ├── config.py                 # Configuration
│    ├── models.py                 # Modèle SQLAlchemy
│    ├── routes.py                 # Routes API REST
│    ├── database.py               # Gestion de la BDD SQLite
│    ├── tests/                    # Tests unitaires
│
│── 📂 fastapi_version/            # Implémentation avec FastAPI + PostgreSQL
│    ├── main.py                   # Point d'entrée FastAPI
│    ├── config.py                 # Configuration
│    ├── models.py                 # Modèle SQLAlchemy + Pydantic
│    ├── routes.py                 # Routes API REST
│    ├── database.py               # Connexion PostgreSQL
│    ├── tests/                    # Tests unitaires
```

## 🔍 Technologies Utilisées

### Version Flask/SQLite
- **Framework Web** : Flask
- **Base de données** : SQLite
- **ORM** : SQLAlchemy
- **Authentification** : Flask-JWT-Extended
- **Validation** : Marshmallow

### Version FastAPI/PostgreSQL
- **Framework Web** : FastAPI
- **Base de données** : PostgreSQL
- **ORM** : SQLAlchemy avec Pydantic
- **Authentification** : PyJWT
- **Documentation API** : Swagger UI (intégré à FastAPI)

## 🚀 Installation et Démarrage

### Prérequis
- Python 3.x
- Postman (pour les tests manuels)
- PostgreSQL (pour la version FastAPI)

### Étapes d'installation

1. Cloner le dépôt
```bash
git clone https://github.com/votre-username/user-management-api.git
cd user-management-api
```

2. Créer et activer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. Installer les dépendances pour la version souhaitée
```bash
# Pour Flask
cd flask_version
pip install -r requirements.txt

# Pour FastAPI
cd ../fastapi_version
pip install -r requirements.txt
```

4. Configuration
   - Pour la version Flask, aucune configuration supplémentaire n'est nécessaire
   - Pour la version FastAPI, configurez les variables d'environnement pour PostgreSQL

5. Lancer l'application
```bash
# Flask
cd flask_version
python app.py

# FastAPI
cd fastapi_version
uvicorn main:app --reload
```

## 📝 Notes d'apprentissage

Ce projet m'a permis d'explorer les différences entre :

- La simplicité de Flask vs la performance et les fonctionnalités modernes de FastAPI
- La légèreté de SQLite vs la robustesse de PostgreSQL
- Les approches différentes pour la validation des données
- La documentation automatique avec FastAPI

## 📖 Ressources d'apprentissage

- [Documentation Flask](https://flask.palletsprojects.com/)
- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [PostgreSQL](https://www.postgresql.org/docs/)

## 📋 À faire / Améliorations possibles

- Implémentation de rôles utilisateurs (admin, utilisateur standard)
- Interface utilisateur frontend
- Système de gestion des mots de passe oubliés

---


*Ce projet a été créé dans un but éducatif pour explorer et comparer différentes technologies de développement backend en Python.*