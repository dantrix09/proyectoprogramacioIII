import sqlite3
from datetime import datetime
conn = sqlite3.connect('basededatosclinicas.db')
cursor = conn.cursor()
import customtkinter as ctk
from tkinter import ttk, messagebox
import random as r
import time as y
from datetime import datetime

## creacion de tablas y relaciones de la base de datos
def crear_tablas():
    query = """
    PRAGMA foreign_keys = ON;

    CREATE TABLE IF NOT EXISTS clinicas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        ubicacion_base TEXT NOT NULL,
        latitud REAL,
        longitud REAL,
        estado TEXT DEFAULT 'activa',  -- SQLite no soporta ENUM
        fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        nombre_completo TEXT,
        correo TEXT UNIQUE,
        rol TEXT NOT NULL, 
        activo INTEGER DEFAULT 1,
        fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS equipos_medicos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL,
        modelo TEXT,
        numero_serie TEXT NOT NULL UNIQUE,
        clinica_id INTEGER,
        estado TEXT DEFAULT 'disponible',
        ultimo_mantenimiento DATE,
        capacidad_litros REAL,
        fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (clinica_id) REFERENCES clinicas(id)
    );

    CREATE TABLE IF NOT EXISTS vacunas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lote TEXT NOT NULL UNIQUE,
        tipo TEXT NOT NULL,
        cantidad INTEGER NOT NULL,
        temperatura_minima REAL NOT NULL,
        temperatura_maxima REAL NOT NULL,
        fecha_vencimiento DATE NOT NULL,
        clinica_id INTEGER,
        estado TEXT DEFAULT 'disponible',
        fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (clinica_id) REFERENCES clinicas(id)
    );

    CREATE TABLE IF NOT EXISTS rutas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        clinica_id INTEGER NOT NULL,
        comunidad TEXT NOT NULL,
        fecha DATE NOT NULL,
        distancia_km REAL,
        estado TEXT DEFAULT 'planificada',
        fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (clinica_id) REFERENCES clinicas(id)
    );

    CREATE TABLE IF NOT EXISTS registros_temperatura (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        clinica_id INTEGER NOT NULL,
        equipo_id INTEGER NOT NULL,
        temperatura REAL NOT NULL,
        latitud REAL,
        longitud REAL,
        fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
        fuente TEXT,
        FOREIGN KEY (clinica_id) REFERENCES clinicas(id),
        FOREIGN KEY (equipo_id) REFERENCES equipos_medicos(id)
    );

    CREATE TABLE IF NOT EXISTS aplicaciones_vacuna (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        clinica_id INTEGER NOT NULL,
        vacuna_id INTEGER NOT NULL,
        lote TEXT NOT NULL,
        cantidad INTEGER NOT NULL,
        comunidad TEXT NOT NULL,
        paciente_identificacion TEXT,
        responsable_id INTEGER,
        evidencia_firma TEXT,
        fecha_aplicacion DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (clinica_id) REFERENCES clinicas(id),
        FOREIGN KEY (vacuna_id) REFERENCES vacunas(id),
        FOREIGN KEY (responsable_id) REFERENCES usuarios(id)
    );

    CREATE TABLE IF NOT EXISTS alertas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo TEXT NOT NULL,
        mensaje TEXT NOT NULL,
        clinica_id INTEGER,
        equipo_id INTEGER,
        vacuna_id INTEGER,
        severidad TEXT DEFAULT 'media',
        leida INTEGER DEFAULT 0,
        fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (clinica_id) REFERENCES clinicas(id),
        FOREIGN KEY (equipo_id) REFERENCES equipos_medicos(id),
        FOREIGN KEY (vacuna_id) REFERENCES vacunas(id)
    );

    CREATE TABLE IF NOT EXISTS mantenimientos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        equipo_id INTEGER NOT NULL,
        tipo_mantenimiento TEXT NOT NULL,
        descripcion TEXT,
        fecha_programada DATE,
        fecha_inicio DATETIME,
        fecha_fin DATETIME,
        estado TEXT DEFAULT 'programado',
        encargado_id INTEGER,
        reporte TEXT,
        fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (equipo_id) REFERENCES equipos_medicos(id),
        FOREIGN KEY (encargado_id) REFERENCES usuarios(id)
    );

    CREATE TABLE IF NOT EXISTS auditoria (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tabla_afectada TEXT NOT NULL,
        registro_id INTEGER,
        accion TEXT NOT NULL,
        usuario_id INTEGER,
        valores_anteriores TEXT,
        valores_nuevos TEXT,
        fecha_cambio DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    );
    """
    cursor.executescript(query)
    conn.commit()
## ejecutar la creacion de tablas
crear_tablas()

def insertar_datos_clnica(nombre, ubicacion_base, latitud, longitud):
    query = """
    INSERT INTO clinicas (nombre, ubicacion_base, latitud, longitud)
    VALUES (?, ?, ?, ?);
    """
    cursor.execute(query, (nombre, ubicacion_base, latitud, longitud))
    conn.commit()
    return cursor.lastrowid
