#!/usr/bin/env python3
"""
Serveur simple pour les fichiers statiques du frontend HBnB
"""
from flask import Flask, send_from_directory
import os
from pathlib import Path

# Chemin absolu vers le dossier part4
frontend_folder = Path(__file__).resolve().parent / 'part4'

app = Flask(__name__, static_folder=str(frontend_folder))

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    print(f"Serveur frontend démarré sur http://localhost:8080")
    print(f"Serveur les fichiers depuis: {frontend_folder}")
    app.run(debug=True, port=8080)