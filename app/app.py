from flask import Flask
from database import db
from sqlalchemy_utils import create_database, database_exists
from routes.routes import blue_print
from flask_jwt_extended import JWTManager
import os
import datetime

# generar llave aleatoria
secret_key = os.urandom(24)

UPLOAD_FOLDER = os.path.abspath("app/uploads")
ALLOWED_EXTENSIONS = {"png"}


app = Flask(__name__)

# Base de datos
db_usuario = "root"
db_clave = "theCRONY.13"
db_host = "localhost"
db_nombre = "db_api_dbz"

DB_URL = f"mysql+pymysql://{db_usuario}:{db_clave}@{db_host}/{db_nombre}"

app.config["SQLALCHEMY_DATABASE_URI"] = DB_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# asignar la llave a la configuración de Flask-JWT
app.config['JWT_SECRET_KEY'] = secret_key
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=1)

# carpeta de archivos
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["ALLOWED_EXTENSIONS"] = ALLOWED_EXTENSIONS


# JWT
jwt = JWTManager(app)
# inicializamos SQLAlchemy
db.init_app(app)


# instanciamos las rutas
app.register_blueprint(blue_print)


# Creamos la base de datos
with app.app_context():
    if not database_exists(DB_URL):
        create_database(DB_URL)
    db.create_all()


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)
