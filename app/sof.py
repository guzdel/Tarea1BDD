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

        
            #max
            cur.execute("""SELECT max_equipos FROM Torneos
                        WHERE id_torneo = %s""", (torneo_seleccionado_id, ))
            max_inscripcion = cur.fetchone()[0]
            
            #actuales
            cur.execute("""SELECT id_equipo FROM inscripcion WHERE
                        id_torneo = %s""", (torneo_seleccionado_id, ))
            inscritos_actuales = [x[0] for x in cur.fetchall()]
            n_actuales = len(inscritos_actuales)

            if max_inscripcion > n_actuales and equipo_seleccionado_id not in inscritos_actuales:
                try:
                    cur.execute("""
                                INSERT INTO inscripcion (id_torneo, id_equipo)
                                VALUES (%s, %s)""", (torneo_seleccionado_id, equipo_seleccionado_id))
                    conn.commit()
                    success_message = 'Inscrito con éxito'
                except Exception as e:
                    error_message = f"Error en la base de datos: {e}, No se pudo realizar la inscripción"
            else:
                error_message = f"Error: Se supera el máximo de inscritos o el equipo ya estaba inscrito."
        else:
            error_message = f"Error: No se seleccionó correctamente un equipo y/o torneo"
    
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

@app.route('/sponsors', methods=['GET'])
def mostrar_sponsors():

    videojuego_seleccionado = request.args.get('videojuego_seleccionado', default=None, type=str)
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
        
        sponsors = ({'nombre':x[0], 'industria':x[1], 'monto':x[2]} for x in cur.fetchall())

    cur.close()
    conn.close()
    return render_template("sponsors.html", videojuego_seleccionado=videojuego_seleccionado,
                           sponsors=sponsors,
                           videojuegos=videojuegos)

if __name__ == "__main__":
    app.run(debug=True)