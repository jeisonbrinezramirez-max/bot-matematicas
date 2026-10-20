from flask import Flask, request
import sympy as sp
import re

app = Flask(__name__)
VERIFY_TOKEN = "matematicas123"

def resolver(texto):
    try:
        texto_original = texto
        t = texto.lower().strip()
        x = sp.symbols('x')
        if "=" in t:
            tt = t.replace("resuelve","").replace(":","").strip()
            izq, der = tt.split("=",1)
            eq = sp.Eq(sp.sympify(izq), sp.sympify(der))
            sol = sp.solve(eq, x)
            return f"Solucion: x = {sol}"
        if "factoriza" in t:
            tt = t.replace("factoriza","").replace(":","").strip()
            return f"Factorizado: {sp.factor(sp.sympify(tt))}"
        if "deriva" in t:
            tt = t.replace("deriva","").replace(":","").strip()
            return f"Derivada: {sp.diff(sp.sympify(tt), x)}"
        if re.match(r'^[\d\s\.\+\-\*\/\(\)\^x]+$', t):
            res = sp.sympify(t)
            return f"Resultado: {texto_original} = {res}"
        return "Hola! Soy tu Bot de Matematicas offline. Usa: resuelve: x+2=5"
    except Exception as e:
        return f"No entendi: {texto_original}"

@app.route('/')
def home():
    return "Bot funcionando - Matematicas sin Internet listo"

@app.route('/webhook', methods=['GET'])
def verify():
    token = request.args.get('hub.verify_token')
    chal = request.args.get('hub.challenge')
    if token == VERIFY_TOKEN:
        return chal
    return "error", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    return "ok", 200

@app.route('/resolver')
def resolver_get():
    q = request.args.get('q','')
    return {"pregunta":q,"respuesta":resolver(q)}

app.run(host='0.0.0.0', port=10000)
