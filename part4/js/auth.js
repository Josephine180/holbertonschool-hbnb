
/**
 * Fonctions liées à l'authentification
 * Gestion du login, du token JWT et de l'état de connexion
 */
import { getCookie } from './utils.js';

// URL de base de l'API - à modifier selon votre configuration
const API_BASE_URL = 'http://localhost:5000';

/**
 * Authentifie un utilisateur auprès de l'API
 * @param {string} email - Email de l'utilisateur
 * @param {string} password - Mot de passe de l'utilisateur
 */
async function loginUser(email, password) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
    });

    if (response.ok) {
      const data = await response.json();
      document.cookie = `token=${data.access_token}; path=/`;
      window.location.href = 'index.html';
    } else {
      const errorData = await response.json();
      alert('Login failed: ' + (errorData.error || errorData.message || response.statusText));
    }
  } catch (error) {
    console.error('Login error:', error);
    alert('Login failed: Network error');
  }
}

/**
 * Met à jour l'affichage du bouton de connexion/déconnexion
 * @param {string|null} token - Token JWT si l'utilisateur est connecté
 */
function updateLoginButton(token) {
  const loginButton = document.querySelector('.login-button');
  if (!loginButton) return;

  if (!token) {
    // L'utilisateur n'est pas connecté
    loginButton.textContent = 'Login';
    loginButton.href = 'login.html';
    const newButton = loginButton.cloneNode(true);
    loginButton.replaceWith(newButton);
  } else {
    // L'utilisateur est connecté
    loginButton.textContent = 'Logout';
    loginButton.href = '#';

    const newButton = loginButton.cloneNode(true);
    loginButton.parentNode.replaceChild(newButton, loginButton);

    // Ajouter l'événement de déconnexion
    newButton.addEventListener('click', function (e) {
      e.preventDefault();
      document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
      window.location.href = 'index.html';
    });
  }
}

/**
 * Initialise le formulaire de connexion avec les écouteurs d'événements
 */
function initLoginForm() {
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      try {
        await loginUser(email, password);
      } catch (error) {
        console.error('Login failed:', error);
      }
    });
  }
}

export { loginUser, updateLoginButton, initLoginForm, API_BASE_URL };