def insertar_datos_usuario(username, nombre_completo, correo, rol):
    query = """
    INSERT INTO usuarios (username, nombre_completo, correo, rol)
    VALUES (?, ?, ?, ?);
    """
    cursor.execute(query, (username, nombre_completo, correo, rol))
    conn.commit()
    return cursor.lastrowid
def insertar_datos_equipo_medico(tipo, modelo, numero_serie, clinica_id, capacidad_litros):
    query = """
    INSERT INTO equipos_medicos (tipo, modelo, numero_serie, clinica_id, capacidad_litros)
    VALUES (?, ?, ?, ?, ?);
    """
    cursor.execute(query, (tipo, modelo, numero_serie, clinica_id, capacidad_litros))
    conn.commit()
    return cursor.lastrowid
def insertar_datos_vacuna(lote, tipo, cantidad, temperatura_minima, temperatura_maxima, fecha_vencimiento, clinica_id):
    query = """
    INSERT INTO vacunas (lote, tipo, cantidad, temperatura_minima, temperatura_maxima, fecha_vencimiento, clinica_id)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    """
    cursor.execute(query, (lote, tipo, cantidad, temperatura_minima, temperatura_maxima, fecha_vencimiento, clinica_id))
    conn.commit()
    return cursor.lastrowid
def insertar_datos_ruta(clinica_id, comunidad, fecha, distancia_km):    
    query = """
    INSERT INTO rutas (clinica_id, comunidad, fecha, distancia_km)
    VALUES (?, ?, ?, ?);
    """
    cursor.execute(query, (clinica_id, comunidad, fecha, distancia_km))
    conn.commit()
    return cursor.lastrowid
def insertar_datos_registro_temperatura(clinica_id, equipo_id, temperatura, latitud, longitud, fuente):
    query = """
    INSERT INTO registros_temperatura (clinica_id, equipo_id, temperatura, latitud, longitud, fuente)
    VALUES (?, ?, ?, ?, ?, ?);
    """
    cursor.execute(query, (clinica_id, equipo_id, temperatura, latitud, longitud, fuente))
    conn.commit()
    return cursor.lastrowid
def insertar_datos_aplicacion_vacuna(clinica_id, vacuna_id, lote, cantidad, comunidad, paciente_identificacion, responsable_id, evidencia_firma):
    query = """
    INSERT INTO aplicaciones_vacuna (clinica_id, vacuna_id, lote, cantidad, comunidad, paciente_identificacion, responsable_id, evidencia_firma)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """
    cursor.execute(query, (clinica_id, vacuna_id, lote, cantidad, comunidad, paciente_identificacion, responsable_id, evidencia_firma))
    conn.commit()
    return cursor.lastrowid
def insertar_datos_alerta(tipo, mensaje, clinica_id, equipo_id, vacuna_id, severidad):
    query = """
    INSERT INTO alertas (tipo, mensaje, clinica_id, equipo_id, vacuna_id, severidad)
    VALUES (?, ?, ?, ?, ?, ?);
    """
    cursor.execute(query, (tipo, mensaje, clinica_id, equipo_id, vacuna_id, severidad))
    conn.commit()
    return cursor.lastrowid
def insertar_datos_mantenimiento(equipo_id, tipo_mantenimiento, descripcion, fecha_programada, encargado_id):
    query = """
    INSERT INTO mantenimientos (equipo_id, tipo_mantenimiento, descripcion, fecha_programada, encargado_id)
    VALUES (?, ?, ?, ?, ?);
    """
    cursor.execute(query, (equipo_id, tipo_mantenimiento, descripcion, fecha_programada, encargado_id))
    conn.commit()
    return cursor.lastrowid 
def insertar_datos_auditoria(tabla_afectada, registro_id, accion, usuario_id, valores_anteriores, valores_nuevos):    
    query = """
    INSERT INTO auditoria (tabla_afectada, registro_id, accion, usuario_id, valores_anteriores, valores_nuevos)
    VALUES (?, ?, ?, ?, ?, ?);
    """
    cursor.execute(query, (tabla_afectada, registro_id, accion, usuario_id, valores_anteriores, valores_nuevos))
    conn.commit()
    return cursor.lastrowid

def nombre_clinica():
    nombre = input("Ingrese el nombre de la clinica: ")
    if nombre.strip() == "":
        print("El nombre no puede estar vacio. Intente de nuevo.")
        return nombre_clinica()
    return nombre
def ubicacion_base():
    ubicacion = input("Ingrese la ubicacion base de la clinica: ")
    if ubicacion.strip() == "":
        print("La ubicacion no puede estar vacia. Intente de nuevo.")
        return ubicacion_base()
    return ubicacion
def latitud():
    try:
        lat = float(input("Ingrese la latitud de la clinica: "))
        return lat
    except ValueError:
        print("Latitud invalida. Intente de nuevo.")
        return latitud()
def longitud():  
    try:
        lon = float(input("Ingrese la longitud de la clinica: "))
        if lon == 0:
            print("La longitud no puede ser cero. Intente de nuevo.")
            return longitud()   
        return lon
    except ValueError:
        print("Longitud invalida. Intente de nuevo.")
        return longitud()
