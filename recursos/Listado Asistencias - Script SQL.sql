-- Creación de la tabla Usuario:
CREATE TABLE Usuario (
    Email TEXT PRIMARY KEY,
    Clave TEXT NOT NULL,
    fecha_creacion TEXT NOT NULL DEFAULT (datetime('now')),
    fecha_modificacion TEXT DEFAULT (datetime('now'))
);

-- Creación de la tabla Rol
CREATE TABLE IF NOT EXISTS Rol (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT NOT NULL,
	fecha_creacion TEXT NOT NULL DEFAULT (datetime('now')),
    fecha_modificacion TEXT DEFAULT (datetime('now'))
);

-- Creación de la tabla Cargo
CREATE TABLE IF NOT EXISTS Cargo (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT NOT NULL,
	fecha_creacion TEXT NOT NULL DEFAULT (datetime('now')),
    fecha_modificacion TEXT DEFAULT (datetime('now'))
);

-- Creación de la tabla Persona
CREATE TABLE IF NOT EXISTS Persona (
    Identificacion TEXT PRIMARY KEY,
    Nombre TEXT NOT NULL,
    Cargo INTEGER,
    Rol INTEGER,
    Email TEXT NOT NULL,
	fecha_creacion TEXT NOT NULL DEFAULT (datetime('now')),
    fecha_modificacion TEXT DEFAULT (datetime('now')),
	FOREIGN KEY (Email) REFERENCES Usuario(Email),
    FOREIGN KEY (Cargo) REFERENCES Cargo(ID),
    FOREIGN KEY (Rol) REFERENCES Rol(ID)
);

-- Creación de la tabla Instructor
CREATE TABLE IF NOT EXISTS Instructor (
    Identificacion TEXT PRIMARY KEY,
    Rol INTEGER,
    Estado INTEGER NOT NULL,
    Observacion TEXT,
	Email Text NOT NULL,
	fecha_creacion TEXT NOT NULL DEFAULT (datetime('now')),
    fecha_modificacion TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (Identificacion) REFERENCES Persona(Identificacion),
    FOREIGN KEY (Rol) REFERENCES Rol(ID),
	FOREIGN KEY (Email) REFERENCES Usuario(Email)
);

-- Creación de la tabla Dependencia
CREATE TABLE IF NOT EXISTS Dependencia (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT NOT NULL,
	fecha_creacion TEXT NOT NULL DEFAULT (datetime('now')),
    fecha_modificacion TEXT DEFAULT (datetime('now'))
);

-- Creación de la tabla TipoInduccion
CREATE TABLE IF NOT EXISTS TipoInduccion (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT NOT NULL,
	fecha_creacion TEXT NOT NULL DEFAULT (datetime('now')),
    fecha_modificacion TEXT DEFAULT (datetime('now'))
);

-- Creación de la tabla Evento
CREATE TABLE IF NOT EXISTS Evento (
    ID TEXT PRIMARY KEY,
    Nombre TEXT NOT NULL,
    TipoInduccionID INTEGER,
    Duracion NUMERIC NOT NULL,
    MedidaDuracion TEXT,
    Autoregistro INTEGER,
    FechaHoraInicio TEXT,
    FechaHoraTerminacion TEXT,
    Tematica TEXT,
    Instructor TEXT,
	fecha_creacion TEXT NOT NULL DEFAULT (datetime('now')),
    fecha_modificacion TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (TipoInduccionID) REFERENCES TipoInduccion(ID),
    FOREIGN KEY (Instructor) REFERENCES Instructor(Identificacion)
);

-- Creación de la tabla asociativa evento_dependencia para la relación muchos-a-muchos entre Evento y Dependencia
CREATE TABLE IF NOT EXISTS evento_dependencia (
    EventoID TEXT,
    DependenciaID INTEGER,
	fecha_creacion TEXT NOT NULL DEFAULT (datetime('now')),
    fecha_modificacion TEXT DEFAULT (datetime('now')),
    PRIMARY KEY (EventoID, DependenciaID),
    FOREIGN KEY (EventoID) REFERENCES Evento(ID),
    FOREIGN KEY (DependenciaID) REFERENCES Dependencia(ID)
);

