from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from models.models import Usuario, Personaje
from schema.schemas import personaje_schema, personajes_schema
from database import db
import bcrypt
from http import HTTPStatus


blue_print = Blueprint("app", __name__)


@blue_print.route('/', methods=['GET'])
def index():
    return jsonify(respuesta="REST API CON FLASK")


@blue_print.route('/auth/registrar', methods=['POST'])
def registrar_usuario():
    try:
        usuario = request.get_json()['usuario']
        clave = request.get_json()['clave']

        if not usuario or not clave:
            return make_response(jsonify({'respuesta': 'Campos invalidos'}), HTTPStatus.BAD_REQUEST)

        existe_usuario = Usuario.query.filter_by(usuario=usuario).first()

        if existe_usuario:
            return make_response(jsonify({'respuesta': 'Usuario ya existe'}), HTTPStatus.BAD_REQUEST)

        clave_encriptada = bcrypt.hashpw(
            clave.encode('utf-8'), bcrypt.gensalt())
        nuevo_usuario = Usuario(usuario, clave_encriptada)
        db.session.add(nuevo_usuario)
        db.session.commit()

        return make_response(jsonify({'respuesta': 'Usuario Creado Exitosamente'}), HTTPStatus.CREATED)
    except Exception:
        db.session.rollback()  # deshacer cualquier cambio pendiente en la base de datos
        return make_response(jsonify({'respuesta': 'Error en la peticion'}), HTTPStatus.INTERNAL_SERVER_ERROR)


@blue_print.route('/auth/login', methods=['POST'])
def iniciar_sesion():
    try:
        usuario = request.get_json()['usuario']
        clave = request.get_json()['clave']

        if not usuario or not clave:
            return make_response(jsonify({'respuesta': 'Campos invalidos'}), HTTPStatus.BAD_REQUEST)

        existe_usuario = Usuario.query.filter_by(usuario=usuario).first()

        if not existe_usuario:
            return make_response(jsonify({'respuesta': 'Usuario no encontrado'}), HTTPStatus.NOT_FOUND)

        clave_valida = bcrypt.checkpw(
            clave.encode('utf-8'), existe_usuario.clave.encode("utf-8"))

        if clave_valida:
            access_token = create_access_token(identity=usuario)
            return make_response(jsonify({'access_token': access_token}), HTTPStatus.OK)

        return make_response(jsonify({'respuesta': 'Clave o Usuario Incorrecto'}), HTTPStatus.NOT_FOUND)
    except Exception:
        return make_response(jsonify({'respuesta': 'Error en la peticion'}), HTTPStatus.INTERNAL_SERVER_ERROR)


# PROTEGER RUTAS CON JWT_REQUIRED

# Crear Personaje
@blue_print.route('/api/personajes', methods=['POST'])
@jwt_required()
def crear_personaje():
    try:
        nombre = request.json['nombre']
        raza = request.json['raza']
        planeta = request.json['planeta']
        descripcion = request.json['descripcion']
        imagen = request.json['imagen']
        edad = request.json['edad']
        altura = request.json['altura']
        peso = request.json['peso']
        poderpelea = request.json['poderpelea']
        habilidades = request.json['habilidades']

        nuevo_personaje = Personaje(
            nombre, raza, planeta, descripcion, imagen, edad, altura, peso, poderpelea, habilidades)

        db.session.add(nuevo_personaje)
        db.session.commit()

        return make_response(jsonify({'respuesta': 'Personaje Creado Exitosamente'}), HTTPStatus.CREATED)
    except Exception:
        return make_response(jsonify({'respuesta': 'Error en la peticion'}), HTTPStatus.INTERNAL_SERVER_ERROR)


# Obtener Personaje
@blue_print.route('/api/personajes', methods=['GET'])
@jwt_required()
def obtener_personajes():
    personajes = Personaje.query.all()
    respuesta = personajes_schema.dump(personajes)
    return respuesta, HTTPStatus.OK