def registrar_clinica():    
    nombre = nombre_clinica()
    ubicacion = ubicacion_base()
    lat = latitud()
    lon = longitud()
    clinica_id = insertar_datos_clnica(nombre, ubicacion, lat, lon)
    print(f"Clinica registrada con ID: {clinica_id}")   
def usuario_username():
    username = input("Ingrese el nombre de usuario: ")
    if username.strip() == "":
        print("El nombre de usuario no puede estar vacio. Intente de nuevo.")
        return usuario_username()
    return username 

def usuario_nombre_completo():
    nombre_completo = input("Ingrese el nombre completo del usuario: ")
    if nombre_completo.strip() == "":
        print("El nombre completo no puede estar vacio. Intente de nuevo.")
        return usuario_nombre_completo()
    return nombre_completo
def usuario_correo():
    correo = input("Ingrese el correo del usuario: ")
    if correo.strip() == "":
        print("El correo no puede estar vacio. Intente de nuevo.")
        return usuario_correo()
    return correo
def usuario_rol():
    while True:
        try:    
            rol = input("Ingrese el rol del usuario (admin, medico, tecnico): ")
            if rol.strip() == "":
                print("El rol no puede estar vacio. Intente de nuevo.")
            elif rol not in ['admin', 'medico', 'tecnico']:
                print("Rol invalido. Intente de nuevo.")
            else:
                return rol
        except ValueError:
            print("Entrada invalida. Intente de nuevo.")    
def registrar_usuario():    
    username = usuario_username()
    nombre_completo = usuario_nombre_completo()
    correo = usuario_correo()
    rol = usuario_rol()
    usuario_id = insertar_datos_usuario(username, nombre_completo, correo, rol)
    print(f"Usuario registrado con ID: {usuario_id}")
    
def tipo_equipo():
    tipo = input("Ingrese el tipo de equipo medico: ")
    if tipo.strip() == "":
        print("El tipo de equipo no puede estar vacio. Intente de nuevo.")
        return tipo_equipo()
    return tipo 
def modelo_equipo():
    modelo = input("Ingrese el modelo del equipo medico: ")
    if modelo.strip() == "":
        print("El modelo no puede estar vacio. Intente de nuevo.")
        return modelo_equipo()
    return modelo
def numero_serie_equipo():
    numero_serie = input("Ingrese el numero de serie del equipo medico: ")
    if numero_serie.strip() == "":
        print("El numero de serie no puede estar vacio. Intente de nuevo.")
        return numero_serie_equipo()
    return numero_serie
def capacidad_litros_equipo():
    litros = float(input("Ingrese la capacidad en litros del equipo medico: ")) 
    if litros <=0:
        print("La capacidad en litros debe ser mayor que cero. Intente de nuevo.")
        
    else:
        return litros
def id_clinica():
    while True:
      try:
        id_clinica = int(input('ingrese el ID de la clinica que quiera relacionar:'))
        if id_clinica <= 0:
          print("El ID debe ser un número positivo.") 
        elif cursor.execute("SELECT * FROM CLINICAS WHERE ID = ?", (id_clinica,)).fetchone() is None:
          print("No existe una clinica con ese ID. Por favor ingrese un ID válido.")
        else:
           return id_clinica
      except ValueError:
        print("Por favor ingrese un ID válido.")
def registrar_equipo_medico():    
    tipo = tipo_equipo()
    modelo = modelo_equipo()
    numero_serie = numero_serie_equipo()
    clinica_id = id_clinica()
    capacidad_litros = capacidad_litros_equipo()
    equipo_id = insertar_datos_equipo_medico(tipo, modelo, numero_serie, clinica_id, capacidad_litros)
    print(f"Equipo medico registrado con ID: {equipo_id}")
def tipo_vacuna():
    tipo = input("Ingrese el tipo de vacuna: ")
    if tipo.strip() == "":
        print("El tipo de vacuna no puede estar vacio. Intente de nuevo.")
        return tipo_vacuna()
    return tipo
def lote_vacuna():
    lote = input("Ingrese el lote de la vacuna: ")
    if lote.strip() == "":
        print("El lote no puede estar vacio. Intente de nuevo.")
        return lote_vacuna()
    return lote
def cantidad_vacuna():
    while True:
      try:
        cantidad = int(input('Ingrese la cantidad de vacunas:'))
        if cantidad <= 0:
          print("La cantidad debe ser un número positivo. Intente de nuevo.")
        else:
           return cantidad
      except ValueError:
        print("Por favor ingrese una cantidad válida.")
def temperatura_minima_vacuna():
    while True:
      try:
        temp_min = float(input('Ingrese la temperatura minima de almacenamiento de la vacuna:'))
        return temp_min
      except ValueError:
        print("Por favor ingrese una temperatura válida.")  
def temperatura_maxima_vacuna():
    while True:
      try:
        temp_max = float(input('Ingrese la temperatura maxima de almacenamiento de la vacuna:'))
        return temp_max
      except ValueError:
        print("Por favor ingrese una temperatura válida.")  