-- Creación de la tabla asociativa evento_persona para la relación muchos-a-muchos entre Evento y Persona
CREATE TABLE IF NOT EXISTS evento_persona (
    EventoID TEXT,
    PersonaIdentificacion TEXT,
	fecha_creacion TEXT NOT NULL DEFAULT (datetime('now')),
    fecha_modificacion TEXT DEFAULT (datetime('now')),
    PRIMARY KEY (EventoID, PersonaIdentificacion),
    FOREIGN KEY (EventoID) REFERENCES Evento(ID),
    FOREIGN KEY (PersonaIdentificacion) REFERENCES Persona(Identificacion)
);


INSERT INTO Usuario (Email, Clave, fecha_creacion, fecha_modificacion) VALUES ('usuario1@asistencia.co', 'clave1', datetime('now'), datetime('now'));
INSERT INTO Usuario (Email, Clave, fecha_creacion, fecha_modificacion) VALUES ('usuario2@asistencia.co', 'clave2', datetime('now'), datetime('now'));
INSERT INTO Usuario (Email, Clave, fecha_creacion, fecha_modificacion) VALUES ('usuario3@asistencia.co', 'clave3', datetime('now'), datetime('now'));
INSERT INTO Usuario (Email, Clave, fecha_creacion, fecha_modificacion) VALUES ('usuario4@asistencia.co', 'clave4', datetime('now'), datetime('now'));
INSERT INTO Usuario (Email, Clave, fecha_creacion, fecha_modificacion) VALUES ('usuario5@asistencia.co', 'clave5', datetime('now'), datetime('now'));
INSERT INTO Usuario (Email, Clave, fecha_creacion, fecha_modificacion) VALUES ('usuario6@asistencia.co', 'clave6', datetime('now'), datetime('now'));
INSERT INTO Usuario (Email, Clave, fecha_creacion, fecha_modificacion) VALUES ('usuario7@asistencia.co', 'clave7', datetime('now'), datetime('now'));
INSERT INTO Usuario (Email, Clave, fecha_creacion, fecha_modificacion) VALUES ('usuario8@asistencia.co', 'clave8', datetime('now'), datetime('now'));
INSERT INTO Usuario (Email, Clave, fecha_creacion, fecha_modificacion) VALUES ('usuario9@asistencia.co', 'clave9', datetime('now'), datetime('now'));
INSERT INTO Usuario (Email, Clave, fecha_creacion, fecha_modificacion) VALUES ('usuario10@asistencia.co', 'clave10', datetime('now'), datetime('now'));


INSERT INTO Dependencia (Nombre) VALUES ('Recursos Humanos');
INSERT INTO Dependencia (Nombre) VALUES ('Finanzas');
INSERT INTO Dependencia (Nombre) VALUES ('Tecnología de la Información');
INSERT INTO Dependencia (Nombre) VALUES ('Marketing');
INSERT INTO Dependencia (Nombre) VALUES ('Ventas');
INSERT INTO Dependencia (Nombre) VALUES ('Atención al Cliente');
INSERT INTO Dependencia (Nombre) VALUES ('Investigación y Desarrollo');
INSERT INTO Dependencia (Nombre) VALUES ('Producción');
INSERT INTO Dependencia (Nombre) VALUES ('Compras');
INSERT INTO Dependencia (Nombre) VALUES ('Logística');


INSERT INTO TipoInduccion (Nombre) VALUES ('Inducción de Seguridad');
INSERT INTO TipoInduccion (Nombre) VALUES ('Orientación para Nuevos Empleados');
INSERT INTO TipoInduccion (Nombre) VALUES ('Capacitación en Software');
INSERT INTO TipoInduccion (Nombre) VALUES ('Taller de Liderazgo');
INSERT INTO TipoInduccion (Nombre) VALUES ('Entrenamiento de Servicio al Cliente');
INSERT INTO TipoInduccion (Nombre) VALUES ('Seminario de Gestión de Proyectos');
INSERT INTO TipoInduccion (Nombre) VALUES ('Curso de Marketing Digital');
INSERT INTO TipoInduccion (Nombre) VALUES ('Programa de Desarrollo Profesional');
INSERT INTO TipoInduccion (Nombre) VALUES ('Sesión de Estrategia Corporativa');
INSERT INTO TipoInduccion (Nombre) VALUES ('Capacitación en Prevención de Riesgos');


