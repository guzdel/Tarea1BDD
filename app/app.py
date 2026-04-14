from flask import Flask, render_template, request, flash
import psycopg2
import os

app = Flask(__name__)

def conectar_a_bdd():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        port=os.environ.get('DB_PORT', 5432),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD', 'postgres'),
        database=os.environ.get('DB_NAME', 'tarea1')
    )


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/torneos/", methods=['GET'])
def torneos():

    # argumentos por default
    torneos = None
    torneo_seleccionado = None
    tabla_grupos = None
    partidas = None
    equipos_inscritos = None
    sponsors = None

    conn = conectar_a_bdd()
    cur = conn.cursor()

    cur.execute('SELECT * FROM Torneos')
    torneos = cur.fetchall()
    torneos = [{
                "id_torneo": f[0],
                "nombre": f[1],
                "videojuego": f[2],
                "fecha_inicio": f[3],
                "fecha_fin": f[4]
            } for f in torneos]


    torneo_id = request.args.get('torneo_id', default=None, type=int)

    if torneo_id != None:

        # info general del torneo seleccionado
        cur.execute("""SELECT * FROM Torneos WHERE id_torneo = %s""", (torneo_id,))
        ts = cur.fetchone()
        torneo_seleccionado = {
                "id_torneo": ts[0],
                "nombre": ts[1],
                "videojuego": ts[2],
                "fecha_inicio": ts[3],
                "fecha_fin": ts[4]
            }

        # Partidas del torneo
        cur.execute("""SELECT p.fecha, e1.nombre, p.puntaje_a, p.puntaje_b, e2.nombre
            FROM Partidas p
            JOIN Equipos e1 ON p.id_equipo_a = e1.id_equipo
            JOIN Equipos e2 ON p.id_equipo_b = e2.id_equipo
            WHERE p.id_torneo = %s
            ORDER BY p.fecha, p.hora""", (torneo_id,))
        partidas = cur.fetchall()
        partidas = [
                {
                    "fecha": f[0],
                    "equipo_a": f[1],
                    "marcador_a": f[2],
                    "marcador_b": f[3],
                    "equipo_b": f[4]
                }
                for f in partidas]

        # Equipos inscritos
        cur.execute("""SELECT e.nombre 
                    FROM inscripcion i JOIN equipos e ON i.id_equipo = e.id_equipo
                    WHERE i.id_torneo = %s""", (torneo_id,))
        equipos_inscritos = [x[0] for x in cur.fetchall()]

        # Sponsors
        cur.execute("""SELECT nombre_sponsor FROM auspicia_a
                    WHERE id_torneo = %s""", (torneo_id,))
        sponsors = [x[0] for x in cur.fetchall()]

        # Tabla posiciones
        cur.execute("""SELECT e.nombre, COUNT(*) AS jugadas,
                    SUM(CASE WHEN sub.gf > sub.gc THEN 1 ELSE 0 END) AS ganadas,
                    SUM(CASE WHEN sub.gf = sub.gc THEN 1 ELSE 0 END) AS empatadas,
                    SUM(CASE WHEN sub.gf < sub.gc THEN 1 ELSE 0 END) AS perdidas,
                    SUM(CASE WHEN sub.gf > sub.gc THEN 3 WHEN sub.gf = sub.gc THEN 1 ELSE 0 END) AS puntos
                    FROM (SELECT p.id_equipo_a AS id_equipo, p.puntaje_a AS gf, p.puntaje_b AS gc
                    FROM Partidas p WHERE p.id_torneo = %s AND p.fase = 'grupos'
                    UNION ALL
                    SELECT
                        p.id_equipo_b AS id_equipo,
                        p.puntaje_b AS gf,
                        p.puntaje_a AS gc
                    FROM Partidas p
                    WHERE p.id_torneo = %s
                    AND p.fase = 'grupos') AS sub
                    JOIN Equipos e ON sub.id_equipo = e.id_equipo
                    GROUP BY e.id_equipo, e.nombre
                    ORDER BY puntos DESC, ganadas DESC, e.nombre ASC
                    """, (torneo_id, torneo_id))

        tabla_grupos = [{"equipo": f[0],
                          "jugadas": f[1],
                          "ganadas": f[2],
                          "empatadas": f[3],
                          "perdidas": f[4],
                          "puntos": f[5]} for f in cur.fetchall()]

    cur.close()
    conn.close()
    return render_template("torneos.html",
        torneos=torneos,
        torneo_seleccionado=torneo_seleccionado,
        partidas=partidas,
        tabla_grupos=tabla_grupos,
        equipos_inscritos=equipos_inscritos,
        sponsors=sponsors)

