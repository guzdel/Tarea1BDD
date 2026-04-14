-- =========================================
-- DATOS SINTÉTICOS
-- =========================================

BEGIN;

-- =========================================
-- 1. TORNEOS
-- =========================================
INSERT INTO Torneos (id_torneo, nombre, videojuego, fecha_inicio, fecha_fin, prize_pool, max_equipos) VALUES
(1, 'World Arena Masters 2026', 'Valorant', '2026-06-01', '2026-06-07', 50000.00, 8),
(2, 'Legends Clash Open 2026', 'League of Legends', '2026-07-10', '2026-07-15', 30000.00, 8),
(3, 'Rocket Rivals Cup 2026', 'Rocket League', '2026-08-20', '2026-08-22', 15000.00, 8);

-- =========================================
-- 2. EQUIPOS
-- =========================================
INSERT INTO Equipos (id_equipo, nombre, fecha_creacion) VALUES
(1, 'Alpha Wolves', '2024-01-10'),
(2, 'Crimson Vipers', '2024-02-14'),
(3, 'Nebula Core', '2024-03-01'),
(4, 'Titan Forge', '2024-03-22'),
(5, 'Shadow Ravens', '2024-04-12'),
(6, 'Solar Phoenix', '2024-05-05'),
(7, 'Iron Tempest', '2024-05-28'),
(8, 'Quantum Reapers', '2024-06-15'),
(9, 'Frost Giants', '2024-07-03'),
(10, 'Void Strikers', '2024-08-11');

-- =========================================
-- 3. JUGADORES (5 por equipo = 50)
-- =========================================
INSERT INTO Jugadores (gamertag, nombre, email, nacimiento, pais) VALUES
('alpha1', 'Ariel Soto', 'alpha1@esports.com', '2000-01-10', 'Chile'),
('alpha2', 'Benjamín Rojas', 'alpha2@esports.com', '2001-02-11', 'Chile'),
('alpha3', 'Camilo Díaz', 'alpha3@esports.com', '2002-03-12', 'Perú'),
('alpha4', 'Diego Fuentes', 'alpha4@esports.com', '2000-04-13', 'Argentina'),
('alpha5', 'Esteban Lara', 'alpha5@esports.com', '1999-05-14', 'Chile'),

('viper1', 'Felipe Cruz', 'viper1@esports.com', '2000-06-10', 'Chile'),
('viper2', 'Gabriel Mora', 'viper2@esports.com', '2001-07-11', 'Uruguay'),
('viper3', 'Héctor Pérez', 'viper3@esports.com', '2002-08-12', 'Chile'),
('viper4', 'Ignacio Silva', 'viper4@esports.com', '2000-09-13', 'Argentina'),
('viper5', 'Joaquín Vera', 'viper5@esports.com', '1999-10-14', 'Chile'),

('nebula1', 'Kevin Torres', 'nebula1@esports.com', '2001-01-15', 'Chile'),
('nebula2', 'Luis Paredes', 'nebula2@esports.com', '2000-02-16', 'Perú'),
('nebula3', 'Matías Bravo', 'nebula3@esports.com', '2002-03-17', 'Chile'),
('nebula4', 'Nicolás Leiva', 'nebula4@esports.com', '2001-04-18', 'Chile'),
('nebula5', 'Óscar Pinto', 'nebula5@esports.com', '1999-05-19', 'Bolivia'),

('titan1', 'Pablo Núñez', 'titan1@esports.com', '2000-06-20', 'Chile'),
('titan2', 'Quentin Mella', 'titan2@esports.com', '2001-07-21', 'Chile'),
('titan3', 'Ricardo Saez', 'titan3@esports.com', '2002-08-22', 'Argentina'),
('titan4', 'Sebastián Orellana', 'titan4@esports.com', '2000-09-23', 'Chile'),
('titan5', 'Tomás Gallardo', 'titan5@esports.com', '1999-10-24', 'Perú'),

