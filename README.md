# api_rest_dbz
API REST de Personajes de Dragon Ball Z


Este proyecto es una API REST desarrollada en Flask para manejar el CRUD de personajes de Dragon Ball Z. La API permite registrar usuarios, autenticarse y obtener un token JWT para realizar peticiones, además de consultar, crear, actualizar y eliminar personajes de la base de datos.

## Instalación:

1-Clona el repositorio de GitHub en tu computadora.

2-Abre la terminal y navega hasta la carpeta donde se encuentra el repositorio.

3-Crea un ambiente virtual para el proyecto con el siguiente comando:
python -m venv env

4-Activa el ambiente virtual con el siguiente comando:
source env/bin/activate

5-Instala las dependencias necesarias del proyecto utilizando el archivo requirements.txt con el siguiente comando:
pip install -r requirements.txt

6-Ejecuta el proyecto con el siguiente comando:
python3 app.py




## Endpoints
La API cuenta con los siguientes endpoints:

POST /auth/registrar: permite registrar un usuario nuevo en la aplicación.  
POST /auth/login: permite autenticarse y obtener un token JWT para realizar peticiones.  
GET /api/personajes: devuelve una lista de todos los personajes almacenados en la base de datos.  
GET /api/personaje/{id}: devuelve la información de un personaje específico identificado por su id.  
POST /api/personajes: crea un nuevo personaje en la base de datos.  
PUT /api/personajes/{id}: actualiza la información de un personaje específico identificado por su id.  
DELETE /api/personajes/{id}: elimina un personaje específico identificado por su id.

## Ejemplos de uso

Registrar un nuevo usuario  
POST /auth/register
Content-Type: application/json

{
  "username": "ejemplo",
  "clave": "contraseña"
}


Autenticarse y obtener un token JWT  
POST /auth/login
Content-Type: application/json

{
  "username": "ejemplo",
  "clave": "contraseña"
}


Consultar la lista de personajes  
GET /api/personajes
Authorization: Bearer {token_jwt}


Consultar un personaje específico  
GET /api/personajes/1
Authorization: Bearer {token_jwt}


Crear un nuevo personaje  
POST /characters
Content-Type: multipart/form-data
Authorization: Bearer {token_jwt}

{
  "name": "Goku",
  "raza": "Saiyan",
  "poderpelea": 10000,
  "planeta": "Tierra",
  "descripcion": "Personaje muy fuerte",
  "imagen": imagen.png,
  "edad": 10,
  "altura": 180,
  "peso": 100,
  "habilidades": "super kaioken"
}


Actualizar un personaje existente  
PUT /api/personajes/1
Content-Type: multipart/form-data
Authorization: Bearer {token_jwt}

{
  "poderpelea": 12000,
  "imagen": goku.png
}

Eliminar un personaje existente  
DELETE /api/personaje/1
Authorization: Bearer {token_jwt}