# INSCRIPCIÓN
@app.route('/inscripcion', methods=['GET', 'POST'])
def inscribir():
    torneos = None
    equipos = None
    error_message = None
    success_message = None
    torneo_seleccionado_id = None
    equipo_seleccionado_id = None
    cupos_torneo = None

    conn = conectar_a_bdd()
    cur = conn.cursor()
    if request.method == 'POST':
        torneo_seleccionado_id = request.form.get("torneo_id", type=int)
        equipo_seleccionado_id = request.form.get("equipo_id", type=int)

        if torneo_seleccionado_id != None and equipo_seleccionado_id != None:

            # max
            cur.execute("""SELECT max_equipos FROM Torneos
                        WHERE id_torneo = %s""", (torneo_seleccionado_id, ))
            max_inscripcion = cur.fetchone()[0]

            # actuales
            cur.execute("""SELECT id_equipo FROM inscripcion WHERE
                        id_torneo = %s""", (torneo_seleccionado_id, ))
            inscritos_actuales = [x[0] for x in cur.fetchall()]
            n_actuales = len(inscritos_actuales)

            if max_inscripcion > n_actuales and equipo_seleccionado_id not in inscritos_actuales:
                try:
                    cur.execute("""
                    INSERT INTO Inscripcion (id_torneo, id_equipo)
                    VALUES (%s, %s)
                """, (torneo_seleccionado_id, equipo_seleccionado_id))
                    conn.commit()
                    success_message = '200'
                except Exception as e:
                    error_message = f"No se pudo realizar la inscripción: {e}"
            else:
                error_message = f"No se pudo realizar la inscripción"
        else:
            error_message = f"No se pudo realizar la inscripción"

    cur.execute('SELECT * FROM Torneos')
    torneos = cur.fetchall()
    torneos = [{
                "id_torneo": f[0],
                "nombre": f[1],
                "videojuego": f[2],
                "fecha_inicio": f[3],
                "fecha_fin": f[4]
            } for f in torneos]

    cur.execute('SELECT id_equipo, nombre FROM Equipos')
    filas_equipos = cur.fetchall()
    equipos = [{
        "id_equipo": f[0],
        "nombre": f[1]
    } for f in filas_equipos]

    cur.execute("""
        SELECT
            t.nombre,
            COUNT(i.id_equipo) AS inscritos_actuales,
            t.max_equipos
        FROM Torneos t
        LEFT JOIN Inscripcion i ON t.id_torneo = i.id_torneo
        GROUP BY t.id_torneo, t.nombre, t.max_equipos
        ORDER BY t.id_torneo
    """)

    cupos_torneo = [{
        "nombre_torneo": f[0],
        "inscritos_actuales": f[1],
        "max_equipos": f[2]
    } for f in cur.fetchall()]

    cur.close()
    conn.close()
    return render_template(
        "inscripcion.html",
        torneos=torneos,
        equipos=equipos,
        cupos_torneo=cupos_torneo,
        error_message=error_message,
        success_message=success_message,
        torneo_seleccionado_id=torneo_seleccionado_id,
        equipo_seleccionado_id=equipo_seleccionado_id)

