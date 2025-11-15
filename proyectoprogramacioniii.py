import sqlite3

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

