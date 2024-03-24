from flask import Flask, request, jsonify
import json
import pymysql

app = Flask(__name__)

# Configuración de la conexión a la base de datos MySQL


# Funciones auxiliares
def conectar_db():
    return pymysql.connect(host='localhost', user='root', password='efrainfox1212', database='emprezaxyz')


def validar_credenciales(usuario, contraseña):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Usuario WHERE id_usuario = %s AND contraseña = %s', (usuario, contraseña))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None


def asignar_perfil_a_usuario(id_usuario):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO perfilesdeusuarios (id_usuario, id_perfil) VALUES (%s, %s)', (id_usuario, 1))  # Asignando id_perfil = 1 por defecto
    conn.commit()
    conn.close()


@app.route('/login', methods=['POST'])
def login():
    datos_login = request.json
    usuario = datos_login.get('id_usuario')
    contraseña = datos_login.get('contraseña')
    if usuario is None or contraseña is None:
        return jsonify({"error": "Usuario y contraseña son requeridos"}), 400

    if validar_credenciales(usuario, contraseña):
        return jsonify({"mensaje": "Inicio de sesión exitoso"}), 200
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401


# Obtener todos los usuarios
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Usuario')
    usuarios = cursor.fetchall()
    conn.close()
    return jsonify(usuarios)


# Crear un nuevo usuario
@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    nuevo_usuario = request.json
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO Usuario (id_usuario, nombre, apellido, estado, contraseña, cargo, salario, fecha_ingreso) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
        (nuevo_usuario['id_usuario'], nuevo_usuario['nombre'], nuevo_usuario['apellido'], nuevo_usuario['estado'],
         nuevo_usuario['contraseña'], nuevo_usuario['cargo'], nuevo_usuario['salario'], nuevo_usuario['fecha_ingreso']))
    conn.commit()
    asignar_perfil_a_usuario(nuevo_usuario['id_usuario'])  # Asignar perfil al nuevo usuario
    nuevo_usuario['id_usuario'] = cursor.lastrowid
    conn.close()
    return jsonify(nuevo_usuario), 201


# Obtener todos los perfiles
@app.route('/perfiles', methods=['GET'])
def obtener_perfiles():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Perfil')
    perfiles = cursor.fetchall()
    conn.close()
    return jsonify(perfiles)


# Crear un nuevo perfil
@app.route('/perfiles', methods=['POST'])
def crear_perfil():
    nuevo_perfil = request.json
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Perfil (id_perfil, nombre, fecha_vigencia, descripcion) VALUES (%s, %s, %s, %s)',
                   (nuevo_perfil['id_perfil'], nuevo_perfil['nombre'], nuevo_perfil['fecha_vigencia'],
                    nuevo_perfil['descripcion']))
    conn.commit()
    nuevo_perfil['id_perfil'] = cursor.lastrowid
    conn.close()
    return jsonify(nuevo_perfil), 201


# Obtener todos los registros de fidelización
@app.route('/fidelizacion', methods=['GET'])
def obtener_fidelizacion():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Fidelizacion')
    fidelizacion = cursor.fetchall()
    conn.close()
    return jsonify(fidelizacion)


# Crear un nuevo registro de fidelización
@app.route('/fidelizacion', methods=['POST'])
def crear_fidelizacion():
    nueva_fidelizacion = request.json
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO Fidelizacion (id_fidelizacion, id_usuario, puntos, fecha_actividad) VALUES (%s, %s, %s, %s)',
        (nueva_fidelizacion['id_fidelizacion'], nueva_fidelizacion['id_usuario'], nueva_fidelizacion['puntos'],
         nueva_fidelizacion['fecha_actividad']))
    conn.commit()
    nueva_fidelizacion['id_fidelizacion'] = cursor.lastrowid
    conn.close()
    return jsonify(nueva_fidelizacion), 201


# Obtener datos de la vista de fidelización
@app.route('/fidelizacion_vista', methods=['GET'])
def obtener_fidelizacion_vista():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Vista_Fidelizacion')
    fidelizacion_vista = cursor.fetchall()
    conn.close()
    return jsonify(fidelizacion_vista)


if __name__ == '__main__':
    app.run(debug=True)
