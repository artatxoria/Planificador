-- Activa el control de claves foráneas
PRAGMA foreign_keys = ON;

-- =========================================
-- Tabla: Cliente
-- =========================================
CREATE TABLE IF NOT EXISTS Cliente (
  id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
  empresa TEXT NOT NULL,
  persona_contacto TEXT,
  telefono TEXT,
  email TEXT,
  direccion TEXT,
  cif TEXT,
  notas TEXT,
  color_hex TEXT DEFAULT '#377eb8',
  UNIQUE (cif)
);

-- =========================================
-- Tabla: ClienteFinal (empresa donde se imparte la formación)
-- =========================================
CREATE TABLE IF NOT EXISTS ClienteFinal (
  id_cliente_final INTEGER PRIMARY KEY AUTOINCREMENT,
  empresa TEXT NOT NULL,
  persona_encargada TEXT,
  telefono_encargada TEXT,
  email_encargada TEXT,
  direccion TEXT,
  notas TEXT
);

-- =========================================
-- Tabla: ContactoClienteFinal (contactos asociados al cliente final)
-- =========================================
CREATE TABLE IF NOT EXISTS ContactoClienteFinal (
  id_contacto_final INTEGER PRIMARY KEY AUTOINCREMENT,
  id_cliente_final INTEGER NOT NULL,
  nombre TEXT NOT NULL,
  telefono TEXT,
  email TEXT,
  rol TEXT CHECK (rol IN ('encargado_formacion','participante','otro')) DEFAULT 'encargado_formacion',
  notas TEXT,
  FOREIGN KEY (id_cliente_final) REFERENCES ClienteFinal(id_cliente_final)
    ON UPDATE CASCADE ON DELETE CASCADE
);

-- =========================================
-- Tabla: Participante (listado de asistentes si se dispone)
-- =========================================
CREATE TABLE IF NOT EXISTS Participante (
  id_participante INTEGER PRIMARY KEY AUTOINCREMENT,
  id_cliente_final INTEGER NOT NULL,
  nombre TEXT NOT NULL,
  email TEXT,
  telefono TEXT,
  observaciones TEXT,
  FOREIGN KEY (id_cliente_final) REFERENCES ClienteFinal(id_cliente_final)
    ON UPDATE CASCADE ON DELETE CASCADE
);

-- =========================================
-- Tabla: Tema (catálogo)
-- =========================================
CREATE TABLE IF NOT EXISTS Tema (
  id_tema INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL UNIQUE,
  descripcion TEXT
);

-- =========================================
-- Tabla: FormacionBase (catálogo)
-- =========================================
CREATE TABLE IF NOT EXISTS FormacionBase (
  id_formacion_base INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL,
  descripcion TEXT,
  id_tema INTEGER NOT NULL,
  horas_referencia REAL,
  nivel TEXT,               -- p.ej.: basico | intermedio | avanzado
  contenido_base TEXT,
  FOREIGN KEY (id_tema) REFERENCES Tema(id_tema)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  UNIQUE (nombre, nivel)
);

-- =========================================
-- Tabla: ContratacionClienteFormacion (acuerdo con cliente)
-- =========================================
CREATE TABLE IF NOT EXISTS ContratacionClienteFormacion (
  id_contratacion INTEGER PRIMARY KEY AUTOINCREMENT,
  id_cliente INTEGER NOT NULL,
  id_cliente_final INTEGER NULL,                  -- añadido en fase 9
  id_formacion_base INTEGER NOT NULL,
  expediente TEXT NOT NULL,                       -- código único
  precio_hora REAL,
  horas_previstas REAL,
  modalidad TEXT CHECK (modalidad IN ('presencial','online','mixta')),
  direccion TEXT,
  enlace_vc TEXT,
  persona_responsable TEXT,
  telefono_responsable TEXT,
  email_responsable TEXT,
  fecha_inicio_prevista TEXT,                     -- YYYY-MM-DD
  fecha_fin_prevista TEXT,                        -- YYYY-MM-DD
  observaciones TEXT,
  estado TEXT NOT NULL DEFAULT 'tentativo' CHECK (estado IN ('tentativo','confirmado','cancelado')),
  prioridad TEXT NOT NULL DEFAULT 'media' CHECK (prioridad IN ('baja','media','alta')),
  created_at TEXT NOT NULL DEFAULT (CURRENT_TIMESTAMP),
  updated_at TEXT NOT NULL DEFAULT (CURRENT_TIMESTAMP),
  FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  FOREIGN KEY (id_cliente_final) REFERENCES ClienteFinal(id_cliente_final)
    ON UPDATE CASCADE ON DELETE SET NULL,
  FOREIGN KEY (id_formacion_base) REFERENCES FormacionBase(id_formacion_base)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  UNIQUE (expediente)
);

