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

@app.route("/torneos/")
def torneos():
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

    cur.close()
    conn.close()
    return render_template("torneos.html", torneos=torneos)

@app.route("/busqueda", methods=["GET"])
def busqueda():
    conn = conectar_a_bdd()
    cur = conn.cursor()
    gamertag = request.args.get('gamertag')
    pais = request.args.get('pais')

    if gamertag is None and pais is None:
        cur.execute('SELECT DISTINCT pais FROM jugadores')
        paises = [x[0] for x in cur.fetchall()]
        cur.close()
        conn.close()
        return render_template("busqueda.html", paises=paises)

    query = '''SELECT 
	            j.gamertag,
	            j.pais,
	            e.nombre AS nombre_equipo,
	            CASE
		            WHEN c.gamertag IS NOT NULL THEN 'Sí'
		            ELSE 'No'
	            END AS es_capitan
                FROM jugadores j
                NATURAL JOIN  pertenece_a p
                JOIN equipos e ON p.id_equipo = e.id_equipo
                LEFT JOIN es_capitan c ON c.gamertag = j.gamertag
                WHERE j.gamertag LIKE '%ph%' AND j.pais = 'Chile' '''
    cur.execute(query, {'gamertag': gamertag, 'pais': pais})
    jugadores = cur.fetchall()
    jugadores = [{
                "gamertag": f[0],
                "nombre": f[1],
                "email": f[2],
                "nacimiento": f[3],
                "pais": f[4]
            } for f in jugadores]
    cur.execute('SELECT DISTINCT pais FROM jugadores')
    paises = [x for x in cur.fetchall()]
    cur.close()
    conn.close()
    return render_template("busqueda.html", resultados=jugadores, paises=paises)


if __name__ == "__main__":
    app.run(debug=True)