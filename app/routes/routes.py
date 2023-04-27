from flask import Blueprint, request, jsonify, make_response, url_for
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask import current_app
from werkzeug.utils import secure_filename

from models.models import Usuario, Personaje
from schema.schemas import personaje_schema, personajes_schema
from database import db
from utils import allowed_file

import bcrypt
from http import HTTPStatus
import os


blue_print = Blueprint("app", __name__)


@blue_print.route('/', methods=['GET'])
def index():
    return jsonify(respuesta="REST API CON FLASK")


@blue_print.route('/auth/registrar', methods=['POST'])
def registrar_usuario():
    try:
        # Obtener los datos de usuario y contraseña del JSON de la solicitud
        usuario = request.get_json()['usuario']
        clave = request.get_json()['clave']

        # Validar que ambos campos estén presentes en la solicitud
        if not usuario or not clave:

            # Si los campos son inválidos, registrar una advertencia y la dirección IP del solicitante
            current_app.logger.warning(
                f'Se intentó registrar un usuario con campos inválidos,Dirección IP: {request.remote_addr}')

            # Devolver una respuesta con un código de estado HTTP 400 Bad Request
            return make_response(jsonify({'respuesta': 'Campos invalidos'}), HTTPStatus.BAD_REQUEST)

        # Verificar si el usuario ya existe en la base de datos
        existe_usuario = Usuario.query.filter_by(usuario=usuario).first()

        if existe_usuario:

            # Si el usuario ya existe, registrar una advertencia y la dirección IP del solicitante
            current_app.logger.info(
                f'Se intentó registrar un usuario que ya existe, Dirección IP: {request.remote_addr}')

            # Devolver una respuesta con un código de estado HTTP 200 Bad Request
            return make_response(jsonify({'respuesta': 'No se pudo completar la operación'}), HTTPStatus.OK)

        # Encriptar la contraseña y crear un nuevo objeto Usuario en la base de datos
        clave_encriptada = bcrypt.hashpw(
            clave.encode('utf-8'), bcrypt.gensalt())
        nuevo_usuario = Usuario(usuario, clave_encriptada)
        db.session.add(nuevo_usuario)
        db.session.commit()

        # Si todo ha ido bien, registrar un mensaje de información y la dirección IP del solicitante
        current_app.logger.info(
            f"Usuario '{usuario}' registrado exitosamente , Dirección IP: {request.remote_addr}")

        # Devolver una respuesta con un código de estado HTTP 201 Created
        return make_response(jsonify({'respuesta': 'Usuario Creado Exitosamente'}), HTTPStatus.CREATED)
    except Exception:
        # Si se produce una excepción, deshacer cualquier cambio pendiente en la base de datos y registrar un mensaje de error y la dirección IP del solicitante
        db.session.rollback()
        current_app.logger.error(
            f'Ocurrió un error en la petición de registro de usuario, Dirección IP: {request.remote_addr}', exc_info=True)

        # Devolver una respuesta con un código de estado HTTP 500 Internal Server Error
        return make_response(jsonify({'respuesta': 'Error en la peticion'}), HTTPStatus.INTERNAL_SERVER_ERROR)


@blue_print.route('/auth/login', methods=['POST'])
def iniciar_sesion():
    try:
        usuario = request.get_json()['usuario']
        clave = request.get_json()['clave']

        if not usuario or not clave:
            # Si los campos son inválidos, registrar una advertencia y la dirección IP del solicitante
            current_app.logger.warning(
                f'Se intentó registrar un usuario con campos inválidos: Dirección IP: {request.remote_addr}')

            return make_response(jsonify({'respuesta': 'Campos invalidos'}), HTTPStatus.BAD_REQUEST)

        existe_usuario = Usuario.query.filter_by(usuario=usuario).first()

        if not existe_usuario:
            # Si el usuario no existe, registrar una advertencia y la dirección IP del solicitante
            current_app.logger.warning(
                f'Se intentó iniciar sesion con un usuario que no existe: {usuario}. Dirección IP: {request.remote_addr}')

            # Devolver una respuesta con un código de estado HTTP 200 Bad Request
            # Mandamos este mensaje para que el usuario no sepa si existe o no algun usuario con ese nombre
            return make_response(jsonify({'respuesta': 'No se pudo completar la operación'}), HTTPStatus.OK)

        clave_valida = bcrypt.checkpw(
            clave.encode('utf-8'), existe_usuario.clave.encode("utf-8"))

        if clave_valida:
            access_token = create_access_token(identity=usuario)

            current_app.logger.info(
                f'El usuario {usuario} ha iniciado sesion, Dirección IP: {request.remote_addr}')

            return make_response(jsonify({'access_token': access_token}), HTTPStatus.OK)
        current_app.logger.warning(
            f'Se intentó iniciar sesion con un usuario {usuario} o clave {clave} incorrecto. Dirección IP: {request.remote_addr}')
        return make_response(jsonify({'respuesta': 'Clave o Usuario Incorrecto'}), HTTPStatus.NOT_FOUND)
    except Exception:

        current_app.logger.error(
            f'Ocurrió un error en la petición de inicio de sesion, Dirección IP: {request.remote_addr}', exc_info=True)
        return make_response(jsonify({'respuesta': 'Error en la peticion'}), HTTPStatus.INTERNAL_SERVER_ERROR)


