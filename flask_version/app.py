# flask_version/app.py
from flask import Flask
from config import Config
from database import init_db
from routes import register_routes

app = Flask(__name__)
app.config.from_object(Config)
init_db(app)
register_routes(app)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