# SPONSORS
@app.route('/sponsors', methods=['GET'])
def mostrar_sponsors():
    videojuego_seleccionado = request.args.get(
        'videojuego_seleccionado', default=None, type=str)
    sponsors = None
    conn = conectar_a_bdd()
    cur = conn.cursor()

    cur.execute("""SELECT DISTINCT videojuego FROM torneos""")
    videojuegos = [x[0] for x in cur.fetchall()]

    if videojuego_seleccionado != None:
        cur.execute("""SELECT s.nombre, s.industria, s.monto
                    FROM Sponsor s
                    JOIN Auspicia_a a
                    ON s.nombre = a.nombre_sponsor
                    JOIN Torneos t
                    ON a.id_torneo = t.id_torneo
                    WHERE t.videojuego = %s""", (videojuego_seleccionado, ))

        sponsors = ({'nombre': x[0], 'industria': x[1], 'monto': x[2]}
                    for x in cur.fetchall())

    cur.close()
    conn.close()
    return render_template("sponsors.html",
                           videojuego_seleccionado=videojuego_seleccionado,
                           sponsors=sponsors,
                           videojuegos=videojuegos)


# BUSQUEDA
@app.route("/busqueda", methods=["GET"])
def busqueda():
    conn = conectar_a_bdd()
    cur = conn.cursor()
    gamertag = request.args.get('gamertag')
    pais = request.args.get('pais')
    nombre_equipo = request.args.get('nombre_equipo')

    if gamertag is None and pais is None and nombre_equipo is None:  # Para el primer request
        cur.execute('SELECT DISTINCT pais FROM jugadores')
        paises = [x[0] for x in cur.fetchall()]
        cur.close()
        conn.close()
        print('Entregando paises para la lista')
        return render_template("busqueda.html", paises=paises)

# BUSQUEDA JUGADORES
    if pais is not None:
        print('gamertag buscado:', type(gamertag))
        if pais != 'todos':
            query = '''SELECT j.gamertag, j.pais, e.nombre AS nombre_equipo,
                        CASE
                            WHEN c.gamertag IS NOT NULL THEN 'Sí'
                            ELSE 'No'
                        END AS es_capitan
                        FROM jugadores j
                        NATURAL JOIN  pertenece_a p
                        JOIN equipos e ON p.id_equipo = e.id_equipo
                        LEFT JOIN es_capitan c ON c.gamertag = j.gamertag
                        WHERE j.gamertag LIKE %(gamertag)s AND j.pais = %(pais)s
                        ORDER BY j.gamertag'''
            cur.execute(query, {'gamertag': '%{}%'.format(gamertag), 'pais': pais})
        else:
            query = '''SELECT j.gamertag, j.pais, e.nombre AS nombre_equipo,
                        CASE
                            WHEN c.gamertag IS NOT NULL THEN 'Sí'
                            ELSE 'No'
                        END AS es_capitan
                        FROM jugadores j
                        NATURAL JOIN  pertenece_a p
                        JOIN equipos e ON p.id_equipo = e.id_equipo
                        LEFT JOIN es_capitan c ON c.gamertag = j.gamertag
                        WHERE j.gamertag LIKE %(gamertag)s
                        ORDER BY j.gamertag'''
            cur.execute(query, {'gamertag': '%{}%'.format(gamertag)})

        jugadores = cur.fetchall()

        jugadores = [{
                    "gamertag": f[0],
                    "pais": f[1],
                    "equipo": f[2],
                    "es_capitan": f[3]} for f in jugadores]
        cur.execute('SELECT DISTINCT pais FROM jugadores')
        paises = [x[0] for x in cur.fetchall()]
        cur.close()
        conn.close()
        return render_template("busqueda.html", resultados=jugadores, paises=paises)

# BUSQUEDA DE EQUIPOS
    if nombre_equipo is not None:
        print(f'equipo buscado: {type(nombre_equipo)}')
        query = '''SELECT e.nombre, e.fecha_creacion
                FROM equipos e
                WHERE UPPER(e.nombre) LIKE UPPER(%(nombre_equipo)s)'''
        cur.execute(query, {'nombre_equipo': '%{}%'.format(nombre_equipo)})
        equipos = cur.fetchall()
        equipos = [{'nombre_equipo': x[0], 'fecha_creacion': x[1]}
                   for x in equipos]
        cur.execute('SELECT DISTINCT pais FROM jugadores')
        paises = [x[0] for x in cur.fetchall()]
        cur.close()
        conn.close()
        print(f'equipos: {equipos}')
        return render_template('busqueda.html',
                               resultados_equipos=equipos, paises=paises)
    else:
        cur.close()
        conn.close()
        return render_template('busqueda.html')