# PROTEGER RUTAS CON JWT_REQUIRED

# Crear Personaje
@blue_print.route('/api/personajes', methods=['POST'])
@jwt_required()
def crear_personaje():
    try:

        # Agregar registro de solicitud entrante
        current_app.logger.info('Solicitud entrante: %s', request.form)

        # Obtenemos los datos enviados por el usuario
        nombre = request.form['nombre']
        raza = request.form['raza']
        planeta = request.form['planeta']
        descripcion = request.form['descripcion']
        imagen = request.files['imagen']
        edad = request.form['edad']
        altura = request.form['altura']
        peso = request.form['peso']
        poderpelea = request.form['poderpelea']
        habilidades = request.form['habilidades']

        # toma el nombre del archivo de imagen, lo procesa para hacerlo seguro y luego lo codifica en formato utf-8
        imagen_filename = secure_filename(imagen.filename).encode('utf-8')

        # Crear un nuevo objeto Personaje con los datos recibidos y la imagen procesada
        nuevo_personaje = Personaje(nombre, raza, planeta, descripcion,
                                    imagen_filename, edad, altura, peso, poderpelea, habilidades)

        # Agregamos el objeto a la db y guardamos cambios
        db.session.add(nuevo_personaje)
        db.session.commit()

        # Verificar si la transacción fue exitosa
        if nuevo_personaje.id is not None:
            # Guardar la imagen en el sistema de archivos
            imagen.save(os.path.join(
                current_app.config['UPLOAD_FOLDER'], imagen.filename))

            # Agregar registro de respuesta saliente
            current_app.logger.info(
                f'Respuesta saliente: Personaje Creado Exitosamente, Dirección IP: {request.remote_addr}')

            return make_response(jsonify({'respuesta': 'Personaje Creado Exitosamente'}), HTTPStatus.CREATED)

    except Exception as e:
        # Agregar registro de error
        current_app.logger.error(
            f'Error en la peticion: {e}, Dirección IP: {request.remote_addr}')

        return make_response(jsonify({'respuesta': 'Error en la peticion'}), HTTPStatus.INTERNAL_SERVER_ERROR)


# Obtener Personaje
@blue_print.route('/api/personajes', methods=['GET'])
@jwt_required()
def obtener_personajes():
    try:
        # Obtener todos los personajes
        personajes = Personaje.query.all()
        # Convertir los personajes en una respuesta JSON
        respuesta = personajes_schema.dump(personajes)
        # Registrar la información de acceso exitoso a la ruta en el registro
        current_app.logger.info(
            f'Acceso exitoso a la ruta /api/personajes, Dirección IP: {request.remote_addr}')

        for personaje in respuesta:
            personaje['imagen'] = url_for(
                'static', filename=f"images/{personaje['imagen']}", _external=True)

        # Devolver la respuesta con un código de estado HTTP 200 OK
        return respuesta, HTTPStatus.OK

    except Exception as e:
        # En caso de que ocurra un error, registrar el error en el registro con la información de la excepción
        current_app.logger.error(
            f'Error en la petición de la ruta /api/personajes: {str(e)}, Dirección IP: {request.remote_addr}', exc_info=True)

        # Devolver una respuesta con un código de estado HTTP 500 Internal Server Error
        return make_response(jsonify({'respuesta': 'Error en la petición'}), HTTPStatus.INTERNAL_SERVER_ERROR)