def fecha_vencimiento_vacuna():
    fecha_str = input("Ingrese la fecha de vencimiento de la vacuna (YYYY-MM-DD): ")
    try:
        fecha_vencimiento = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        return fecha_vencimiento
    except ValueError:
        print("Formato de fecha invalido. Intente de nuevo.")
        return fecha_vencimiento_vacuna()

def registrar_vacuna():   
    lote = lote_vacuna()
    tipo = tipo_vacuna()
    cantidad = cantidad_vacuna()
    temperatura_minima = temperatura_minima_vacuna()
    temperatura_maxima = temperatura_maxima_vacuna()
    fecha_vencimiento = fecha_vencimiento_vacuna()
    clinica_id = id_clinica()
    vacuna_id = insertar_datos_vacuna(lote, tipo, cantidad, temperatura_minima, temperatura_maxima, fecha_vencimiento, clinica_id)
    print(f"Vacuna registrada con ID: {vacuna_id}")

def rutas():
    ruta = input("Ingrese la comunidad de la ruta: ")
    if ruta.strip() == "":
        print("La comunidad no puede estar vacia. Intente de nuevo.")
        return rutas()
    return ruta
def fecha_ruta():
    fecha_str = input("Ingrese la fecha de la ruta (YYYY-MM-DD): ")
    try:
        fecha_ruta = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        return fecha_ruta
    except ValueError:
        print("Formato de fecha invalido. Intente de nuevo.")
        return fecha_ruta()
def distancia_km_ruta():
    while True:
      try:
        distancia = float(input('Ingrese la distancia en km de la ruta:'))
        if distancia <= 0:
          print("La distancia debe ser un número positivo. Intente de nuevo.")
        else:
           return distancia
      except ValueError:
        print("Por favor ingrese una distancia válida.")    
def registrar_ruta():  
    clinica_id = id_clinica()
    comunidad = rutas()
    fecha = fecha_ruta()
    distancia_km = distancia_km_ruta()
    ruta_id = insertar_datos_ruta(clinica_id, comunidad, fecha, distancia_km)
    print(f"Ruta registrada con ID: {ruta_id}")
def registros_temperatura():
    while True:
      try:
        temperatura = float(input('Ingrese la temperatura registrada:'))
        return temperatura
      except ValueError:
        print("Por favor ingrese una temperatura válida.")
def latitud_registro():
    try:
        lat = float(input("Ingrese la latitud del registro de temperatura: "))
        return lat
    except ValueError:
        print("Latitud invalida. Intente de nuevo.")
        return latitud_registro()
def longitud_registro():
    try:
        lon = float(input("Ingrese la longitud del registro de temperatura: "))
        if lon == 0:
            print("La longitud no puede ser cero. Intente de nuevo.")
            return longitud_registro()   
        return lon
    except ValueError:
        print("Longitud invalida. Intente de nuevo.")
        return longitud_registro()
def fuente_registro():
    fuente = input("Ingrese la fuente del registro de temperatura: ")
    if fuente.strip() == "":
        print("La fuente no puede estar vacia. Intente de nuevo.")
        return fuente_registro()
    return fuente
def registrar_registro_temperatura():  
    clinica_id = id_clinica()
    equipo_id = int(input("Ingrese el ID del equipo medico: "))
    temperatura = registros_temperatura()
    latitud = latitud_registro()
    longitud = longitud_registro()
    fuente = fuente_registro()
    registro_id = insertar_datos_registro_temperatura(clinica_id, equipo_id, temperatura, latitud, longitud, fuente)
    print(f"Registro de temperatura registrado con ID: {registro_id}")

def aplicaciones_vacuna_lote():
    lote = input("Ingrese el lote de la vacuna aplicada: ")
    if lote.strip() == "":
        print("El lote no puede estar vacio. Intente de nuevo.")
        return aplicaciones_vacuna_lote()
    return lote
def aplicaciones_vacuna_cantidad():
    while True:
      try:
        cantidad = int(input('Ingrese la cantidad de vacunas aplicadas:'))
        if cantidad <= 0:
          print("La cantidad debe ser un número positivo. Intente de nuevo.")
        else:
           return cantidad
      except ValueError:
        print("Por favor ingrese una cantidad válida.")
def aplicaciones_vacuna_paciente_identificacion():
    identificacion = input("Ingrese la identificacion del paciente: ")
    if identificacion.strip() == "":
        print("La identificacion no puede estar vacia. Intente de nuevo.")
        return aplicaciones_vacuna_paciente_identificacion()
    return identificacion
def id_comunidad_responsable():
    while True:
      try:
        id_responsable = int(input('Ingrese el ID del responsable de la aplicacion:'))
        if id_responsable <= 0:
          print("El ID debe ser un número positivo.") 
        elif cursor.execute("SELECT * FROM USUARIOS WHERE ID = ?", (id_responsable,)).fetchone() is None:
          print("No existe un usuario con ese ID. Por favor ingrese un ID válido.")
        else:
           return id_responsable
      except ValueError:
        print("Por favor ingrese un ID válido.")    