@app.route('/estadisticas', methods=['GET'])
def estadisticas():
    conn = conectar_a_bdd()
    cur = conn.cursor()
    torneo_id = request.args.get('torneo_id')
    equipo_id = request.args.get('equipo_id')
    
    cur.execute('''SELECT nombre, id_equipo
                FROM equipos''')
    equipos = [{'nombre': x[0], 'id_equipo': x[1]} for x in cur.fetchall()]

    cur.execute('''SELECT nombre, id_torneo
                FROM torneos''')
    torneos = [{'nombre': x[0], 'id_torneo': x[1]} for x in cur.fetchall()]

    if (torneo_id is None and equipo_id is None) or (
            not torneo_id and not equipo_id):
        cur.close()
        conn.close()
        return render_template("estadisticas.html",
                               equipos=equipos, torneos=torneos)

    elif torneo_id is not None and torneo_id:
        print('realizando consulta')
        cur.execute('''
            SELECT j.gamertag, eq.nombre, SUM(e.ko) AS "KOs",
                SUM(e.restarts) AS "Restarts",
                SUM(e.asists) AS "Assists",
                ROUND(SUM(e.ko)*1.0/SUM(e.restarts),2) AS "Ratio"
            FROM jugadores j, estadisticas_individuales e,
                partidas pex, pertenece_a per, equipos eq
            WHERE j.gamertag=per.gamertag 
                AND per.id_equipo=eq.id_equipo
                AND j.gamertag=e.gamertag
                AND e.id_partida=pex.id_partida
                AND pex.id_torneo=%(torneo_id)s
                AND j.gamertag IN (
                    SELECT j.gamertag
                    FROM jugadores j, estadisticas_individuales e,
                    partidas pin
                    WHERE j.gamertag=e.gamertag 
                        AND e.id_partida=pin.id_partida 
                        AND pin.id_torneo=pex.id_torneo
                    GROUP BY j.gamertag
                    HAVING COUNT(e.id_partida) > 2
                    ORDER BY j.gamertag
                    )
            GROUP BY j.gamertag, eq.nombre
            ORDER BY ROUND(SUM(e.ko)*1.0/SUM(e.restarts),2) DESC
                    ''', {'torneo_id': int(torneo_id)})
        ranking_jugadores = [{
            'gamertag': x[0],
            'equipo': x[1],
            'total_kos': x[2],
            'restarts': x[3],
            'assists': x[4],
            'ratio': x[5]} for x in cur.fetchall()]
        print(torneos)
        for torneo_dict in torneos:
            if torneo_dict['id_torneo'] == int(torneo_id):
                torneo_seleccionado = torneo_dict
        cur.close()
        conn.close()
        return render_template(
            "estadisticas.html", equipos=equipos,
            torneos=torneos, ranking_jugadores=ranking_jugadores)
            torneos=torneos, ranking_jugadores=ranking_jugadores,
            torneo_seleccionado=torneo_seleccionado)

    elif equipo_id is not None and equipo_id:
        cur.execute('''
                    SELECT gamertag, round(AVG(ko),2) AS ko,
                    round(AVG(restarts),2) AS restarts,
                    round(AVG(asists),2) AS asists,
                        CASE
                            WHEN fase='final' OR fase='semifinal' THEN 'Eliminatorias'
                            ELSE 'Grupos'
                        END AS fase2
                    FROM estadisticas_individuales NATURAL JOIN partidas
                    WHERE id_torneo=%s AND (fase='final' OR fase='semifinal')
                    GROUP BY fase2, gamertag
                    ORDER BY gamertag, fase2''', (torneo_id,))



if __name__ == "__main__":
    app.run(debug=True)