# Obtener Personaje por id
@blue_print.route('/api/personajes/<int:id>', methods=['GET'])
@jwt_required()
def obtener_personaje_id(id):
    try:
        personaje = Personaje.query.get(id)
        if personaje is None:
            return make_response(jsonify({'respuesta': 'No se encontró el personaje solicitado'}), HTTPStatus.NOT_FOUND)
        return personaje_schema.jsonify(personaje), HTTPStatus.OK
    except Exception:
        return make_response(jsonify({'respuesta': 'Error en la peticion'}), HTTPStatus.INTERNAL_SERVER_ERROR)


# Actualizar Personaje
@blue_print.route('/api/personajes/<int:id>', methods=['PUT'])
@jwt_required()
def actualizar_personaje(id):
    try:

        personaje = Personaje.query.get(id)
        if personaje is None:
            return make_response(jsonify({'respuesta': 'No se encontró el personaje solicitado'}), HTTPStatus.NOT_FOUND)

        campos = ['nombre', 'raza', 'planeta', 'descripcion', 'imagen',
                  'edad', 'altura', 'peso', 'poderpelea', 'habilidades']

        for campo in campos:
            if campo in request.json:
                setattr(personaje, campo, request.json[campo])

        db.session.commit()

        return make_response(jsonify({'respuesta': 'Personaje Actualizado Exitosamente'}), HTTPStatus.CREATED)
    except Exception:
        return make_response(jsonify({'respuesta': 'Faltan campos obligatorios en la solicitud'}), HTTPStatus.BAD_REQUEST)


# Eliminar Personaje por id
@blue_print.route('/api/personajes/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_personaje_id(id):
    personaje = Personaje.query.get_or_404(id)
    db.session.delete(personaje)
    db.session.commit()
    return make_response(jsonify({'respuesta': 'Personaje Eliminado Exitosamente'}), HTTPStatus.OK)


'''
# CODIGO ORIGINAL
@blue_print.route('/auth/registrar', methods=['POST'])
def registrar_usuario():
    try:
        # obtener usuario
        usuario = request.json.get("usuario")
        # obtener clave
        clave = request.json.get("clave")

        if not usuario or not clave:
            return jsonify(respuesta="Campos invalidos"), 400

        # consultar db
        existe_usuario = Usuario.query.filter_by(usuario=usuario).first()

        if existe_usuario:
            return jsonify(respuesta="Usuario ya existe"), 400

        # encriptar clave de usuario
        clave_encriptada = bcrypt.hashpw(
            clave.encode("utf-8"), bcrypt.gensalt())

        # creamos modelo para guardar en la db
        nuevo_usuario = Usuario(usuario, clave_encriptada)
        db.session.add(nuevo_usuario)
        db.session.commit()

        return jsonify(respuesta="Usuario Creado Exitosamente"), 201

    except Exception:
        return jsonify(respuesta="Error en la peticion"), 500


@blue_print.route('/auth/login', methods=['POST'])
def iniciar_sesion():
    try:
        # obtener usuario
        usuario = request.json.get("usuario")
        # obtener clave
        clave = request.json.get("clave")

        if not usuario or not clave:
            return jsonify(respuesta="Campos invalidos"), 400

        # consultar db
        existe_usuario = Usuario.query.filter_by(usuario=usuario).first()

        if not existe_usuario:
            return jsonify(respuesta="Usuario no encontrado"), 404

        clave_valida = bcrypt.checkpw(clave.encode(
            "utf-8"), existe_usuario.clave.encode("utf-8"))

        #validar que la clave sea igual
        if clave_valida:
            access_token = create_access_token(identity=usuario)
            return jsonify(access_token=access_token), 200
        return jsonify(respuesta="Clave o Usuario Incorrecto"), 404
    except Exception:
        return jsonify(respuesta="Error en la peticion"), 500
'''
