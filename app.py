from flask import Flask, request, jsonify

app = Flask(__name__)

# Endpoint principale per test
@app.route("/")
def home():
    return "Hello, Flask!"

# Endpoint per ricevere dati
@app.route("/process-data", methods=["POST"])
def process_data():
    # Legge i dati inviati
    data = request.get_json()
    if not data:
        return jsonify({"error": "Nessun dato ricevuto"}), 400

    # Mostra i dati ricevuti nel terminale (per debug)
    print(f"Dati ricevuti: {data}")

    # Risposta di successo
    return jsonify({"status": "success", "message": "Dati ricevuti correttamente"}), 200

if __name__ == "__main__":
    app.run(debug=True)
