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

if __name__ == "__main__":
    app.run(debug=True)