from flask import Flask, render_template_string, request

app = Flask(__name__)

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
def home():
    if request.method == 'POST':
        try:
            n = float(request.form['numero'])
            p = float(request.form['porcentaje'])
            # Lógica: Número + (Número * Porcentaje / 100)
            resultado_final = n + (n * (p / 100))
            return render_template_string(HTML_BOOTSTRAP, resultado=resultado_final, n_original=n, p_original=p)
        except:
            return render_template_string(HTML_BOOTSTRAP)
    
    return render_template_string(HTML_BOOTSTRAP)

if __name__ == '__main__':
    app.run(debug=True)
