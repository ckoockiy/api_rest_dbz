from flask import Flask
from database import db
from sqlalchemy_utils import create_database, database_exists


app = Flask(__name__)

# Base de datos
db_usuario = ""
db_clave = ""
db_host = ""
db_nombre = ""

DB_URL = f"mysql+pymysql://{db_usuario}:{db_clave}@{db_host}/{db_nombre}"

#inicializamos SQLAlchemy
db.init_app(app)

@app.route('/', methods=['GET'])
def inicio():
    return "<h1>Hola</h1>"


# Creamos la base de datos
with app.app_context():
    if not database_exists(DB_URL):
        create_database(DB_URL)
    db.create_all()


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5000)
