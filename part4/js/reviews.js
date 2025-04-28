/**
 * Fonctions liées à l'ajout et à l'affichage des revues
 */
import { getCookie, getUrlParams, showError } from './utils.js';
import { updateLoginButton, API_BASE_URL } from './auth.js';

/**
 * Configuration du formulaire d'ajout de revue sur la page des détails
 * @param {string} placeId - ID de la place concernée
 * @param {string} token - Token JWT pour l'authentification
 */
function setupReviewForm(placeId, token) {
  const reviewForm = document.getElementById('review-form');
  if (!reviewForm) return;

  reviewForm.addEventListener('submit', async function (event) {
    event.preventDefault();

    const reviewText = document.getElementById('review-text').value;
    const rating = document.getElementById('rating').value;

    if (!reviewText || !rating) {
      alert('Please fill in all fields');
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/places/${placeId}/reviews`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          text: reviewText,
          rating: parseInt(rating)
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || errorData.message || 'Failed to submit review');
      }

      alert('Review submitted successfully!');
      window.location.reload(); // Rafraîchir la page pour afficher la nouvelle revue

    } catch (error) {
      console.error('Error submitting review:', error);
      alert(error.message || 'Failed to submit review. Please try again.');
    }
  });
}

/**
 * Initialisation de la page d'ajout d'avis
 */
function initAddReviewPage() {
  // Vérifier l'authentification et rediriger si non authentifié
  const token = getCookie('token');
  if (!token) {
    window.location.href = 'index.html';
    return;
  }

  // Mettre à jour le bouton de connexion
  updateLoginButton(token);

  // Récupérer l'ID de la place depuis l'URL
  const params = getUrlParams();
  const placeId = params.id;

  if (!placeId) {
    showError('Place ID is missing in the URL');
    return;
  }

  // Récupérer les détails de la place pour afficher son titre
  fetchPlaceForReview(placeId, token);

  // Configurer le formulaire d'ajout d'avis
  setupAddReviewForm(placeId, token);
}

/**
 * Récupère les informations basiques d'une place pour la page d'ajout de revue
 * @param {string} placeId - ID de la place
 * @param {string} token - Token JWT pour l'authentification
 */
async function fetchPlaceForReview(placeId, token) {
  try {
    const headers = {
      'Content-Type': 'application/json'
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE_URL}/api/v1/places/${placeId}`, {
      method: 'GET',
      headers: headers
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const placeData = await response.json();

    // Mettre à jour le titre de la page avec le nom de la place
    const pageTitle = document.querySelector('main h2');
    if (pageTitle) {
      pageTitle.textContent = `Add a review for : ${placeData.title}`;
    }

  } catch (error) {
    console.error('Error fetching place info:', error);
    showError('Failed to load place information');
  }
}

/**
 * Configuration du formulaire d'ajout d'avis sur la page add_review.html
 * @param {string} placeId - ID de la place concernée
 * @param {string} token - Token JWT pour l'authentification
 */
function setupAddReviewForm(placeId, token) {
  const reviewForm = document.getElementById('review-form');
  if (!reviewForm) return;

  reviewForm.addEventListener('submit', async function (event) {
    event.preventDefault();

    const reviewText = document.getElementById('review').value;
    const rating = document.getElementById('rating').value;

    if (!reviewText || !rating) {
      alert('Please fill in all fields');
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/places/${placeId}/reviews`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          text: reviewText,
          rating: parseInt(rating)
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || errorData.message || 'Failed to submit review');
      }

      alert('Review submitted successfully!');

      // Rediriger vers la page des détails de la place
      window.location.href = `place.html?id=${placeId}`;

    } catch (error) {
      console.error('Error submitting review:', error);
      alert(error.message || 'Failed to submit review. Please try again.');
    }
  });
}

export { setupReviewForm, initAddReviewPage, fetchPlaceForReview, setupAddReviewForm };