def aplicaciones_vacuna_evidencia_firma():
    while True:
        try:
            evidencia = input("Ingrese la evidencia de firma (ruta del archivo o descripcion): ")
            if evidencia.strip() == "":
                print("La evidencia no puede estar vacia. Intente de nuevo.")
            else:
                return evidencia
        except ValueError:
            print("Entrada invalida. Intente de nuevo.")
def id_vacuna():
    while True:
      try:
        id_vacuna = int(input('ingrese el ID de la vacuna aplicada:'))
        if id_vacuna <= 0:
          print("El ID debe ser un número positivo.") 
        elif cursor.execute("SELECT * FROM VACUNAS WHERE ID = ?", (id_vacuna,)).fetchone() is None:
          print("No existe una vacuna con ese ID. Por favor ingrese un ID válido.")
        else:
           return id_vacuna
      except ValueError:
        print("Por favor ingrese un ID válido.")    
def registrar_aplicacion_vacuna():  
    clinica_id = id_clinica()
    vacuna_id = id_vacuna()
    lote = aplicaciones_vacuna_lote()
    cantidad = aplicaciones_vacuna_cantidad()
    comunidad = id_comunidad_responsable()
    paciente_identificacion = aplicaciones_vacuna_paciente_identificacion()
    responsable_id = id_comunidad_responsable()
    evidencia_firma = aplicaciones_vacuna_evidencia_firma()
    aplicacion_id = insertar_datos_aplicacion_vacuna(clinica_id, vacuna_id, lote, cantidad, comunidad, paciente_identificacion, responsable_id, evidencia_firma)
    print(f"Aplicacion de vacuna registrada con ID: {aplicacion_id}")

def tipo_alerta():
    tipo = input("Ingrese el tipo de alerta: ")
    if tipo.strip() == "":
        print("El tipo de alerta no puede estar vacio. Intente de nuevo.")
        return tipo_alerta()
    return tipo 
def mensaje_alerta():
    mensaje = input("Ingrese el mensaje de la alerta: ")
    if mensaje.strip() == "":
        print("El mensaje no puede estar vacio. Intente de nuevo.")
        return mensaje_alerta()
    return mensaje
def severidad_alerta():
    while True:
        try:
            severidad = input("Ingrese la severidad de la alerta (baja, media, alta): ")
            if severidad.strip() == "":
                print("La severidad no puede estar vacia. Intente de nuevo.")
            elif severidad not in ['baja', 'media', 'alta']:
                print("Severidad invalida. Intente de nuevo.")
            else:
                return severidad    
        except ValueError:
            print("Entrada invalida. Intente de nuevo.")
def leida():
    leida = input("Ingrese si la alerta ha sido leida (0 para no, 1 para si): ")
    if leida.strip() == "":
        print("El campo no puede estar vacio. Intente de nuevo.")
    elif leida not in ['0', '1']:
        print("Valor invalido. Intente de nuevo.")
    else:
        return int(leida)
def fecha_creacion_alerta():
    fecha_str = input("Ingrese la fecha de creacion de la alerta (YYYY-MM-DD HH:MM:SS): ")
    try:
        fecha_creacion = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")
        return fecha_creacion
    except ValueError:
        print("Formato de fecha invalido. Intente de nuevo.")
        return fecha_creacion_alerta()
def id_equipo(): 
    while True:
      try:
        id_equipo = int(input('ingrese el ID del equipo medico relacionado con la alerta:'))
        if id_equipo <= 0:
          print("El ID debe ser un número positivo.") 
        elif cursor.execute("SELECT * FROM EQUIPOS_MEDICOS WHERE ID = ?", (id_equipo,)).fetchone() is None:
          print("No existe un equipo medico con ese ID. Por favor ingrese un ID válido.")
        else:
           return id_equipo
      except ValueError:
        print("Por favor ingrese un ID válido.")   
    
def registrar_alerta():  
    tipo = tipo_alerta()
    mensaje = mensaje_alerta()
    clinica_id = id_clinica()
    equipo_id = id_equipo()
    vacuna_id = id_vacuna()
    severidad = severidad_alerta()
    alerta_id = insertar_datos_alerta(tipo, mensaje, clinica_id, equipo_id, vacuna_id, severidad)
    print(f"Alerta registrada con ID: {alerta_id}")
def mantenimiento_tipo():
    tipo_mantenimiento = input("Ingrese el tipo de mantenimiento: ")
    if tipo_mantenimiento.strip() == "":
        print("El tipo de mantenimiento no puede estar vacio. Intente de nuevo.")
        return tipo_mantenimiento()
    return tipo_mantenimiento
def descripcion_mantenimiento():
    descripcion = input("Ingrese la descripcion del mantenimiento: ")
    if descripcion.strip() == "":
        print("La descripcion no puede estar vacia. Intente de nuevo.")
        return descripcion_mantenimiento()
    return descripcion
def fecha_programada_mantenimiento():
    fecha_str = input("Ingrese la fecha programada del mantenimiento (YYYY-MM-DD): ")
    try:
        fecha_programada = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        return fecha_programada
    except ValueError:
        print("Formato de fecha invalido. Intente de nuevo.")
        return fecha_programada_mantenimiento()
