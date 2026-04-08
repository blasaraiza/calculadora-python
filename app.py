import os
import pymysql
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# Configuración de Base de Datos
DB_CONFIG = {
    'host': os.environ.get('DB_HOST'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'database': os.environ.get('DB_NAME'),
    'cursorclass': pymysql.cursors.DictCursor
}

def obtener_conexion():
    return pymysql.connect(**DB_CONFIG)

# DISEÑO BOOTSTRAP UNIFICADO
HTML_BOOTSTRAP = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Calculadora Pro</title>
    <link href="https://jsdelivr.net" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; min-height: 100vh; display: flex; align-items: center; padding: 20px 0; }
        .card { border: none; border-radius: 20px; box-shadow: 0 15px 35px rgba(0,0,0,0.05); padding: 2rem; }
        .form-control { padding: 0.8rem; border-radius: 10px; }
        .btn-primary { background-color: #4e73df; border: none; border-radius: 10px; padding: 12px; transition: 0.3s; }
        .btn-primary:hover { background-color: #2e59d9; transform: translateY(-2px); }
        .resultado-box { margin-top: 2rem; border-radius: 15px; padding: 1.5rem; background-color: #eef2ff; border: none; }
        .historial-card { margin-top: 20px; border-radius: 15px; border: none; box-shadow: 0 5px 15px rgba(0,0,0,0.05); }
        .historial-item { border-bottom: 1px solid #f1f1f1; padding: 10px 0; font-size: 0.9rem; }
        .historial-item:last-child { border-bottom: none; }
    </style>
</head>
<body>
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-6 col-lg-5">
            <div class="card">
                <h2 class="text-center mb-5 text-dark fw-bold">Calcular Porcentaje</h2>
                <form method="POST">
                    <div class="mb-4">
                        <label class="form-label fw-semibold">Número base</label>
                        <input type="number" step="any" min="0" name="numero" class="control form-control" placeholder="Ingrese la cantidad" required>
                    </div>
                    <div class="mb-4">
                        <label class="form-label fw-semibold">Porcentaje (%)</label>
                        <input type="number" step="any" min="0" name="porcentaje" class="form-control" placeholder="Ingrese el %" required>
                    </div>
                    <div class="d-grid mt-4 gap-2">
                        <button type="submit" class="btn btn-primary text-white fw-bold">CALCULAR AHORA</button>
                        <a href="/" class="btn btn-light btn-sm text-muted">Limpiar Formulario</a>
                    </div>
                </form>

                {% if resultado %}
                <div class="resultado-box alert alert-primary shadow-sm text-center">
                    <h5 class="text-primary mb-2 small fw-bold text-uppercase">Resultado Obtenido</h5>
                    <small class="text-muted">El {{ p_original }}% de ${{ "{:,.2f}".format(n_original) }} es:</small>
                    <div class="fs-2 fw-bold text-dark mt-1">${{ "{:,.2f}".format(resultado) }}</div>
                </div>
                {% endif %}
            </div>

            <!-- BLOQUE DE HISTORIAL DESDE LA DB -->
            {% if historial %}
            <div class="card historial-card p-4">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h6 class="fw-bold text-secondary mb-0">HISTORIAL (DB)</h6>
                    <a href="/borrar_historial" class="btn btn-outline-danger btn-sm" style="font-size: 0.7rem;">BORRAR TODO</a>
                </div>
                {% for item in historial %}
                <div class="historial-item d-flex justify-content-between">
                    <span>{{ item.p }}% de ${{ "{:,.2f}".format(item.n) }}</span>
                    <span class="fw-bold text-dark">${{ "{:,.2f}".format(item.r) }}</span>
                </div>
                {% endfor %}
            </div>
            {% endif %}

            <p class="text-center mt-4 text-muted small">Python + Flask + Hostinger DB</p>
        </div>
    </div>
</div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    resultado_actual = None
    n_orig = p_orig = 0
    
    if request.method == 'POST':
        n_orig = float(request.form['numero'])
        p_orig = float(request.form['porcentaje'])
        resultado_actual = n_orig + (n_orig * (p_orig / 100))
        
        # Guardar en Hostinger
        try:
            conn = obtener_conexion()
            with conn.cursor() as cursor:
                sql = "INSERT INTO historial (numero, porcentaje, resultado) VALUES (%s, %s, %s)"
                cursor.execute(sql, (n_orig, p_orig, resultado_actual))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error al insertar: {e}")

    # Cargar Historial
    historial_lista = []
    try:
        conn = obtener_conexion()
        with conn.cursor() as cursor:
            cursor.execute("SELECT numero as n, porcentaje as p, resultado as r FROM historial ORDER BY id DESC LIMIT 5")
            historial_lista = cursor.fetchall()
        conn.close()
    except Exception as e:
        print(f"Error al leer: {e}")

    return render_template_string(HTML_BOOTSTRAP, 
                                  resultado=resultado_actual, 
                                  n_original=n_orig, 
                                  p_original=p_orig, 
                                  historial=historial_lista)

@app.route('/borrar_historial')
def borrar_historial():
    try:
        conn = obtener_conexion()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM historial")
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error al borrar: {e}")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
