// login.js

// Fonction pour récupérer le cookie par son nom
function getCookie(name) {
  const cookieString = document.cookie;
  const cookies = cookieString.split(';');
  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].trim();
    if (cookie.startsWith(name + '=')) {
      return cookie.substring(name.length + 1);
    }
  }
  return null;
}

// Fonction pour vérifier l'authentification
function checkAuthentication() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (!token) {
    loginLink.style.display = 'block';
    console.log("Aucun token : on affiche le login");
  } else {
    loginLink.style.display = 'none';
    console.log("Token présent : on cache le login");
    // Fetch places data if the user is authenticated
    fetchPlaces(token);
  }
}

// Fonction de gestion du formulaire de connexion
document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      try {
        const response = await fetch('http://localhost:5000/api/v1/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email, password })
        });

        const data = await response.json();
        if (response.ok) {
          // Stockage du token dans un cookie
          document.cookie = `token=${data.access_token}; path=/`;
          // Redirection vers index.html
          window.location.href = 'index.html';
        } else {
          const errorData = await response.json();
          alert('Login failed: ' + (errorData.message || response.statusText));
        }
      } catch (error) {
        console.error('Erreur lors de la requête:', error);
        alert('Une erreur est survenue. Veuillez réessayer plus tard.');
      }
    });
  }
  checkAuthentication();
});
