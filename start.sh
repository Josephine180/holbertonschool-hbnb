#!/bin/bash
# Ce script lance à la fois le serveur backend et le serveur frontend

# Fonction pour arrêter les serveurs lorsque le script est interrompu
cleanup() {
    echo "Arrêt des serveurs..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Attraper les signaux pour arrêter proprement les serveurs
trap cleanup SIGINT SIGTERM

# Vérifier si les dépendances sont installées
if ! python3 -c "import flask, flask_restx, flask_bcrypt, sqlalchemy, flask_sqlalchemy, flask_jwt_extended, flask_cors" 2>/dev/null; then
    echo "Installation des dépendances..."
    pip install -r part3/requirements.txt
    pip install flask-jwt-extended flask-cors
fi

# Créer le dossier d'images s'il n'existe pas
if [ ! -d "part4/images" ]; then
    mkdir -p part4/images
    echo "Dossier d'images créé. N'oubliez pas d'y ajouter des images."
fi

# Lancer le serveur backend (API)
echo "Démarrage du serveur backend..."
cd part3
python3 run.py &
BACKEND_PID=$!
cd ..

# Attendre que le serveur backend soit prêt
sleep 2

# Lancer le serveur frontend (fichiers statiques)
echo "Démarrage du serveur frontend..."
python3 static_server.py &
FRONTEND_PID=$!

echo "================================================"
echo "Application HBnB démarrée!"
echo "- Frontend: http://localhost:8080"
echo "- Backend API: http://localhost:5000/api/v1"
echo "- Documentation API: http://localhost:5000/api/v1/"
echo "- Login admin: admin@example.com / adminpassword"
echo "================================================"
echo "Appuyez sur Ctrl+C pour arrêter les serveurs"

# Attendre que les processus fils se terminent
wait