def id_encargado():
    while True:
      try:
        id_encargado = int(input('ingrese el ID del encargado del mantenimiento:'))
        if id_encargado <= 0:
          print("El ID debe ser un número positivo.") 
        elif cursor.execute("SELECT * FROM usuarios WHERE id = ? AND LOWER(rol) = 'tecnico'",(id_encargado,)).fetchone() is None:
          print("No existe un usuario con ese ID con rol de tecnico. Por favor ingrese un ID válido.")
        else:
           return id_encargado
      except ValueError:
        print("Por favor ingrese un ID válido.")    

def registrar_mantenimiento():  
    equipo_id = id_equipo()
    tipo_mantenimiento = mantenimiento_tipo()
    descripcion = descripcion_mantenimiento()
    fecha_programada = fecha_programada_mantenimiento()
    encargado_id = id_encargado()
    mantenimiento_id = insertar_datos_mantenimiento(equipo_id, tipo_mantenimiento, descripcion, fecha_programada, encargado_id)
    print(f"Mantenimiento registrado con ID: {mantenimiento_id}")
def tabla_afectada():
    tabla = input("Ingrese la tabla afectada (clinicas, usuarios, equipos_medicos, vacunas, rutas, registros_temperatura, aplicaciones_vacuna, alertas, mantenimientos): ")
    if tabla.strip() == "":
        print("La tabla no puede estar vacia. Intente de nuevo.")
    elif tabla not in ['clinicas', 'usuarios', 'equipos_medicos', 'vacunas', 'rutas', 'registros_temperatura', 'aplicaciones_vacuna', 'alertas', 'mantenimientos']:
        print("Tabla invalida. Intente de nuevo.")
    else:
        return tabla
def accion_auditoria():
    accion = input("Ingrese la accion realizada (INSERT, UPDATE, DELETE): ")
    if accion.strip() == "":
        print("La accion no puede estar vacia. Intente de nuevo.")
    elif accion not in ['INSERT', 'UPDATE', 'DELETE']:
        print("Accion invalida. Intente de nuevo.")
    else:
        return accion

def usuario_id():
    while True:
      try:
        usuario_id = int(input('ingrese el ID del usuario que realizo la accion:'))
        if usuario_id <= 0:
          print("El ID debe ser un número positivo.") 
        elif cursor.execute("SELECT * FROM USUARIOS WHERE ID = ? AND LOWER(rol) = 'admin'", (usuario_id,)).fetchone() is None:
          print("No existe un usuario con ese ID. Por favor ingrese un ID válido.")
        else:
           return usuario_id
      except ValueError:
        print("Por favor ingrese un ID válido.")

def modificar_datos_tablas():
    match tabla_afectada():
        case 'clinicas':
            match accion_auditoria():
                case 'UPDATE':
                    modificar_datos_clinica()
                case 'DELETE':
                    eliminar_clinica()
        case 'usuarios':
            match accion_auditoria():
                case 'UPDATE':
                    modificar_datos_usuario()
                case 'DELETE':
                    eliminar_usuario()
        case 'equipos_medicos':
            match accion_auditoria():
                case 'UPDATE':
                    modificar_datos_equipo_medico()
                case 'DELETE':
                    eliminar_equipo_medico()
        case 'vacunas':
            match accion_auditoria():   
                case 'UPDATE':
                    modificar_datos_vacuna()
                case 'DELETE':
                    eliminar_vacuna()
        case 'rutas':
            match accion_auditoria():   
                case 'DELETE':
                    eliminar_ruta()
                case 'UPDATE':
                    modificar_datos_ruta()
        case 'registros_temperatura':
            match accion_auditoria():
                case 'DELETE':
                    eliminar_registro_temperatura()
                case'UPDATE':
                    modificar_datos_registro_temperatura()
        case 'aplicaciones_vacuna':
            match accion_auditoria():
                case 'DELETE':
                    eliminar_aplicacion_vacuna()
                case 'UPDATE':
                    modificar_datos_aplicacion_vacuna()
        case 'alertas':
            match accion_auditoria():
                case 'DELETE':
                    eliminar_alerta()
                case 'UPDATE':
                    modificar_datos_alerta()
        case 'mantenimientos':
            match accion_auditoria():
                case 'DELETE':
                    eliminar_mantenimiento()
                case 'UPDATE':
                    modificar_datos_mantenimiento() 
                    
                        

def registrar_auditoria():  
    tabla_afectada = tabla_afectada()
    registro_id = int(input("Ingrese el ID del registro afectado: "))
    accion = accion_auditoria()
    usuario_id = usuario_id()
    valores_anteriores = input("Ingrese los valores anteriores (formato JSON o texto): ")
    valores_nuevos = modificar_datos_tablas
    auditoria_id = insertar_datos_auditoria(tabla_afectada, registro_id, accion, usuario_id, valores_anteriores, valores_nuevos)
    print(f"Auditoria registrada con ID: {auditoria_id}") 
      
def eliminar_clinica():
    clinica_id = id_clinica()
    cursor.execute("DELETE FROM clinicas WHERE id = ?", (clinica_id,))
    conn.commit()
    print(f"Clinica con ID {clinica_id} eliminada.")
