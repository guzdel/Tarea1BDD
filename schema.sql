DROP TABLE IF EXISTS Torneos CASCADE;
DROP TABLE IF EXISTS Equipos CASCADE;
DROP TABLE IF EXISTS Jugadores CASCADE;
DROP TABLE IF EXISTS Sponsor CASCADE;
DROP TABLE IF EXISTS Pertenece_a CASCADE;
DROP TABLE IF EXISTS Es_capitan CASCADE;
DROP TABLE IF EXISTS Inscripcion CASCADE;
DROP TABLE IF EXISTS Partidas CASCADE;
DROP TABLE IF EXISTS Estadisticas_individuales CASCADE;
DROP TABLE IF EXISTS Auspicia_a CASCADE;

CREATE TABLE Torneos(
    id_torneo SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    videojuego VARCHAR(100) NOT NULL,
    fecha_inicio DATE,
    fecha_fin DATE,
    prize_pool DECIMAL (12,2) CHECK (prize_pool >= 0),
    max_equipos INTEGER CHECK (max_equipos > 0)
);

CREATE TABLE Jugadores(
    gamertag VARCHAR(100) PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100),
    nacimiento DATE,
    pais VARCHAR(100)
);

CREATE TABLE Equipos (
    id_equipo SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    fecha_creacion DATE
);

CREATE TABLE Pertenece_a (
    id_equipo INTEGER REFERENCES Equipos(id_equipo) ON DELETE CASCADE,
    gamertag VARCHAR(50) REFERENCES Jugadores(gamertag) ON DELETE CASCADE,
    PRIMARY KEY (gamertag)
);

CREATE TABLE Es_capitan (
    id_equipo INTEGER REFERENCES Equipos(id_equipo) ON DELETE CASCADE,
    gamertag VARCHAR(50) REFERENCES Jugadores(gamertag) ON DELETE CASCADE,
    PRIMARY KEY (id_equipo)
);

CREATE TABLE Inscripcion (
    id_torneo INTEGER REFERENCES Torneos(id_torneo) ON DELETE CASCADE,
    id_equipo INTEGER REFERENCES Equipos(id_equipo) ON DELETE CASCADE,
    PRIMARY KEY (id_torneo, id_equipo)
);

CREATE TABLE Partidas (
    id_partida SERIAL PRIMARY KEY,
    id_torneo INTEGER REFERENCES Torneos(id_torneo) ON DELETE CASCADE,
    id_equipo_a INTEGER REFERENCES Equipos(id_equipo) ON DELETE CASCADE,
    id_equipo_b INTEGER REFERENCES Equipos(id_equipo) ON DELETE CASCADE,
    puntaje_a INTEGER,
    puntaje_b INTEGER,
    fase VARCHAR(50),
    fecha DATE,
    hora TIME
);

CREATE TABLE Estadisticas_individuales (
    id_partida INTEGER REFERENCES Partidas(id_partida) ON DELETE CASCADE,
    gamertag VARCHAR(50) REFERENCES Jugadores(gamertag) ON DELETE CASCADE,
    ko INTEGER DEFAULT 0,
    restarts INTEGER DEFAULT 0,
    asists INTEGER DEFAULT 0,
    PRIMARY KEY (id_partida, gamertag)
);

CREATE TABLE Sponsor (
    nombre VARCHAR(100) PRIMARY KEY,
    industria VARCHAR(100)
);

CREATE TABLE Auspicia_a (
    nombre_sponsor VARCHAR(100) REFERENCES Sponsor(nombre) ON DELETE CASCADE,
    id_torneo INTEGER REFERENCES Torneos(id_torneo) ON DELETE CASCADE,
    monto DECIMAL(12, 2) CHECK (monto >= 0),
    PRIMARY KEY (nombre_sponsor, id_torneo)
);