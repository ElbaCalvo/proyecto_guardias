CREATE TABLE profesores (
    id_profesor INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    departamento TEXT NOT NULL
);

CREATE TABLE horario (
    id_horario INTEGER PRIMARY KEY AUTOINCREMENT,
    id_profesor INTEGER NOT NULL,
    dia_semana INTEGER NOT NULL CHECK(dia_semana BETWEEN 1 AND 5),
    hora INTEGER NOT NULL,
    tipo TEXT NOT NULL CHECK(tipo IN ('clase', 'guardia', 'libre')),
    aula TEXT,
    UNIQUE(id_profesor, dia_semana, hora), -- Para que un profesor no tenga dos clases al mismo tiempo
    FOREIGN KEY (id_profesor) REFERENCES profesores(id_profesor)
);

CREATE TABLE ausencias (
    id_ausencia INTEGER PRIMARY KEY AUTOINCREMENT,
    id_profesor INTEGER NOT NULL,
    fecha DATE NOT NULL,
    hora INTEGER NOT NULL,
    FOREIGN KEY (id_profesor) REFERENCES profesores(id_profesor)
);

CREATE TABLE presencia (
    id_presencia INTEGER PRIMARY KEY AUTOINCREMENT,
    id_profesor INTEGER NOT NULL,
    fecha DATE NOT NULL,
    hora INTEGER NOT NULL,
    presente BOOLEAN NOT NULL,
    FOREIGN KEY (id_profesor) REFERENCES profesores(id_profesor)
);

CREATE TABLE guardias (
    id_guardia INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha DATE NOT NULL,
    hora INTEGER NOT NULL,
    id_profesor_ausente INTEGER NOT NULL,
    id_profesor_cubre INTEGER NOT NULL,
    aula TEXT NOT NULL,
    UNIQUE(id_profesor_cubre, fecha, hora, aula), -- Para que no se asignen dos guardias al mismo profesor
    FOREIGN KEY (id_profesor_ausente) REFERENCES profesores(id_profesor),
    FOREIGN KEY (id_profesor_cubre) REFERENCES profesores(id_profesor)
);