def eliminar_usuario():
    usuario_id = int(input("Ingrese el ID del usuario a eliminar: "))
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
    conn.commit()
    print(f"Usuario con ID {usuario_id} eliminado.")
def eliminar_equipo_medico():
    equipo_id = id_equipo()
    cursor.execute("DELETE FROM equipos_medicos WHERE id = ?", (equipo_id,))
    conn.commit()
    print(f"Equipo medico con ID {equipo_id} eliminado.")
def eliminar_vacuna():
    vacuna_id = id_vacuna()
    cursor.execute("DELETE FROM vacunas WHERE id = ?", (vacuna_id,))
    conn.commit()
    print(f"Vacuna con ID {vacuna_id} eliminada.")
def eliminar_ruta():
    ruta_id = int(input("Ingrese el ID de la ruta a eliminar: "))
    cursor.execute("DELETE FROM rutas WHERE id = ?", (ruta_id,))
    conn.commit()
    print(f"Ruta con ID {ruta_id} eliminada.")  
def eliminar_registro_temperatura():
    registro_id = int(input("Ingrese el ID del registro de temperatura a eliminar: "))
    cursor.execute("DELETE FROM registros_temperatura WHERE id = ?", (registro_id,))
    conn.commit()
    print(f"Registro de temperatura con ID {registro_id} eliminado.")   
def eliminar_aplicacion_vacuna():
    aplicacion_id = int(input("Ingrese el ID de la aplicacion de vacuna a eliminar: "))
    cursor.execute("DELETE FROM aplicaciones_vacuna WHERE id = ?", (aplicacion_id,))
    conn.commit()
    print(f"Aplicacion de vacuna con ID {aplicacion_id} eliminada.")
def eliminar_alerta():
    alerta_id = int(input("Ingrese el ID de la alerta a eliminar: "))
    cursor.execute("DELETE FROM alertas WHERE id = ?", (alerta_id,))
    conn.commit()
    print(f"Alerta con ID {alerta_id} eliminada.")
def eliminar_mantenimiento():
    mantenimiento_id = int(input("Ingrese el ID del mantenimiento a eliminar: "))
    cursor.execute("DELETE FROM mantenimientos WHERE id = ?", (mantenimiento_id,))
    conn.commit()
    print(f"Mantenimiento con ID {mantenimiento_id} eliminado.")

def modificar_datos_clinica():
    clinica_id = id_clinica()
    nuevo_nombre = nombre_clinica()
    nuevo_ubicacion = ubicacion_base()
    nuevo_latitud = latitud()
    nuevo_longitud = longitud()
    cursor.execute("""
        UPDATE clinicas
        SET nombre = ?, ubicacion_base = ?, latitud = ?, longitud = ?
        WHERE id = ?;
    """, (nuevo_nombre, nuevo_ubicacion, nuevo_latitud, nuevo_longitud, clinica_id))
    conn.commit()
    print(f"Clinica con ID {clinica_id} modificada.")   
def modificar_datos_usuario():
    usuario_id = int(input("Ingrese el ID del usuario a modificar: "))
    nuevo_username = usuario_username()
    nuevo_nombre_completo = usuario_nombre_completo()
    nuevo_correo = usuario_correo()
    nuevo_rol = usuario_rol()
    cursor.execute("""
        UPDATE usuarios
        SET username = ?, nombre_completo = ?, correo = ?, rol = ?
        WHERE id = ?;
    """, (nuevo_username, nuevo_nombre_completo, nuevo_correo, nuevo_rol, usuario_id))
    conn.commit()
    print(f"Usuario con ID {usuario_id} modificado.")   
def modificar_datos_equipo_medico():
    equipo_id = id_equipo()
    nuevo_tipo = tipo_equipo()
    nuevo_modelo = modelo_equipo()
    nuevo_numero_serie = numero_serie_equipo()
    nuevo_clinica_id = id_clinica()
    nuevo_capacidad_litros = capacidad_litros_equipo()
    cursor.execute("""
        UPDATE equipos_medicos
        SET tipo = ?, modelo = ?, numero_serie = ?, clinica_id = ?, capacidad_litros = ?
        WHERE id = ?;
    """, (nuevo_tipo, nuevo_modelo, nuevo_numero_serie, nuevo_clinica_id, nuevo_capacidad_litros, equipo_id))
    conn.commit()
    print(f"Equipo medico con ID {equipo_id} modificado.")
def modificar_datos_vacuna():
    vacuna_id = id_vacuna()
    nuevo_lote = lote_vacuna()
    nuevo_tipo = tipo_vacuna()
    nuevo_cantidad = cantidad_vacuna()
    nuevo_temperatura_minima = temperatura_minima_vacuna()
    nuevo_temperatura_maxima = temperatura_maxima_vacuna()
    nuevo_fecha_vencimiento = fecha_vencimiento_vacuna()
    nuevo_clinica_id = id_clinica()
    cursor.execute("""
        UPDATE vacunas
        SET lote = ?, tipo = ?, cantidad = ?, temperatura_minima = ?, temperatura_maxima = ?, fecha_vencimiento = ?, clinica_id = ?
        WHERE id = ?;
    """, (nuevo_lote, nuevo_tipo, nuevo_cantidad, nuevo_temperatura_minima, nuevo_temperatura_maxima, nuevo_fecha_vencimiento, nuevo_clinica_id, vacuna_id))
    conn.commit()
    print(f"Vacuna con ID {vacuna_id} modificada.") 