# Obtener Personaje por id
@blue_print.route('/api/personaje/<int:id>', methods=['GET'])
@jwt_required()
def obtener_personaje_id(id):
    try:
        # Obtener personaje por id
        personaje = Personaje.query.get(id)

        if personaje is None:
            # Registramos la información de personaje no encontrado
            current_app.logger.warning(
                f'No se encontró el personaje solicitado con id: {id}, Dirección IP: {request.remote_addr}')
            # Devolver la respuesta con código de estado HTTP 404
            return make_response(jsonify({'respuesta': 'No se encontró el personaje solicitado'}), HTTPStatus.NOT_FOUND)

        current_app.logger.info(
            f'Se encontró el personaje solicitado con id: {id}, Dirección IP: {request.remote_addr}')

        # Obtener la ruta completa de la imagen
        ruta_imagen = url_for("static", filename='images/' +
                              personaje.imagen.decode("utf-8"), _external=True)

        # Modificar el objeto JSON para incluir la URL completa de la imagen
        response_data = personaje_schema.dump(personaje)
        response_data['imagen'] = ruta_imagen

        return jsonify(response_data), HTTPStatus.OK
    except Exception as e:
        current_app.logger.error(
            f'Error en la petición obtener personaje ruta /api/personajes/<int:id>: {str(e)}, Dirección IP: {request.remote_addr}', exc_info=True)
        return make_response(jsonify({'respuesta': 'Error en la peticion'}), HTTPStatus.INTERNAL_SERVER_ERROR)


# Actualizar Personaje
@blue_print.route('/api/personajes/<int:id>', methods=['PUT'])
@jwt_required()
def actualizar_personaje(id):
    try:

        personaje = Personaje.query.get(id)
        if personaje is None:
            current_app.logger.warning(
                f'No se encontró el personaje solicitado para actualizar con el id: {id}, Dirección IP: {request.remote_addr}')
            return make_response(jsonify({'respuesta': 'No se encontró el personaje solicitado'}), HTTPStatus.NOT_FOUND)

        campos = ['nombre', 'raza', 'planeta', 'descripcion', 'imagen',
                  'edad', 'altura', 'peso', 'poderpelea', 'habilidades']

        for campo in campos:
            if campo == 'imagen' and campo in request.files:
                # Removemos la imagen antigua antes de guardar la imagen nueva
                imagen_eliminar = personaje.imagen.decode("utf-8")
                ruta_imagen_eliminar = os.path.join(
                    current_app.config['UPLOAD_FOLDER'], imagen_eliminar)

                if os.path.exists(ruta_imagen_eliminar):
                    os.remove(ruta_imagen_eliminar)
                    current_app.logger.info(
                        f"El archivo {ruta_imagen_eliminar} fue eliminado exitosamente.")
                else:
                    current_app.logger.warning(
                        f"El archivo {ruta_imagen_eliminar} no existe.")

                # Guardar la imagen en el servidor con un nombre seguro
                imagen = request.files['imagen']
                filename = secure_filename(imagen.filename)

                ruta_imagen = os.path.join(
                    current_app.config['UPLOAD_FOLDER'], filename)

                # Guardamos la nueva imagen
                imagen.save(ruta_imagen)
                # Actualizar el atributo imagen del objeto personaje con la ruta de la imagen guardada en el servidor
                setattr(personaje, campo, str(filename).encode("utf-8"))
            elif campo in request.form:
                setattr(personaje, campo, request.form[campo])

        db.session.commit()
        current_app.logger.info(
            f'Personaje Actualizado Exitosamente con el id:{id}, Dirección IP: {request.remote_addr}')
        return make_response(jsonify({'respuesta': 'Personaje Actualizado Exitosamente'}), HTTPStatus.CREATED)
    except Exception as e:
        current_app.logger.error(
            f'Error en la solicitud para actualizar el personaje: {str(e)}, Dirección IP: {request.remote_addr}')
        return make_response(jsonify({'respuesta': 'Faltan campos obligatorios en la solicitud'}), HTTPStatus.BAD_REQUEST)


# Eliminar Personaje por id
@blue_print.route('/api/personajes/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_personaje_id(id):
    try:
        personaje = Personaje.query.get_or_404(id)
        db.session.delete(personaje)
        db.session.commit()

        current_app.logger.info(
            f'Personaje con ID {id} eliminado exitosamente, Dirección IP:{request.remote_addr}')
        return make_response(jsonify({'respuesta': 'Personaje Eliminado Exitosamente'}), HTTPStatus.OK)

    except Exception as e:
        current_app.logger.error(
            f'Error al eliminar el personaje con ID {id}: {str(e)}, Dirección IP:{request.remote_addr}', exc_info=True)
        return make_response(jsonify({'respuesta': 'Error al eliminar el personaje'}), HTTPStatus.INTERNAL_SERVER_ERROR)