('shadow1', 'Ulises Campos', 'shadow1@esports.com', '2001-11-10', 'Chile'),
('shadow2', 'Vicente Moya', 'shadow2@esports.com', '2000-12-11', 'Chile'),
('shadow3', 'Walter Jara', 'shadow3@esports.com', '2002-01-12', 'Paraguay'),
('shadow4', 'Xavier Núñez', 'shadow4@esports.com', '2001-02-13', 'Chile'),
('shadow5', 'Yago Salinas', 'shadow5@esports.com', '1999-03-14', 'Argentina'),

('solar1', 'Zaid Herrera', 'solar1@esports.com', '2000-04-10', 'Chile'),
('solar2', 'Andrés Ruiz', 'solar2@esports.com', '2001-05-11', 'Chile'),
('solar3', 'Bruno Cid', 'solar3@esports.com', '2002-06-12', 'Uruguay'),
('solar4', 'César Pino', 'solar4@esports.com', '2000-07-13', 'Chile'),
('solar5', 'Damián Yáñez', 'solar5@esports.com', '1999-08-14', 'Perú'),

('iron1', 'Elías Riquelme', 'iron1@esports.com', '2001-09-10', 'Chile'),
('iron2', 'Franco Tapia', 'iron2@esports.com', '2000-10-11', 'Argentina'),
('iron3', 'Gonzalo Cañas', 'iron3@esports.com', '2002-11-12', 'Chile'),
('iron4', 'Hugo Espinoza', 'iron4@esports.com', '2001-12-13', 'Chile'),
('iron5', 'Iván Molina', 'iron5@esports.com', '1999-01-14', 'Bolivia'),

('quantum1', 'Julián Araya', 'quantum1@esports.com', '2000-02-10', 'Chile'),
('quantum2', 'Kurt Lagos', 'quantum2@esports.com', '2001-03-11', 'Chile'),
('quantum3', 'Leandro Peña', 'quantum3@esports.com', '2002-04-12', 'Perú'),
('quantum4', 'Marco Arce', 'quantum4@esports.com', '2000-05-13', 'Chile'),
('quantum5', 'Nadir Cáceres', 'quantum5@esports.com', '1999-06-14', 'Argentina'),

('frost1', 'Orlando Reyes', 'frost1@esports.com', '2001-07-10', 'Chile'),
('frost2', 'Patricio Toro', 'frost2@esports.com', '2000-08-11', 'Chile'),
('frost3', 'Ramiro Soto', 'frost3@esports.com', '2002-09-12', 'Uruguay'),
('frost4', 'Sergio Puga', 'frost4@esports.com', '2001-10-13', 'Chile'),
('frost5', 'Thiago Moreno', 'frost5@esports.com', '1999-11-14', 'Perú'),

('void1', 'Uriel Lagos', 'void1@esports.com', '2000-12-10', 'Chile'),
('void2', 'Valentín Cifuentes', 'void2@esports.com', '2001-01-11', 'Chile'),
('void3', 'William Prado', 'void3@esports.com', '2002-02-12', 'Paraguay'),
('void4', 'Ximeno Díaz', 'void4@esports.com', '2000-03-13', 'Chile'),
('void5', 'Yerko Mardones', 'void5@esports.com', '1999-04-14', 'Argentina');

-- =========================================
-- 4. PERTENENCIA
-- =========================================
INSERT INTO Pertenece_a (id_equipo, gamertag) VALUES
(1, 'alpha1'), (1, 'alpha2'), (1, 'alpha3'), (1, 'alpha4'), (1, 'alpha5'),
(2, 'viper1'), (2, 'viper2'), (2, 'viper3'), (2, 'viper4'), (2, 'viper5'),
(3, 'nebula1'), (3, 'nebula2'), (3, 'nebula3'), (3, 'nebula4'), (3, 'nebula5'),
(4, 'titan1'), (4, 'titan2'), (4, 'titan3'), (4, 'titan4'), (4, 'titan5'),
(5, 'shadow1'), (5, 'shadow2'), (5, 'shadow3'), (5, 'shadow4'), (5, 'shadow5'),
(6, 'solar1'), (6, 'solar2'), (6, 'solar3'), (6, 'solar4'), (6, 'solar5'),
(7, 'iron1'), (7, 'iron2'), (7, 'iron3'), (7, 'iron4'), (7, 'iron5'),
(8, 'quantum1'), (8, 'quantum2'), (8, 'quantum3'), (8, 'quantum4'), (8, 'quantum5'),
(9, 'frost1'), (9, 'frost2'), (9, 'frost3'), (9, 'frost4'), (9, 'frost5'),
(10, 'void1'), (10, 'void2'), (10, 'void3'), (10, 'void4'), (10, 'void5');

