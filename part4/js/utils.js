/**
 * Fonctions utilitaires utilisées dans toute l'application
 */

/**
 * Récupère un cookie par son nom
 * @param {string} name - Nom du cookie à récupérer
 * @return {string|null} - Valeur du cookie ou null si non trouvé
 */
function getCookie(name) {
  const cookies = document.cookie.split(';');
  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].trim();
    if (cookie.startsWith(name + '=')) {
      return cookie.substring(name.length + 1);
    }
  }
  return null;
}

/**
 * Extrait les paramètres de l'URL
 * @return {Object} - Objet contenant les paramètres de l'URL
 */
function getUrlParams() {
  const params = {};
  const queryString = window.location.search.substring(1);
  const pairs = queryString.split('&');

  for (const pair of pairs) {
    const [key, value] = pair.split('=');
    if (key) {
      params[key] = decodeURIComponent(value || '');
    }
  }

  return params;
}

/**
 * Affiche un message d'erreur à l'utilisateur
 * @param {string} message - Message d'erreur à afficher
 */
function showError(message) {
  const mainElement = document.querySelector('main');
  if (mainElement) {
    mainElement.innerHTML = `<div class="error-message">${message}</div>`;
  } else {
    alert(message);
  }
}

export { getCookie, getUrlParams, showError };