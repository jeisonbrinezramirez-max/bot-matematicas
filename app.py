from flask import Flask, request, jsonify
import re
app = Flask(__name__)
VERIFY_TOKEN = "matematicas123"
def resolver(texto):
    try:
        op = texto.lower().replace("cuanto es","").replace("x","*").replace("?","").strip()
        if re.match(r'^[\d\s\.\+\-\*\/\(\)]+$', op):
            res = eval(op)
            return f"Resultado: {op} = {res}"
        return f"Hola! Soy tu Bot de Matematicas. Escribe como 25*4+10. Tu: {texto}"
    except:
        return f"No entendi: {texto}"
@app.route('/')
def home():
    return "Bot funcionando"
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
    return jsonify({"pregunta":q,"respuesta":resolver(q)})
app.run(host='0.0.0.0', port=10000)
