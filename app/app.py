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
    
    #argumentos por default
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

        #info general del torneo seleccionado
        cur.execute("""SELECT * FROM Torneos WHERE id_torneo = %s""", (torneo_id,))
        ts = cur.fetchone()
        torneo_seleccionado = {
                "id_torneo": ts[0],
                "nombre": ts[1],
                "videojuego": ts[2],
                "fecha_inicio": ts[3],
                "fecha_fin": ts[4]
            }

        #Partidas del torneo
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
                    "equipo_local": f[1],
                    "marcador_local": f[2],
                    "marcador_visitante": f[3],
                    "equipo_visitante": f[4]
                }
                for f in partidas]
        
        #Equipos inscritos
        cur.execute("""SELECT e.nombre 
                    FROM inscripcion i JOIN equipos e ON i.id_equipo = e.id_equipo
                    WHERE i.id_torneo = %s""", (torneo_id,))
        equipos_inscritos = [x[0] for x in cur.fetchall()]

        #Sponsors
        cur.execute("""SELECT nombre_sponsor FROM auspicia_a
                    WHERE id_torneo = %s""", (torneo_id,))
        sponsors = [x[0] for x in cur.fetchall()]

        #Tabla posiciones
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

#INSCRIPCIÓN




@app.route("/busqueda", methods=["GET"])
def busqueda():
    conn = conectar_a_bdd()
    cur = conn.cursor()
    gamertag = request.args.get('gamertag')
    pais = request.args.get('pais')

    if gamertag is None and pais is None:  # Para el primer request
        cur.execute('SELECT DISTINCT pais FROM jugadores')
        paises = [x[0] for x in cur.fetchall()]
        cur.close()
        conn.close()
        return render_template("busqueda.html", paises=paises)
    print('ARGUMENTOS: ',gamertag, pais)
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
                    WHERE j.gamertag LIKE %(gamertag)s AND j.pais = %(pais)s '''
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
                    WHERE j.gamertag LIKE %(gamertag)s '''
        cur.execute(query, {'gamertag': '%{}%'.format(gamertag)})

    jugadores = cur.fetchall()
    jugadores = [{
                "gamertag": f[0],
                "pais": f[1],
                "nombre_equipo": f[2],
                "es_capitan": f[3]} for f in jugadores]
    cur.execute('SELECT DISTINCT pais FROM jugadores')
    paises = [x[0] for x in cur.fetchall()]
    cur.close()
    conn.close()
    return render_template("busqueda.html", resultados=jugadores, paises=paises)


if __name__ == "__main__":
    app.run(debug=True)