-- =========================================
-- 5. CAPITANES
-- =========================================
INSERT INTO Es_capitan (id_equipo, gamertag) VALUES
(1, 'alpha1'),
(2, 'viper1'),
(3, 'nebula1'),
(4, 'titan1'),
(5, 'shadow1'),
(6, 'solar1'),
(7, 'iron1'),
(8, 'quantum1'),
(9, 'frost1'),
(10, 'void1');

-- =========================================
-- 6. SPONSORS
-- =========================================
INSERT INTO Sponsor (nombre, industria, monto) VALUES
('HyperX', 'Tecnología', 12000.00),
('Red Bull', 'Bebidas', 10000.00),
('Adidas Gaming', 'Ropa', 8000.00),
('Intel', 'Hardware', 15000.00),
('Logitech G', 'Periféricos', 9000.00);

-- =========================================
-- 7. INSCRIPCIONES
-- Torneo 1 lleno con 8 equipos
-- =========================================
INSERT INTO Inscripcion (id_torneo, id_equipo) VALUES
(1, 1), (1, 2), (1, 3), (1, 4),
(1, 5), (1, 6), (1, 7), (1, 8),

(2, 1), (2, 2), (2, 9), (2, 10),
(2, 3), (2, 4), (2, 5), (2, 6),

(3, 3), (3, 4), (3, 5), (3, 6);

-- =========================================
-- 8. AUSPICIOS
-- =========================================
INSERT INTO Auspicia_a (nombre_sponsor, id_torneo) VALUES
('HyperX', 1),
('Red Bull', 1),
('Intel', 1),
('Logitech G', 1),

('HyperX', 2),
('Adidas Gaming', 2),
('Red Bull', 2),

('Intel', 3),
('Logitech G', 3),
('Adidas Gaming', 3);

-- =========================================
-- 9. PARTIDAS
-- Torneo 1 completo:
-- fase de grupos (12)
-- semifinales (2)
-- final (1)
-- =========================================
INSERT INTO Partidas (
    id_partida, id_torneo, id_equipo_a, id_equipo_b,
    puntaje_a, puntaje_b, fase, fecha, hora
) VALUES

-- TORNEO 1
-- Grupo A: equipos 1,2,3,4
(1, 1, 1, 2, 13, 8, 'grupos', '2026-06-01', '10:00'),
(2, 1, 1, 3, 13, 11, 'grupos', '2026-06-01', '13:00'),
(3, 1, 1, 4, 9, 13, 'grupos', '2026-06-01', '16:00'),
(4, 1, 2, 3, 13, 10, 'grupos', '2026-06-02', '10:00'),
(5, 1, 2, 4, 7, 13, 'grupos', '2026-06-02', '13:00'),
(6, 1, 3, 4, 13, 6, 'grupos', '2026-06-02', '16:00'),

-- Grupo B: equipos 5,6,7,8
(7, 1, 5, 6, 13, 9, 'grupos', '2026-06-03', '10:00'),
(8, 1, 5, 7, 13, 7, 'grupos', '2026-06-03', '13:00'),
(9, 1, 5, 8, 11, 13, 'grupos', '2026-06-03', '16:00'),
(10, 1, 6, 7, 13, 10, 'grupos', '2026-06-04', '10:00'),
(11, 1, 6, 8, 8, 13, 'grupos', '2026-06-04', '13:00'),
(12, 1, 7, 8, 6, 13, 'grupos', '2026-06-04', '16:00'),

