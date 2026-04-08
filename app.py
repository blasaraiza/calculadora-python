import os
import json
import pymysql
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# Configura aquí los datos que te da Hostinger
DB_CONFIG = {
    'host': os.environ.get('DB_HOST'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'database': os.environ.get('DB_NAME'),
    'cursorclass': pymysql.cursors.DictCursor
}

def obtener_conexion():
    return pymysql.connect(**DB_CONFIG)

@app.route('/', methods=['GET', 'POST'])
def home():
    resultado_actual = None
    if request.method == 'POST':
        n = float(request.form['numero'])
        p = float(request.form['porcentaje'])
        res = n + (n * (p / 100))
        
        # INSERTAR EN HOSTINGER
        conn = obtener_conexion()
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO historial (numero, porcentaje, resultado) VALUES (%s, %s, %s)"
                cursor.execute(sql, (n, p, res))
            conn.commit()
        finally:
            conn.close()
        resultado_actual = res

    # LEER DE HOSTINGER (Últimos 5)
    historial_lista = []
    conn = obtener_conexion()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT numero as n, porcentaje as p, resultado as r FROM historial ORDER BY id DESC LIMIT 5")
            historial_lista = cursor.fetchall()
    finally:
        conn.close()

    return render_template_string(HTML_MODERNO, resultado=resultado_actual, historial=historial_lista)

@app.route('/borrar_historial')
def borrar_historial():
    conn = obtener_conexion()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM historial")
        conn.commit()
    finally:
        conn.close()
    return redirect(url_for('home'))
    

# Nombre del archivo donde guardaremos los datos
ARCHIVO_DATOS = "historial.txt"

def guardar_en_archivo(nuevo_calculo):
    """Guarda un cálculo al principio del archivo y mantiene solo 5."""
    historial = cargar_historial()
    historial.insert(0, nuevo_calculo)
    historial = historial[:5] # Solo guardamos los últimos 5
    
    with open(ARCHIVO_DATOS, "w") as f:
        for item in historial:
            # Guardamos cada cálculo como una línea de texto tipo JSON
            f.write(json.dumps(item) + "\n")

def cargar_historial():
    """Lee el archivo y devuelve una lista de diccionarios."""
    if not os.path.exists(ARCHIVO_DATOS):
        return []
    
    historial = []
    with open(ARCHIVO_DATOS, "r") as f:
        for linea in f:
            historial.append(json.loads(linea.strip()))
    return historial
# Diseño con Bootstrap 5 y espaciado mejorado
HTML_BOOTSTRAP = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Calculadora Pro</title>
    <link href="https://jsdelivr.net" rel="stylesheet">
    <style>
       body { 
            background-color: #f8f9fa; 
            min-height: 100vh; 
            display: flex; 
            align-items: center; 
        }
        .card { 
            border: none; 
            border-radius: 20px; 
            box-shadow: 0 15px 35px rgba(0,0,0,0.05); 
            padding: 2rem; /* Más espacio interno en la tarjeta */
        }
        .form-control {
            padding: 0.8rem; /* Inputs más altos y cómodos */
            border-radius: 10px;
        }
        .btn-primary { 
            background-color: #4e73df; 
            border: none; 
            border-radius: 10px; 
            padding: 12px; 
            transition: 0.3s;
        }
        .btn-primary:hover { background-color: #2e59d9; transform: translateY(-2px); }
        .resultado-box {
            margin-top: 2.5rem; /* Separación extra para el resultado */
            border-radius: 15px;
            padding: 1.5rem;
        }
    </style>
</head>
<body>
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-5">
            <div class="card">
                <h2 class="text-center mb-5 text-dark fw-bold">Calcular Porcentaje</h2>
                
                <form method="POST">
                    <!-- Separamos el primer grupo -->
                    <div class="mb-4">
                        <label class="form-label fw-semibold">Número base</label>
                        <input type="number" step="any" name="numero" class="form-control" placeholder="Ingrese la cantidad" required>
                    </div>
                    
                    <!-- Separamos el segundo grupo -->
                    <div class="mb-4">
                        <label class="form-label fw-semibold">Porcentaje (%)</label>
                        <input type="number" step="any" name="porcentaje" class="form-control" placeholder="Ingrese el %" required>
                    </div>
                    
                    <!-- Separamos el botón de los inputs -->
                    <div class="d-grid mt-4">
                        <button type="submit" class="btn btn-primary text-white fw-bold">CALCULAR AHORA</button>
                    </div>
                </form>

                {% if resultado %}
                <div class="resultado-box alert alert-primary border-0 shadow-sm animate__animated animate__fadeIn">
                    <h5 class="text-center text-primary mb-3">Resultado Obtenido</h5>
                    <div class="text-center">
                        <small class="text-muted">El {{ p_original }}% de {{ n_original }} es:</small>
                        <div class="fs-2 fw-bold text-dark mt-2">
                            ${{ "{:,.2f}".format(resultado) }}
                        </div>
                    </div>
                </div>
                {% endif %}
                
            </div>
            <p class="text-center mt-4 text-muted small">Python + Flask Local Server</p>
        </div>
    </div>
</div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def homee():
    resultado_actual = None
    if request.method == 'POST':
        n = float(request.form['numero'])
        p = float(request.form['porcentaje'])
        resultado_actual = n + (n * (p / 100))
        
        # Guardamos físicamente en el archivo
        guardar_en_archivo({"n": n, "p": p, "r": resultado_actual})
    
    # Cargamos el historial desde el archivo para mostrarlo
    historial_lista = cargar_historial()
    return render_template_string(HTML_MODERNO, resultado=resultado_actual, historial=historial_lista)

@app.route('/borrar_historial')
def borrar_historiall():
    # Borramos el archivo físico
    if os.path.exists(ARCHIVO_DATOS):
        os.remove(ARCHIVO_DATOS)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
