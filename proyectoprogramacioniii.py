import sqlite3
from datetime import datetime
conn = sqlite3.connect('basededatosclinicas.db')
cursor = conn.cursor()

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
        rol TEXT NOT NULL, -- ENUM removido
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
        metadata TEXT,
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
def insertar_datos_alerta(tipo, mensaje, clinica_id, equipo_id, vacuna_id, severidad, metadata):
    query = """
    INSERT INTO alertas (tipo, mensaje, clinica_id, equipo_id, vacuna_id, severidad, metadata)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    """
    cursor.execute(query, (tipo, mensaje, clinica_id, equipo_id, vacuna_id, severidad, metadata))
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
    rol = input("Ingrese el rol del usuario (admin, medico, tecnico): ")
    if rol.strip() == "":
        print("El rol no puede estar vacio. Intente de nuevo.")
    elif rol not in ['admin', 'medico', 'tecnico']:
        print("Rol invalido. Intente de nuevo.")
    else:
        return rol
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

    

    
 