-- Semifinales
(13, 1, 4, 5, 13, 9, 'semifinal', '2026-06-06', '15:00'),
(14, 1, 8, 1, 10, 13, 'semifinal', '2026-06-06', '18:00'),

-- Final
(15, 1, 4, 1, 12, 13, 'final', '2026-06-07', '20:00')

-- TORNEO2
-- Grupo A: equipos 1, 2, 9, 10
(16, 2, 1, 2, 13, 8, 'grupos', '2026-07-10', '10:00'),
(17, 2, 1, 9, 13, 11, 'grupos', '2026-07-10', '13:00'),
(18, 2, 1, 10, 9, 13, 'grupos', '2026-07-10', '16:00'),
(19, 2, 2, 9, 13, 10, 'grupos', '2026-07-11', '10:00'),
(20, 2, 2, 10, 7, 13, 'grupos', '2026-07-11', '13:00'),
(21, 2, 9, 10, 13, 6, 'grupos', '2026-07-11', '16:00'),

-- Grupo B: equipos 3, 4, 5, 6
(22, 2, 3, 4, 13, 9, 'grupos', '2026-07-12', '10:00'),
(23, 2, 3, 5, 13, 7, 'grupos', '2026-07-12', '13:00'),
(24, 2, 3, 6, 11, 13, 'grupos', '2026-07-12', '16:00'),
(25, 2, 4, 5, 13, 10, 'grupos', '2026-07-13', '10:00'),
(26, 2, 4, 6, 8, 13, 'grupos', '2026-07-13', '13:00'),
(27, 2, 5, 6, 6, 13, 'grupos', '2026-07-13', '16:00'),

-- Semifinales (Torneo 2)
(28, 2, 10, 4, 13, 9, 'semifinal', '2026-07-14', '15:00'),
(29, 2, 6, 1, 10, 13, 'semifinal', '2026-07-14', '18:00'),

-- Final (Torneo 2)
(30, 2, 10, 1, 12, 13, 'final', '2026-07-15', '20:00');

-- =========================================
-- 10. ESTADÍSTICAS INDIVIDUALES
-- 10 filas por partida
-- =========================================
INSERT INTO Estadisticas_individuales (id_partida, gamertag, ko, restarts, asists)
SELECT
    p.id_partida,
    pe.gamertag,
    CASE
        WHEN pe.id_equipo = p.id_equipo_a THEN (RIGHT(pe.gamertag, 1)::INTEGER + p.id_partida) % 7
        ELSE (RIGHT(pe.gamertag, 1)::INTEGER + p.id_partida + 1) % 7
    END AS ko,
    CASE
        WHEN pe.id_equipo = p.id_equipo_a THEN (RIGHT(pe.gamertag, 1)::INTEGER + p.id_partida) % 4
        ELSE (RIGHT(pe.gamertag, 1)::INTEGER + p.id_partida + 2) % 4
    END AS restarts,
    CASE
        WHEN pe.id_equipo = p.id_equipo_a THEN (RIGHT(pe.gamertag, 1)::INTEGER + p.id_partida + 2) % 9
        ELSE (RIGHT(pe.gamertag, 1)::INTEGER + p.id_partida + 3) % 9
    END AS asists
FROM Partidas p
JOIN Pertenece_a pe
    ON pe.id_equipo IN (p.id_equipo_a, p.id_equipo_b)
ORDER BY p.id_partida, pe.id_equipo, pe.gamertag;

-- =========================================
-- 11. AJUSTE DE SECUENCIAS
-- =========================================
SELECT setval(pg_get_serial_sequence('torneos', 'id_torneo'), COALESCE((SELECT MAX(id_torneo) FROM Torneos), 1));
SELECT setval(pg_get_serial_sequence('equipos', 'id_equipo'), COALESCE((SELECT MAX(id_equipo) FROM Equipos), 1));
SELECT setval(pg_get_serial_sequence('partidas', 'id_partida'), COALESCE((SELECT MAX(id_partida) FROM Partidas), 1));

COMMIT;