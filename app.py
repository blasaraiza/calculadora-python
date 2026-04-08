import os
import json
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

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

HTML_MODERNO = '''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Calculadora Pro</title>
    <link href="https://jsdelivr.net" rel="stylesheet">
    <style>
        body { background-color: #f0f2f5; min-height: 100vh; padding-top: 50px; }
        .card { border-radius: 15px; border: none; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        .btn-primary { border-radius: 8px; padding: 10px; background-color: #4e73df; border: none; }
        .historial-item { font-size: 0.9rem; border-bottom: 1px solid #eee; padding: 10px 0; }
        .historial-item:last-child { border-bottom: none; }
    </style>
</head>
<body>
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-5">
            <div class="card p-4 mb-4">
                <h3 class="text-center mb-4 fw-bold">📊 Calculadora %</h3>
                <form method="POST">
                    <div class="mb-3">
                        <label class="form-label fw-semibold">Número base</label>
                        <input type="number" step="any" min="0" name="numero" class="form-control" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label fw-semibold">Porcentaje (%)</label>
                        <input type="number" step="any" min="0" name="porcentaje" class="form-control" required>
                    </div>
                    <div class="d-grid gap-2">
                        <button type="submit" class="btn btn-primary fw-bold">CALCULAR</button>
                        <a href="/" class="btn btn-light btn-sm text-muted">Limpiar Formulario</a>
                    </div>
                </form>
                {% if resultado %}
                <div class="alert alert-primary mt-4 text-center">
                    <small class="text-uppercase fw-bold">Resultado</small>
                    <h2 class="fw-bold mb-0">${{ "{:,.2f}".format(resultado) }}</h2>
                </div>
                {% endif %}
            </div>

            {% if historial %}
            <div class="card p-4 shadow-sm">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h6 class="text-uppercase fw-bold text-secondary mb-0">Historial Guardado</h6>
                    <a href="/borrar_historial" class="btn btn-outline-danger btn-sm">BORRAR ARCHIVO</a>
                </div>
                {% for item in historial %}
                <div class="historial-item d-flex justify-content-between">
                    <span>{{ item.p }}% de ${{ "{:,.2f}".format(item.n) }}</span>
                    <span class="fw-bold text-dark">${{ "{:,.2f}".format(item.r) }}</span>
                </div>
                {% endfor %}
            </div>
            {% endif %}
        </div>
    </div>
</div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
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
def borrar_historial():
    # Borramos el archivo físico
    if os.path.exists(ARCHIVO_DATOS):
        os.remove(ARCHIVO_DATOS)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
