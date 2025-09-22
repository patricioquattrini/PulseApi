from flask import Flask, jsonify, request
import random
import uuid
from datetime import datetime, timedelta
import hmac
from dotenv import load_dotenv
import os

load_dotenv()

API_TOKEN = os.getenv("API-KEY").encode("utf-8")
app = Flask(__name__)

# Helper function to generate a random alert object.
def generate_random_alert():
    """Generates a single alert with random data."""

    # Randomly select a source and an email.
    sources = ["data breach", "malware"]
    source = random.choice(sources)

    emails = [
        "juan.perez@email.com", "ana.lopez@email.com", "carlos.gomez@email.com", "maria.rodriguez@email.com",
        "pedro.sanchez@email.com", "laura.diaz@email.com", "francisco.hernandez@email.com", "sofia.martin@email.com",
        "david.ruiz@email.com", "elena.moreno@email.com", "javier.jimenez@email.com", "patricia.alonso@email.com",
        "daniel.gutierrez@email.com", "isabel.fernandez@email.com", "sergio.navarro@email.com",
        "clara.castro@email.com", "antonio.ortiz@email.com", "rosa.ortega@email.com", "jose.ramirez@email.com",
        "marta.gil@email.com", "miguel.soto@email.com", "cristina.mendoza@email.com", "rafael.nuñez@email.com",
        "andrea.ramos@email.com", "manuel.torres@email.com", "silvia.vazquez@email.com", "pablo.herrera@email.com",
        "irene.morales@email.com", "vicente.ortega@email.com", "rocio.castillo@email.com", "eduardo.soto@email.com",
        "beatriz.delgado@email.com", "fernando.cruz@email.com", "julia.mendez@email.com", "hector.blanco@email.com",
        "adriana.luna@email.com", "alberto.rios@email.com", "natalia.vega@email.com", "oscar.leon@email.com",
        "eva.ortiz@email.com", "hugo.guzman@email.com", "lorena.chavez@email.com", "ricardo.rojas@email.com",
        "monica.salazar@email.com", "ignacio.escobar@email.com", "diana.perez@email.com", "joaquin.flores@email.com",
        "veronica.bravo@email.com", "gustavo.garcia@email.com", "paola.salas@email.com", "alex.torres@email.com",
        "cecilia.ramirez@email.com", "benjamin.jimenez@email.com", "karla.alvarez@email.com", "felipe.soto@email.com",
        "melissa.lopez@email.com", "gaston.hernandez@email.com", "sofia.gonzalez@email.com", "roberto.castro@email.com",
        "camila.moreno@email.com", "matias.navarro@email.com", "daniela.diaz@email.com", "emilio.martin@email.com",
        "alejandra.ruiz@email.com", "maximiliano.gutierrez@email.com", "valeria.sanchez@email.com",
        "esteban.fernandez@email.com", "gabriela.rodriguez@email.com", "agustin.gomez@email.com",
        "marina.lopez@email.com", "facundo.soto@email.com", "romina.diaz@email.com", "nicolas.torres@email.com",
        "celeste.vazquez@email.com", "lucas.perez@email.com", "luana.sanchez@email.com", "santiago.gonzalez@email.com",
        "valentina.hernandez@email.com", "tomas.fernandez@email.com", "juana.rodriguez@email.com",
        "federico.gomez@email.com", "ximena.diaz@email.com", "leandro.lopez@email.com", "belen.rodriguez@email.com",
        "gonzalo.sanchez@email.com", "micaela.martin@email.com", "cristian.gomez@email.com", "agustina.ruiz@email.com",
        "marcelo.gutierrez@email.com", "paula.soto@email.com", "mauro.hernandez@email.com", "sabrina.diaz@email.com",
        "osvaldo.vazquez@email.com", "giselle.perez@email.com", "ernesto.alonso@email.com", "yanina.morales@email.com",
        "ezequiel.castro@email.com", "romina.gomez@email.com", "sebastian.diaz@email.com", "florencia.lopez@email.com",
        "agustin.rodriguez@email.com"
    ]
    email = random.choice(emails)

    # Generate timestamps for detection and creation, making sure creation is after detection.
    now = datetime.utcnow()
    detected_at = now - timedelta(minutes=random.randint(1, 60), seconds=random.randint(1, 60))
    created_at = detected_at + timedelta(seconds=random.randint(1, 30))

    alert = {
        "id": str(uuid.uuid4()),
        "email": email,
        "source_info": {
            "source": source
        },
        "detected_at": detected_at.isoformat() + "Z",
        "created_at": created_at.isoformat() + "Z"
    }

    # Add severity only if the source is "data breach".
    if source == "data breach":
        severities = ["high", "low"]
        alert["source_info"]["severity"] = random.choice(severities)

    return alert


# Generamos un conjunto de datos grande una sola vez
# para que las paginaciones sean consistentes.
TOTAL_ALERTS = 500
ALL_ALERTS = [generate_random_alert() for _ in range(TOTAL_ALERTS)]
LAST_THROTTLED_TIME: datetime = None
THROTTLE_COOLDOWN_SECONDS = 30 # Time the client must wait after being throttled

# El nuevo endpoint con paginación.
@app.route('/alerts', methods=['GET'])
def get_alerts():
    """
    Returns a paginated list of random alerts, requiring API token authorization.
    """
    global LAST_THROTTLED_TIME

    # 1. Check for API token in the header.
    token = request.headers.get('X-API-Key')
    if not token or not hmac.compare_digest(token.encode('utf-8'), API_TOKEN):
        return jsonify({"error": "Unauthorized: Invalid or missing API token."}), 401

    now = datetime.now()
    # 1. Check persistent throttle state
    # If the client was recently throttled, reject immediately.
    if LAST_THROTTLED_TIME and (now - LAST_THROTTLED_TIME).total_seconds() < THROTTLE_COOLDOWN_SECONDS:
        remaining_time = THROTTLE_COOLDOWN_SECONDS - (now - LAST_THROTTLED_TIME).total_seconds()
        response = jsonify({"error": f"Please wait. You were throttled. Try again in {int(remaining_time)} seconds."})
        response.headers['Retry-After'] = int(remaining_time)
        return response, 429

    # 2. Random Throttling (10% chance of failing)
    if random.random() < 0.1 and (not LAST_THROTTLED_TIME or (now - LAST_THROTTLED_TIME).total_seconds() > 10):
        LAST_THROTTLED_TIME = now
        response = jsonify({"error": "Too Many Requests: API is currently overloaded. Please try again later."})
        response.headers['Retry-After'] = 60 # Suggest the client waits for 60 seconds
        return response, 429

    # 2. If authorized, proceed with pagination logic.
    try:
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 10)), 20)
    except (ValueError, TypeError):
        return jsonify({"error": "Los parámetros 'page' y 'per_page' deben ser enteros."}), 400

    if page < 1:
        page = 1
    if per_page < 1:
        per_page = 10

    start_index = (page - 1) * per_page
    end_index = start_index + per_page

    paginated_alerts = ALL_ALERTS[start_index:end_index]

    response_data = {
        "page": page,
        "per_page": per_page,
        "total_alerts": TOTAL_ALERTS,
        "total_pages": (TOTAL_ALERTS + per_page - 1) // per_page,
        "alerts": paginated_alerts
    }

    return jsonify(response_data)


# Standard entry point for running the Flask app.
if __name__ == '__main__':
    app.run(debug=True) 