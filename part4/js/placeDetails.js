/**
 * Fonctions liées à l'affichage des détails d'une place
 */
import { getCookie, getUrlParams, showError } from './utils.js';
import { updateLoginButton, API_BASE_URL } from './auth.js';
import { setupReviewForm } from './reviews.js';

/**
 * Initialise la page de détails d'une place
 */
function initPlaceDetailsPage() {
  const token = getCookie('token');
  const params = getUrlParams();
  const placeId = params.id;

  if (!placeId) {
    showError('Place ID is missing in the URL');
    return;
  }

  // Mettre à jour le bouton login/logout
  updateLoginButton(token);

  // Gestion de l'affichage du formulaire d'ajout de revue
  const addReviewSection = document.getElementById('add-review');
  if (addReviewSection) {
    if (!token) {
      // Masquer le formulaire si l'utilisateur n'est pas connecté
      addReviewSection.style.display = 'none';
    } else {
      // Afficher le formulaire et l'initialiser
      addReviewSection.style.display = 'block';
      setupReviewForm(placeId, token);
    }
  }

  // Récupérer et afficher les détails de la place
  fetchPlaceDetails(placeId, token);
}

/**
 * Récupère les détails d'une place depuis l'API
 * @param {string} placeId - ID de la place à récupérer
 * @param {string|null} token - Token JWT pour l'authentification (optionnel)
 */
async function fetchPlaceDetails(placeId, token) {
  try {
    const headers = {
      'Content-Type': 'application/json'
    };

    // Ajouter le token d'authentification si disponible
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
    displayPlaceDetails(placeData);

  } catch (error) {
    console.error('Error fetching place details:', error);
    showError('Failed to load place details. Please try again later.');
  }
}

/**
 * Affiche les détails d'une place dans l'interface
 * @param {Object} place - Données de la place à afficher
 */
function displayPlaceDetails(place) {
  // Section des détails de la place
  const placeInfoElement = document.querySelector('.place-info');
  if (placeInfoElement) {
    // Utiliser une image basée sur l'ID de la place pour avoir une consistance
    const imageIndex = (place.id.length % 5) + 1;
  
    placeInfoElement.innerHTML = `
      <img src="/images/${place.id}.jpg" alt="${place.title}">
      <h2>${place.title}</h2>
      <p><strong>Hosted by Owner ID: </strong>${place.owner_id}</p>
      <p><strong>$${place.price} per night</strong></p>
      <p>${place.description || 'No description available'}</p>
      <br/>
      <hr />
      <h3>Amenities</h3>
      <ul id="amenities-list">
        ${place.amenities && place.amenities.length > 0
        ? place.amenities.map(amenity => `<li>${amenity.name}</li>`).join('')
        : '<li>No amenities listed</li>'}
      </ul>
    `;
  }

  // Section des revues
  const reviewsSection = document.getElementById('reviews');
  if (reviewsSection) {
    // Conserver le titre et le bouton pour ajouter une revue
    const title = reviewsSection.querySelector('h2');
    const addReviewButton = reviewsSection.querySelector('.details-button');

    reviewsSection.innerHTML = '';

    if (title) {
      reviewsSection.appendChild(title);
    }

    // Afficher les revues si disponibles
    if (place.reviews && place.reviews.length > 0) {
      place.reviews.forEach(review => {
        const reviewElement = document.createElement('div');
        reviewElement.className = 'review-card';
        reviewElement.innerHTML = `
          <p><strong>User ID:</strong> ${review.user_id}</p>
          <p>${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}</p>
          <p>${review.text}</p>
        `;
        reviewsSection.appendChild(reviewElement);
      });
    } else {
      // Message si aucune revue n'est disponible
      const noReviewsElement = document.createElement('p');
      noReviewsElement.textContent = 'No reviews yet.';
      reviewsSection.appendChild(noReviewsElement);
    }

    // Ajouter le bouton pour ajouter une revue
    if (addReviewButton) {
      // Mettre à jour le lien avec l'ID de la place
      addReviewButton.href = `add_review.html?id=${place.id}`;
      reviewsSection.appendChild(addReviewButton);
    }
  }
}

export { initPlaceDetailsPage, fetchPlaceDetails, displayPlaceDetails };