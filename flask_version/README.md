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

#### Partie 2 : Tester Flask + SQLite

On va tester l’API Flask qui utilise SQLite (une petite base de données dans un fichier).

##### 1. Préparer l’environnement virtuel

Un environnement virtuel garde les outils de Flask séparés du reste de ton ordinateur.
- Ouvre PowerShell (tape `powershell` dans la barre de recherche Windows) :

   ```powershell
   cd C:\Users\...\user-management-api\flask_version
   python -m venv venv
   .\venv\Scripts\activate
   ```

- Tu verras `(venv)` devant la ligne, ça veut dire que tu es dans un espace isolé.

##### 2. Installer les dépendances

- Vérifie que `requirements.txt` dans `flask_version` contient :
  ```
  flask==3.0.2
  flask-sqlalchemy==3.0.3
  flask-jwt-extended==4.6.0
  bcrypt==4.1.2
  pytest==8.3.5
  httpx==0.27.0
  ```

- Tape :
  ```powershell
  pip install -r requirements.txt
  ```

  - Ça installe tout ce qu’il faut pour Flask et les tests.

##### 3. Tests automatisés avec Pytest

Pytest vérifie le code automatiquement.
- Assure-toi que `tests/test_routes.py` existe puis
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

##### 4. Tests manuels avec Postman

Postman te laisse tester l’API comme un utilisateur.
- Lance l’API :
  ```powershell
  python app.py
  ```
   - Tu verras “Running on http://127.0.0.1:5000”.

- Ouvre Postman :
  - **Inscription** :
    - Nouvelle requête : `POST` > `http://127.0.0.1:5000/register`.
    - Onglet “Body” > “raw” > “JSON” :
      ```json
      {"username": "bob", "email": "bob@example.com", "password": "pass789"}
      ```
    - Clique “Send”. Résultat : `200 OK`, avec les infos de Bob.

  - **Connexion** :
    - `POST` > `http://127.0.0.1:5000/login`.
    - Body :
      ```json
      {"username": "bob", "password": "pass789"}
      ```
    - Résultat : `200 OK`, avec un `access_token` (copie-le).

  - **Profil** :
    - `GET` > `http://127.0.0.1:5000/profile`.
    - Onglet “Authorization” > “Bearer Token” > colle le token.
    - Résultat : `200 OK`, avec les infos de Bob.

  - **Mise à jour** :
    - `PUT` > `http://127.0.0.1:5000/profile`.
    - Authorization : Bearer Token.
    - Body :
      ```json
      {"email": "bob.new@example.com", "password": "newpass789"}
      ```
    - Résultat : `200 OK`.

  - **Suppression** :
    - `DELETE` > `http://127.0.0.1:5000/profile`.
    - Authorization : Bearer Token.
    - Résultat : `200 OK`, avec `"message": "Compte supprimé"`.
- Arrête l’API : `Ctrl + C`.

##### 5. Quitter l’environnement
```powershell
deactivate
```