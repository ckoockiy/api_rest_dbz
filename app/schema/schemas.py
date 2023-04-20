from flask_marshmallow import Marshmallow

ma = Marshmallow()


# Esquema usuario
class UsuarioSchema(ma.Schema):
    class Meta:
        fields = ("id", "usuario", "clave")


# Esquema personajes
class PersonajesSchema(ma.Schema):
    class Meta:
        fields = ("id", "nombre", "raza", "planeta", "descripcion", "imagen",
                  "edad", "altura", "peso", "poderpelea", "habilidades")


personaje_schema = PersonajesSchema()
personajes_schema = PersonajesSchema(many=True)
