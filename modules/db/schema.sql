CREATE TABLE profesores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    departamento TEXT NOT NULL
);

CREATE TABLE horarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profesor_id INTEGER NOT NULL,
    dia TEXT NOT NULL CHECK(dia IN ('lunes','martes','miercoles','jueves','viernes')),
    hora INTEGER NOT NULL,
    UNIQUE(profesor_id, dia, hora),
    FOREIGN KEY (profesor_id) REFERENCES profesores(id)
);

CREATE TABLE ausencias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profesor_id INTEGER NOT NULL,
    fecha DATE NOT NULL,
    motivo TEXT,
    FOREIGN KEY (profesor_id) REFERENCES profesores(id)
);

CREATE TABLE presencia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profesor_id INTEGER NOT NULL,
    fecha DATE NOT NULL,
    estado TEXT NOT NULL CHECK(estado IN ('presente', 'ausente')),
    FOREIGN KEY (profesor_id) REFERENCES profesores(id)
);

CREATE TABLE guardias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profesor_id INTEGER NOT NULL,
    fecha DATE NOT NULL,
    hora TEXT NOT NULL,
    aula TEXT NOT NULL,
    UNIQUE(profesor_id, fecha, hora, aula),
    FOREIGN KEY (profesor_id) REFERENCES profesores(id)
);