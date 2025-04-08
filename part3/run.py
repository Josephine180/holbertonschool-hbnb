from app import create_app
from flask_cors import CORS
from app.extensions import db
from flask import request

app = create_app()
CORS(app, supports_credentials=True, origins="http://localhost:5500", methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"])

@app.before_request
def handle_preflight():
    if request.method == 'OPTIONS':
        return '', 200

# Ceci crée toutes les tables si elles n'existent pas
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