INSERT INTO Persona (Identificacion, Nombre, Cargo, Rol, Email) VALUES ('1000000001', 'Ana Torres', 1, 1, 'usuario@asistencia.co');
INSERT INTO Persona (Identificacion, Nombre, Cargo, Rol, Email) VALUES ('1000000002', 'Carlos Gómez', 2, 2, 'usuario@asistencia.co');
INSERT INTO Persona (Identificacion, Nombre, Cargo, Rol, Email) VALUES ('1000000003', 'Beatriz Molina', 3, 3, 'usuario@asistencia.co');
INSERT INTO Persona (Identificacion, Nombre, Cargo, Rol, Email) VALUES ('1000000004', 'David Jiménez', 4, 4, 'usuario@asistencia.co');
INSERT INTO Persona (Identificacion, Nombre, Cargo, Rol, Email) VALUES ('1000000005', 'Elena Núñez', 5, 5, 'usuario@asistencia.co');
INSERT INTO Persona (Identificacion, Nombre, Cargo, Rol, Email) VALUES ('1000000006', 'Fernando Castro', 6, 6, 'usuario@asistencia.co');
INSERT INTO Persona (Identificacion, Nombre, Cargo, Rol, Email) VALUES ('1000000007', 'Gabriela López', 7, 7, 'usuario@asistencia.co');
INSERT INTO Persona (Identificacion, Nombre, Cargo, Rol, Email) VALUES ('1000000008', 'Hugo Sánchez', 8, 8, 'usuario@asistencia.co');
INSERT INTO Persona (Identificacion, Nombre, Cargo, Rol, Email) VALUES ('1000000009', 'Irene Márquez', 9, 9, 'usuario@asistencia.co');
INSERT INTO Persona (Identificacion, Nombre, Cargo, Rol, Email) VALUES ('1000000010', 'Javier Ponce', 10, 10, 'usuario@asistencia.co');
INSERT INTO Persona (Identificacion, Nombre, Cargo, Rol, Email) VALUES ('1000000011', 'Karla Gutiérrez', 11, 1, 'usuario@asistencia.co');
INSERT INTO Persona (Identificacion, Nombre, Cargo, Rol, Email) VALUES ('1000000012', 'Luis Navarro', 12, 2, 'usuario@asistencia.co');
INSERT INTO Persona (Identificacion, Nombre, Cargo, Rol, Email) VALUES ('1000000013', 'Mónica Herrera', 13, 3, 'usuario@asistencia.co');
INSERT INTO Persona (Identificacion, Nombre, Cargo, Rol, Email) VALUES ('1000000014', 'Nicolás Vega', 14, 4, 'usuario@asistencia.co');
INSERT INTO Persona (Identificacion, Nombre, Cargo, Rol, Email) VALUES ('1000000015', 'Olivia Rodríguez', 1, 5, 'usuario@asistencia.co');
INSERT INTO Persona (Identificacion, Nombre, Cargo, Rol, Email) VALUES ('1000000016', 'Pablo Alonso', 2, 6, 'usuario@asistencia.co');
INSERT INTO Persona (Identificacion, Nombre, Cargo, Rol, Email) VALUES ('1000000017', 'Quintina Solís', 3, 7, 'usuario@asistencia.co');
INSERT INTO Persona (Identificacion, Nombre, Cargo, Rol, Email) VALUES ('1000000018', 'Roberto Giraldo', 4, 8, 'usuario@asistencia.co');
INSERT INTO Persona (Identificacion, Nombre, Cargo, Rol, Email) VALUES ('1000000019', 'Sandra Osorio', 5, 9, 'usuario@asistencia.co');
INSERT INTO Persona (Identificacion, Nombre, Cargo, Rol, Email) VALUES ('1000000020', 'Tomás Mejía', 6, 10, 'usuario@asistencia.co');