def modificar_datos_ruta():
    ruta_id = int(input("Ingrese el ID de la ruta a modificar: "))
    nuevo_clinica_id = id_clinica()
    nuevo_comunidad = rutas()
    nuevo_fecha = fecha_ruta()
    nuevo_distancia_km = distancia_km_ruta()
    cursor.execute("""
        UPDATE rutas
        SET clinica_id = ?, comunidad = ?, fecha = ?, distancia_km = ?
        WHERE id = ?;
    """, (nuevo_clinica_id, nuevo_comunidad, nuevo_fecha, nuevo_distancia_km, ruta_id))
    conn.commit()
    print(f"Ruta con ID {ruta_id} modificada.")
def modificar_datos_registro_temperatura():
    registro_id = int(input("Ingrese el ID del registro de temperatura a modificar: "))
    nuevo_clinica_id = id_clinica()
    nuevo_equipo_id = id_equipo()
    nuevo_temperatura = registros_temperatura()
    nuevo_latitud = latitud_registro()
    nuevo_longitud = longitud_registro()
    nuevo_fuente = fuente_registro()
    cursor.execute("""
        UPDATE registros_temperatura
        SET clinica_id = ?, equipo_id = ?, temperatura = ?, latitud = ?, longitud = ?, fuente = ?
        WHERE id = ?;
    """, (nuevo_clinica_id, nuevo_equipo_id, nuevo_temperatura, nuevo_latitud, nuevo_longitud, nuevo_fuente, registro_id))
    conn.commit()
    print(f"Registro de temperatura con ID {registro_id} modificado.")  
def modificar_datos_aplicacion_vacuna():
    aplicacion_id = int(input("Ingrese el ID de la aplicacion de vacuna a modificar: "))
    nuevo_clinica_id = id_clinica()
    nuevo_vacuna_id = id_vacuna()
    nuevo_lote = aplicaciones_vacuna_lote()
    nuevo_cantidad = aplicaciones_vacuna_cantidad()
    nuevo_comunidad = id_comunidad_responsable()
    nuevo_paciente_identificacion = aplicaciones_vacuna_paciente_identificacion()
    nuevo_responsable_id = id_comunidad_responsable()
    nuevo_evidencia_firma = aplicaciones_vacuna_evidencia_firma()
    cursor.execute("""
        UPDATE aplicaciones_vacuna
        SET clinica_id = ?, vacuna_id = ?, lote = ?, cantidad = ?, comunidad = ?, paciente_identificacion = ?, responsable_id = ?, evidencia_firma = ?
        WHERE id = ?;
    """, (nuevo_clinica_id, nuevo_vacuna_id, nuevo_lote, nuevo_cantidad, nuevo_comunidad, nuevo_paciente_identificacion, nuevo_responsable_id, nuevo_evidencia_firma, aplicacion_id))
    conn.commit()
    print(f"Aplicacion de vacuna con ID {aplicacion_id} modificada.")   
def modificar_datos_alerta():
    alerta_id = int(input("Ingrese el ID de la alerta a modificar: "))
    nuevo_tipo = tipo_alerta()
    nuevo_mensaje = mensaje_alerta()
    nuevo_clinica_id = id_clinica()
    nuevo_equipo_id = id_equipo()
    nuevo_vacuna_id = id_vacuna()
    nuevo_severidad = severidad_alerta()
    cursor.execute("""
        UPDATE alertas
        SET tipo = ?, mensaje = ?, clinica_id = ?, equipo_id = ?, vacuna_id = ?, severidad = ?
        WHERE id = ?;
    """, (nuevo_tipo, nuevo_mensaje, nuevo_clinica_id, nuevo_equipo_id, nuevo_vacuna_id, nuevo_severidad, alerta_id))
    conn.commit()
    print(f"Alerta con ID {alerta_id} modificada.") 
def modificar_datos_mantenimiento():
    mantenimiento_id = int(input("Ingrese el ID del mantenimiento a modificar: "))
    nuevo_equipo_id = id_equipo()
    nuevo_tipo_mantenimiento = mantenimiento_tipo()
    nuevo_descripcion = descripcion_mantenimiento()
    nuevo_fecha_programada = fecha_programada_mantenimiento()
    nuevo_encargado_id = id_encargado()
    cursor.execute("""
        UPDATE mantenimientos
        SET equipo_id = ?, tipo_mantenimiento = ?, descripcion = ?, fecha_programada = ?, encargado_id = ?
        WHERE id = ?;
    """, (nuevo_equipo_id, nuevo_tipo_mantenimiento, nuevo_descripcion, nuevo_fecha_programada, nuevo_encargado_id, mantenimiento_id))
    conn.commit()
    print(f"Mantenimiento con ID {mantenimiento_id} modificado.")