-- Mantener updated_at al día
CREATE TRIGGER IF NOT EXISTS trg_contratacion_updated_at
AFTER UPDATE ON ContratacionClienteFormacion
FOR EACH ROW
BEGIN
  UPDATE ContratacionClienteFormacion
    SET updated_at = CURRENT_TIMESTAMP
    WHERE id_contratacion = NEW.id_contratacion;
END;

-- =========================================
-- Tabla: Sesion (eventos de calendario)
-- =========================================
CREATE TABLE IF NOT EXISTS Sesion (
  id_sesion INTEGER PRIMARY KEY AUTOINCREMENT,
  id_contratacion INTEGER NOT NULL,
  fecha TEXT NOT NULL,        -- YYYY-MM-DD
  hora_inicio TEXT NOT NULL,  -- HH:MM
  hora_fin TEXT NOT NULL,     -- HH:MM
  direccion TEXT,
  enlace_vc TEXT,
  estado TEXT NOT NULL DEFAULT 'propuesta' CHECK (estado IN ('propuesta','programada','reprogramada','cancelada')),
  notas TEXT,
  FOREIGN KEY (id_contratacion) REFERENCES ContratacionClienteFormacion(id_contratacion)
    ON UPDATE CASCADE ON DELETE CASCADE,
  CHECK (length(hora_inicio)=5 AND substr(hora_inicio,3,1)=':'),
  CHECK (length(hora_fin)=5 AND substr(hora_fin,3,1)=':'),
  CHECK (hora_fin > hora_inicio)
);

-- =========================================
-- Tabla: Adjunto (polimórfica)
-- Nota: la FK polimórfica se validará desde la lógica de negocio.
-- =========================================
CREATE TABLE IF NOT EXISTS Adjunto (
  id_adjunto INTEGER PRIMARY KEY AUTOINCREMENT,
  origen TEXT NOT NULL CHECK (origen IN ('cliente','contratacion','sesion')),
  id_origen INTEGER NOT NULL,
  tipo TEXT,
  ruta_fichero TEXT NOT NULL,
  notas TEXT,
  created_at TEXT NOT NULL DEFAULT (CURRENT_TIMESTAMP)
);

-- =========================================
-- Tabla: InteraccionCliente (mini-CRM)
-- =========================================
CREATE TABLE IF NOT EXISTS InteraccionCliente (
  id_interaccion INTEGER PRIMARY KEY AUTOINCREMENT,
  id_cliente INTEGER NOT NULL,
  id_contratacion INTEGER NULL,     -- opcional
  fecha TEXT NOT NULL,              -- YYYY-MM-DD
  tipo TEXT NOT NULL CHECK (tipo IN ('llamada','email','reunion','mensaje','otro')),
  descripcion TEXT,
  resultado TEXT NOT NULL DEFAULT 'pendiente' CHECK (resultado IN ('propuesta','pendiente','negociacion','aceptado','rechazado','sin_respuesta')),
  proxima_accion TEXT,
  fecha_proxima_accion TEXT,        -- YYYY-MM-DD
  crear_recordatorio INTEGER NOT NULL DEFAULT 0 CHECK (crear_recordatorio IN (0,1)),
  created_at TEXT NOT NULL DEFAULT (CURRENT_TIMESTAMP),
  FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente)
    ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (id_contratacion) REFERENCES ContratacionClienteFormacion(id_contratacion)
    ON UPDATE CASCADE ON DELETE SET NULL
);

-- =========================================
-- Índices recomendados
-- =========================================
CREATE INDEX IF NOT EXISTS idx_cliente_cif ON Cliente(cif);
CREATE INDEX IF NOT EXISTS idx_cliente_final_empresa ON ClienteFinal(empresa);
CREATE INDEX IF NOT EXISTS idx_contacto_final_cliente ON ContactoClienteFinal(id_cliente_final);
CREATE INDEX IF NOT EXISTS idx_participante_cliente_final ON Participante(id_cliente_final);
CREATE INDEX IF NOT EXISTS idx_contratacion_cliente ON ContratacionClienteFormacion(id_cliente);
CREATE INDEX IF NOT EXISTS idx_contratacion_cliente_final ON ContratacionClienteFormacion(id_cliente_final);
CREATE INDEX IF NOT EXISTS idx_contratacion_formacion ON ContratacionClienteFormacion(id_formacion_base);
CREATE INDEX IF NOT EXISTS idx_sesion_contratacion_fecha ON Sesion(id_contratacion, fecha, hora_inicio);
CREATE INDEX IF NOT EXISTS idx_interaccion_cliente_fecha ON InteraccionCliente(id_cliente, fecha);
CREATE INDEX IF NOT EXISTS idx_interaccion_proxima_accion ON InteraccionCliente(fecha_proxima_accion);
