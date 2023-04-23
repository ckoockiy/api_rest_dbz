from database import db


class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), nullable=False, unique=True)
    clave = db.Column(db.String(100), nullable=False)

    def __init__(self, usuario, clave):
        self.usuario = usuario
        self.clave = clave


class Personaje(db.Model):
    __tablename__ = "personajes"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    raza = db.Column(db.String(50), nullable=False)
    planeta = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    imagen = db.Column(db.LargeBinary(), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    altura = db.Column(db.Integer, nullable=False)
    peso = db.Column(db.Integer, nullable=False)
    poderpelea = db.Column(db.Integer, nullable=False)
    habilidades = db.Column(db.String(200), nullable=False)

    def __init__(self, nombre, raza, planeta, descripcion, imagen, edad, altura, peso, poderpelea, habilidades):
        self.nombre = nombre
        self.raza = raza
        self.planeta = planeta
        self.descripcion = descripcion
        self.imagen = imagen
        self.edad = edad
        self.altura = altura
        self.peso = peso
        self.poderpelea = poderpelea
        self.habilidades = habilidades
