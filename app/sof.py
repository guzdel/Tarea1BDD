from flask import Flask, render_template, request, flash
import psycopg2

app = Flask(__name__)

def conectar_a_bdd():
    conn = psycopg2.connect(
        host="localhost",
        dbname="postgres",
        user="postgres",
        password="postgres"
    )
    return conn


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
@app.route('/inscripcion', methods=['GET', 'PUT'])
def inscribir():
    def inscribir():
    torneos
equipos
error_message
success_message
torneo_seleccionado_id
equipo_seleccionado_id
cupos_torneo



if __name__ == "__main__":
    app.run(debug=True)