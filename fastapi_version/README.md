### Explication sur comment tester l'API

Le code est déjà écrit et fonctionne. Je vais t’expliquer comment installer les outils, installer un environnement virtuel, et tester les fonctionnalités (inscription, connexion, profil, mise à jour, suppression) avec des tests automatisés (Pytest) et manuels (Postman). On part de zéro, comme si tu découvrais tout pour la première fois.

---

#### Partie 1 : Installer les outils de base

Avant de tester, il faut installer quelques outils sur ton ordinateur Windows.

1. **Python** (le moteur qui fait tourner le code) :
   - Ouvre l’invite de commandes : appuie sur `Win + R`, tape `cmd`, et presse Entrée.
   - Tape `python --version`. Si tu vois `Python 3.12.x`, c’est bon. Sinon :
      - Va sur [python.org/downloads](https://www.python.org/downloads/).
      - Télécharge la dernière version (ex. 3.12.6) en cliquant sur “Download Python 3.x.x”.
      - Ouvre le fichier `.exe`, coche **“Add Python 3.x to PATH”** (important pour que ça marche partout), et clique “Install Now”.
      - Re-tape `python --version` pour vérifier.

2. **Visual Studio Code** (pour voir et modifier le code) :
   - Télécharge-le sur [code.visualstudio.com](https://code.visualstudio.com).
   - Installe-le en cliquant “Suivant” jusqu’à la fin.
   - Ouvre VS Code, clique sur l’icône des extensions (carrés à gauche), cherche “Python”, et installe celle de Microsoft.

3. **Postman** (pour tester l’API avec une interface simple) :
   - Va sur [postman.com/downloads](https://www.postman.com/downloads/).
   - Télécharge la version Windows, installe-la (double-clic, “Suivant”), et ouvre Postman.

4. **PostgreSQL** (base de données pour FastAPI) :
   - Télécharge-le sur [postgresql.org/download/windows](https://www.postgresql.org/download/windows/) via “Interactive Installer by EDB” (ex. version 15.x).
   - Lance l’installateur :
      - Accepte le dossier par défaut.
      - Choisis un mot de passe pour l’utilisateur `postgres` (ex. `Ben_Sek_PostgreSQL`), note-le.
      - Garde le port 5432 et clique “Suivant” jusqu’à la fin.
   - Ouvre **pgAdmin 4** (installé avec PostgreSQL) :
      - Connecte-toi avec `postgres` et ton mot de passe.
      - Clic droit sur “Databases” dans l’arbre à gauche > “Create” > “Database”.
      - Nomme-la `users_db` et clique “Save”.

---

#### Partie 2 :  Tester FastAPI + PostgreSQL
On teste maintenant FastAPI, qui utilise une base de données PostgreSQL.

##### 1. Préparer l’environnement virtuel
- Ouvre PowerShell :
  ```powershell
  cd C:\Users\...\user-management-api\fastapi_version
  python -m venv venv
  .\venv\Scripts\activate
  ```

##### 2. Installer les dépendances
- Vérifie `requirements.txt` dans `fastapi_version` :
  ```
  fastapi==0.110.0
  uvicorn==0.29.0
  sqlalchemy==2.0.29
  psycopg2-binary==2.9.9
  pydantic[email]==2.6.4
  pyjwt==2.8.0
  bcrypt==4.1.2
  pytest==8.3.5
  pytest-asyncio==0.25.3
  httpx==0.27.0
  ```
- Tape :
  ```powershell
  pip install -r requirements.txt
  ```

##### 3. Configurer PostgreSQL
- Ouvre pgAdmin 4, connecte-toi avec tes id (`postgres`) et (`monmotdepasse123`).
- Vérifie que `users_db` existe (sinon, crée-la comme dans la Partie 1).

##### 4. Tests automatisés avec Pytest
FastAPI est asynchrone, donc on ajoute une configuration.
- Crée `pytest.ini` dans `fastapi_version` :
  ```ini
  [pytest]
  asyncio_mode = strict
  asyncio_default_fixture_loop_scope = function
  ```

- Vérifie `tests/test_routes.py` :
  ```python
  # fastapi_version/tests/test_routes.py
  import pytest
  import pytest_asyncio
  import sys
  import os
  from httpx import AsyncClient, ASGITransport
  sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
  from main import app
  from database import Base, engine

  @pytest_asyncio.fixture
  async def client():
      async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
          Base.metadata.create_all(bind=engine)
          yield ac
          Base.metadata.drop_all(bind=engine)
  @pytest.mark.asyncio
  async def test_register(client):
      response = await client.post("/register", json={
          "username": "test",
          "email": "test@example.com",
          "password": "pass123"
      })
      assert response.status_code == 200
      assert response.json()["username"] == "test"
  @pytest.mark.asyncio
  async def test_login(client):
      await client.post("/register", json={
          "username": "test",
          "email": "test@example.com",
          "password": "pass123"
      })
      response = await client.post("/login", json={
          "username": "test",
          "password": "pass123"
      })
      assert response.status_code == 200
      assert "access_token" in response.json()
  ```

- Lance les tests :
  ```powershell
  pytest tests/test_routes.py -v
  ```

- Résultat attendu :
  ```
  ============================= test session starts =============================
  collected 2 items
  tests/test_routes.py::test_register PASSED
  tests/test_routes.py::test_login PASSED
  ============================= 2 passed in x.xx seconds =============================
  ```

##### 5. Tests manuels avec Postman
- Lance l’API :
  ```powershell
  python main.py
  ```
  - Tu verras “Uvicorn running on http://0.0.0.0:8000”.
- Ouvre Postman :

  - **Inscription** :
    - `POST` > `http://localhost:8000/register`.
    - Body :
      ```json
      {"username": "alicia", "email": "alicia@example.com", "password": "pass456"}
      ```
    - Résultat : `200 OK`.

  - **Connexion** :
    - `POST` > `http://localhost:8000/login`.
    - Body :
      ```json
      {"username": "alicia", "password": "pass456"}
      ```
    - Résultat : `200 OK`, avec `access_token` (copie-le).

  - **Profil** :
    - `GET` > `http://localhost:8000/profile`.
    - Authorization : Bearer Token > colle le token.
    - Résultat : `200 OK`, avec les infos d’Alicia.

  - **Mise à jour** :
    - `PUT` > `http://localhost:8000/profile`.
    - Authorization : Bearer Token.
    - Body :
      ```json
      {"email": "alicia.new@example.com", "password": "newpass456"}
      ```
    - Résultat : `200 OK`.

  - **Suppression** :
    - `DELETE` > `http://localhost:8000/profile`.
    - Authorization : Bearer Token.
    - Résultat : `200 OK`, avec `"message": "Compte supprimé"`.
- Arrête l’API : `Ctrl + C`.

##### 6. Quitter l’environnement
```powershell
deactivate
```

##### Bonus : Interface Swagger
- Lance l’API (`python main.py`), ouvre ton navigateur à `http://localhost:8000/docs`.
- Tu peux tester les routes directement dans cette page interactive !

---
