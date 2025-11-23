import sqlite3
from datetime import datetime
import customtkinter as ctk
from tkinter import ttk, messagebox
import random as r
import time as y

conn = sqlite3.connect('basededatosclinicas.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

def verificar_admin_auditoria():
    try:
        usuario_id = int(input("Ingrese su ID de Admin para autorizar: "))
        cursor.execute("SELECT * FROM usuarios WHERE id = ?", (usuario_id,))
        usuario = cursor.fetchone()

        if usuario is None:
            print("Error: Usuario no encontrado.")
            return None

        if usuario['rol'].lower() != 'admin':
            print(f"Acceso Denegado: El usuario {usuario['username']} no es administrador.")
            return None

        return usuario_id
    except ValueError:
        print("Error: ID debe ser numerico.")
        return None

def ejecutar_transaccion_auditada(admin_id, tabla, registro_id, query_sql, parametros_sql, accion_tipo):
    try:
        cursor.execute(f"SELECT * FROM {tabla} WHERE id = ?", (registro_id,))
        fila_anterior = cursor.fetchone()

        if not fila_anterior:
            print(f"Error: El registro ID {registro_id} no existe en {tabla}.")
            return False

        valores_ant_str = str(dict(fila_anterior))

        print(f"VALORES ACTUALES ({tabla})")
        print(valores_ant_str)

        confirm = input(f"Confirmar {accion_tipo}? (si/no): ")
        if confirm.lower() != 'si':
            print("Operacion cancelada.")
            return False

        cursor.execute(query_sql, parametros_sql)

        valores_nue_str = ""

        if accion_tipo == 'UPDATE':
            cursor.execute(f"SELECT * FROM {tabla} WHERE id = ?", (registro_id,))
            fila_nueva = cursor.fetchone()
            if fila_nueva:
                valores_nue_str = str(dict(fila_nueva))
                print("VALORES NUEVOS")
                print(valores_nue_str)
        else:
            print("REGISTRO ELIMINADO")

        query_audit = """
        INSERT INTO auditoria (tabla_afectada, registro_id, accion, usuario_id, valores_anteriores, valores_nuevos)
        VALUES (?, ?, ?, ?, ?, ?);
        """
        cursor.execute(query_audit, (tabla, registro_id, accion_tipo, admin_id, valores_ant_str, valores_nue_str))

        conn.commit()
        print("Cambio realizado y auditoria guardada exitosamente.")
        return True

    except sqlite3.Error as e:
        conn.rollback()
        print(f"Error de base de datos: {e}")
        return False

def crear_tablas():
    query = """
    PRAGMA foreign_keys = ON;

    CREATE TABLE IF NOT EXISTS clinicas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL UNIQUE,
        ubicacion_base TEXT NOT NULL,
        latitud REAL,
        longitud REAL,
        estado TEXT DEFAULT 'activa',
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

crear_tablas()

def insertar_datos_clnica(nombre, ubicacion_base, latitud, longitud):
    query = "INSERT INTO clinicas (nombre, ubicacion_base, latitud, longitud) VALUES (?, ?, ?, ?);"
    cursor.execute(query, (nombre, ubicacion_base, latitud, longitud))
    conn.commit()
    return cursor.lastrowid

def insertar_datos_usuario(username, nombre_completo, correo, rol):
    query = "INSERT INTO usuarios (username, nombre_completo, correo, rol) VALUES (?, ?, ?, ?);"
    cursor.execute(query, (username, nombre_completo, correo, rol))
    conn.commit()
    return cursor.lastrowid

def insertar_datos_equipo_medico(tipo, modelo, numero_serie, clinica_id, capacidad_litros):
    query = "INSERT INTO equipos_medicos (tipo, modelo, numero_serie, clinica_id, capacidad_litros) VALUES (?, ?, ?, ?, ?);"
    cursor.execute(query, (tipo, modelo, numero_serie, clinica_id, capacidad_litros))
    conn.commit()
    return cursor.lastrowid

def insertar_datos_vacuna(lote, tipo, cantidad, temperatura_minima, temperatura_maxima, fecha_vencimiento, clinica_id):
    query = "INSERT INTO vacunas (lote, tipo, cantidad, temperatura_minima, temperatura_maxima, fecha_vencimiento, clinica_id) VALUES (?, ?, ?, ?, ?, ?, ?);"
    cursor.execute(query, (lote, tipo, cantidad, temperatura_minima, temperatura_maxima, fecha_vencimiento, clinica_id))
    conn.commit()
    return cursor.lastrowid

def insertar_datos_ruta(clinica_id, comunidad, fecha, distancia_km):    
    query = "INSERT INTO rutas (clinica_id, comunidad, fecha, distancia_km) VALUES (?, ?, ?, ?);"
    cursor.execute(query, (clinica_id, comunidad, fecha, distancia_km))
    conn.commit()
    return cursor.lastrowid

def insertar_datos_registro_temperatura(clinica_id, equipo_id, temperatura, latitud, longitud, fuente):
    query = "INSERT INTO registros_temperatura (clinica_id, equipo_id, temperatura, latitud, longitud, fuente) VALUES (?, ?, ?, ?, ?, ?);"
    cursor.execute(query, (clinica_id, equipo_id, temperatura, latitud, longitud, fuente))
    conn.commit()
    return cursor.lastrowid

def insertar_datos_aplicacion_vacuna(clinica_id, vacuna_id, lote, cantidad, comunidad, paciente_identificacion, responsable_id, evidencia_firma):
    query = "INSERT INTO aplicaciones_vacuna (clinica_id, vacuna_id, lote, cantidad, comunidad, paciente_identificacion, responsable_id, evidencia_firma) VALUES (?, ?, ?, ?, ?, ?, ?, ?);"
    cursor.execute(query, (clinica_id, vacuna_id, lote, cantidad, comunidad, paciente_identificacion, responsable_id, evidencia_firma))
    conn.commit()
    return cursor.lastrowid

def insertar_datos_alerta(tipo, mensaje, clinica_id, equipo_id, vacuna_id, severidad):
    query = "INSERT INTO alertas (tipo, mensaje, clinica_id, equipo_id, vacuna_id, severidad) VALUES (?, ?, ?, ?, ?, ?);"
    cursor.execute(query, (tipo, mensaje, clinica_id, equipo_id, vacuna_id, severidad))
    conn.commit()
    return cursor.lastrowid

def insertar_datos_mantenimiento(equipo_id, tipo_mantenimiento, descripcion, fecha_programada, encargado_id):
    query = "INSERT INTO mantenimientos (equipo_id, tipo_mantenimiento, descripcion, fecha_programada, encargado_id) VALUES (?, ?, ?, ?, ?);"
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
    if nombre.strip() == "": return nombre_clinica()
    return nombre
def ubicacion_base():
    ubicacion = input("Ingrese la ubicacion base de la clinica: ")
    if ubicacion.strip() == "": return ubicacion_base()
    return ubicacion
def latitud():
    try: return float(input("Ingrese la latitud de la clinica: "))
    except ValueError: return latitud()
def longitud():  
    try:
        lon = float(input("Ingrese la longitud de la clinica: "))
        if lon == 0: return longitud()   
        return lon
    except ValueError: return longitud()
def usuario_username():
    username = input("Ingrese el nombre de usuario: ")
    if username.strip() == "": return usuario_username()
    return username 
def usuario_nombre_completo():
    nombre_completo = input("Ingrese el nombre completo del usuario: ")
    if nombre_completo.strip() == "": return usuario_nombre_completo()
    return nombre_completo
def usuario_correo():
    correo = input("Ingrese el correo del usuario: ")
    if correo.strip() == "": return usuario_correo()
    return correo
def usuario_rol():
    while True:
        rol = input("Ingrese el rol del usuario (admin, medico, tecnico): ")
        if rol.strip() != "" and rol in ['admin', 'medico', 'tecnico']: return rol
def tipo_equipo():
    tipo = input("Ingrese el tipo de equipo medico: ")
    if tipo.strip() == "": return tipo_equipo()
    return tipo 
def modelo_equipo():
    modelo = input("Ingrese el modelo del equipo medico: ")
    if modelo.strip() == "": return modelo_equipo()
    return modelo
def numero_serie_equipo():
    numero_serie = input("Ingrese el numero de serie del equipo medico: ")
    if numero_serie.strip() == "": return numero_serie_equipo()
    return numero_serie
def capacidad_litros_equipo():
    try:
        litros = float(input("Ingrese la capacidad en litros del equipo medico: ")) 
        if litros > 0: return litros
    except ValueError: pass
    return capacidad_litros_equipo()
def id_clinica():
    while True:
        try:
            id_c = int(input('ingrese el ID de la clinica:'))
            if id_c > 0:
                if cursor.execute("SELECT 1 FROM CLINICAS WHERE ID = ?", (id_c,)).fetchone(): return id_c
        except ValueError: pass
        print("ID invalido.")

def id_equipo(): 
    while True:
        try:
            id_e = int(input('ingrese el ID del equipo medico:'))
            if id_e > 0:
                if cursor.execute("SELECT 1 FROM EQUIPOS_MEDICOS WHERE ID = ?", (id_e,)).fetchone(): return id_e
        except ValueError: pass
        print("ID invalido.")
def id_vacuna():
    while True:
        try:
            id_v = int(input('ingrese el ID de la vacuna:'))
            if id_v > 0:
                if cursor.execute("SELECT 1 FROM VACUNAS WHERE ID = ?", (id_v,)).fetchone(): return id_v
        except ValueError: pass
        print("ID invalido.")

def registrar_clinica():    
    nombre = nombre_clinica()
    ubicacion = ubicacion_base()
    lat = latitud()
    lon = longitud()
    clinica_id = insertar_datos_clnica(nombre, ubicacion, lat, lon)
    print(f"Clinica registrada con ID: {clinica_id}")   
def registrar_usuario():    
    username = usuario_username()
    nombre_completo = usuario_nombre_completo()
    correo = usuario_correo()
    rol = usuario_rol()
    usuario_id = insertar_datos_usuario(username, nombre_completo, correo, rol)
    print(f"Usuario registrada con ID: {usuario_id}")

def eliminar_clinica():
    admin_id = verificar_admin_auditoria()
    if not admin_id: return
    
    reg_id = id_clinica()
    sql = "DELETE FROM clinicas WHERE id = ?"
    params = (reg_id,)
    
    ejecutar_transaccion_auditada(admin_id, 'clinicas', reg_id, sql, params, 'DELETE')

def eliminar_usuario():
    admin_id = verificar_admin_auditoria()
    if not admin_id: return
    
    try: reg_id = int(input("Ingrese ID Usuario a eliminar: "))
    except: return
    
    sql = "DELETE FROM usuarios WHERE id = ?"
    params = (reg_id,)
    ejecutar_transaccion_auditada(admin_id, 'usuarios', reg_id, sql, params, 'DELETE')

def eliminar_equipo_medico():
    admin_id = verificar_admin_auditoria()
    if not admin_id: return
    reg_id = id_equipo()
    sql = "DELETE FROM equipos_medicos WHERE id = ?"
    params = (reg_id,)
    ejecutar_transaccion_auditada(admin_id, 'equipos_medicos', reg_id, sql, params, 'DELETE')

def eliminar_vacuna():
    admin_id = verificar_admin_auditoria()
    if not admin_id: return
    reg_id = id_vacuna()
    sql = "DELETE FROM vacunas WHERE id = ?"
    params = (reg_id,)
    ejecutar_transaccion_auditada(admin_id, 'vacunas', reg_id, sql, params, 'DELETE')

def eliminar_ruta():
    admin_id = verificar_admin_auditoria()
    if not admin_id: return
    try: reg_id = int(input("Ingrese ID Ruta: "))
    except: return
    sql = "DELETE FROM rutas WHERE id = ?"
    params = (reg_id,)
    ejecutar_transaccion_auditada(admin_id, 'rutas', reg_id, sql, params, 'DELETE')

def eliminar_registro_temperatura():
    admin_id = verificar_admin_auditoria()
    if not admin_id: return
    try: reg_id = int(input("Ingrese ID Registro Temp: "))
    except: return
    sql = "DELETE FROM registros_temperatura WHERE id = ?"
    params = (reg_id,)
    ejecutar_transaccion_auditada(admin_id, 'registros_temperatura', reg_id, sql, params, 'DELETE')

def eliminar_aplicacion_vacuna():
    admin_id = verificar_admin_auditoria()
    if not admin_id: return
    try: reg_id = int(input("Ingrese ID Aplicacion: "))
    except: return
    sql = "DELETE FROM aplicaciones_vacuna WHERE id = ?"
    params = (reg_id,)
    ejecutar_transaccion_auditada(admin_id, 'aplicaciones_vacuna', reg_id, sql, params, 'DELETE')

def eliminar_alerta():
    admin_id = verificar_admin_auditoria()
    if not admin_id: return
    try: reg_id = int(input("Ingrese ID Alerta: "))
    except: return
    sql = "DELETE FROM alertas WHERE id = ?"
    params = (reg_id,)
    ejecutar_transaccion_auditada(admin_id, 'alertas', reg_id, sql, params, 'DELETE')

def eliminar_mantenimiento():
    admin_id = verificar_admin_auditoria()
    if not admin_id: return
    try: reg_id = int(input("Ingrese ID Mantenimiento: "))
    except: return
    sql = "DELETE FROM mantenimientos WHERE id = ?"
    params = (reg_id,)
    ejecutar_transaccion_auditada(admin_id, 'mantenimientos', reg_id, sql, params, 'DELETE')

def modificar_datos_clinica():
    admin_id = verificar_admin_auditoria()
    if not admin_id: return
    
    clinica_id = id_clinica()
    nuevo_nombre = nombre_clinica()
    nuevo_ubicacion = ubicacion_base()
    nuevo_latitud = latitud()
    nuevo_longitud = longitud()
    
    sql = "UPDATE clinicas SET nombre=?, ubicacion_base=?, latitud=?, longitud=? WHERE id=?"
    params = (nuevo_nombre, nuevo_ubicacion, nuevo_latitud, nuevo_longitud, clinica_id)
    
    ejecutar_transaccion_auditada(admin_id, 'clinicas', clinica_id, sql, params, 'UPDATE')

def modificar_datos_usuario():
    admin_id = verificar_admin_auditoria()
    if not admin_id: return
    
    try: usuario_id = int(input("ID Usuario a modificar: "))
    except: return
    
    nuevo_username = usuario_username()
    nuevo_nombre = usuario_nombre_completo()
    nuevo_correo = usuario_correo()
    nuevo_rol = usuario_rol()
    
    sql = "UPDATE usuarios SET username=?, nombre_completo=?, correo=?, rol=? WHERE id=?"
    params = (nuevo_username, nuevo_nombre, nuevo_correo, nuevo_rol, usuario_id)
    
    ejecutar_transaccion_auditada(admin_id, 'usuarios', usuario_id, sql, params, 'UPDATE')

def modificar_datos_equipo_medico():
    admin_id = verificar_admin_auditoria()
    if not admin_id: return
    
    equipo_id = id_equipo()
    ntipo = tipo_equipo()
    nmodelo = modelo_equipo()
    nserie = numero_serie_equipo()
    nclinica = id_clinica()
    ncapacidad = capacidad_litros_equipo()
    
    sql = "UPDATE equipos_medicos SET tipo=?, modelo=?, numero_serie=?, clinica_id=?, capacidad_litros=? WHERE id=?"
    params = (ntipo, nmodelo, nserie, nclinica, ncapacidad, equipo_id)
    
    ejecutar_transaccion_auditada(admin_id, 'equipos_medicos', equipo_id, sql, params, 'UPDATE')

def tabla_afectada():
    tabla = input("Ingrese la tabla afectada (clinicas, usuarios, equipos_medicos, vacunas, rutas, registros_temperatura, aplicaciones_vacuna, alertas, mantenimientos): ")
    if tabla not in ['clinicas', 'usuarios', 'equipos_medicos', 'vacunas', 'rutas', 'registros_temperatura', 'aplicaciones_vacuna', 'alertas', 'mantenimientos']:
        print("Tabla invalida.")
        return tabla_afectada()
    return tabla

def accion_auditoria():
    accion = input("Ingrese la accion realizada (UPDATE, DELETE): ").upper()
    if accion not in ['UPDATE', 'DELETE']:
        print("Accion invalida.")
        return accion_auditoria()
    return accion

def modificar_datos_tablas():
    print("SISTEMA DE GESTION Y AUDITORIA")
    tabla = tabla_afectada()
    accion = accion_auditoria()
    
    if tabla == 'clinicas':
        if accion == 'UPDATE': modificar_datos_clinica()
        elif accion == 'DELETE': eliminar_clinica()
    
    elif tabla == 'usuarios':
        if accion == 'UPDATE': modificar_datos_usuario()
        elif accion == 'DELETE': eliminar_usuario()
        
    elif tabla == 'equipos_medicos':
        if accion == 'UPDATE': modificar_datos_equipo_medico()
        elif accion == 'DELETE': eliminar_equipo_medico()
        
    elif tabla == 'vacunas':
        if accion == 'DELETE': eliminar_vacuna()
        
    elif tabla == 'rutas':
        if accion == 'DELETE': eliminar_ruta()
        
    elif tabla == 'registros_temperatura':
        if accion == 'DELETE': eliminar_registro_temperatura()
        
    elif tabla == 'aplicaciones_vacuna':
        if accion == 'DELETE': eliminar_aplicacion_vacuna()
        
    elif tabla == 'alertas':
        if accion == 'DELETE': eliminar_alerta()
        
    elif tabla == 'mantenimientos':
        if accion == 'DELETE': eliminar_mantenimiento()
        
    else:
        print("Opcion no configurada aun.")