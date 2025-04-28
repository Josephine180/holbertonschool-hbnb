/**
 * Fonctions liées à l'affichage et à la gestion des places
 * Affichage de la liste, filtrage par prix, etc.
 */
import { getCookie } from './utils.js';
import { updateLoginButton, API_BASE_URL } from './auth.js';

/**
 * Vérifie l'authentification et initialise l'affichage en conséquence
 */
function checkAuthentication() {
  const token = getCookie('token');

  // Mettre à jour le bouton de connexion
  updateLoginButton(token);

  // Récupérer les places (avec ou sans token)
  fetchPlaces(token);
}

/**
 * Récupère la liste des places depuis l'API
 * @param {string|null} token - Token JWT pour l'authentification (optionnel)
 */
async function fetchPlaces(token) {
  try {
    const headers = {
      'Content-Type': 'application/json'
    };

    // Ajouter le token d'authentification si disponible
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE_URL}/api/v1/places/`, {
      method: 'GET',
      headers: headers
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const placesData = await response.json();

    // Stocker les données pour le filtrage ultérieur
    window.allPlaces = placesData;

    // Afficher les places et initialiser le filtre de prix
    displayPlaces(placesData);
    initializePriceFilter();
  } catch (error) {
    console.error('Error fetching places:', error);
    const placesListElement = document.getElementById('places-list');
    if (placesListElement) {
      placesListElement.innerHTML = `<p>Unable to load places. Please try again later.</p>`;
    }
  }
}

/**
 * Affiche la liste des places dans l'interface
 * @param {Array} places - Liste des places à afficher
 */
function displayPlaces(places) {
  const placesListElement = document.getElementById('places-list');
  if (!placesListElement) return;

  // Conserver le titre de la section
  const headerElement = placesListElement.querySelector('h2');
  placesListElement.innerHTML = '';
  if (headerElement) {
    placesListElement.appendChild(headerElement);
  }

  // Afficher un message si aucune place n'est disponible
  if (!places || places.length === 0) {
    placesListElement.innerHTML += '<p>No places available at the moment.</p>';
    return;
  }

  // Créer les cartes pour chaque place
  places.forEach((place, index) => {
    // Distribuer les images entre les différentes places (1-5)
    const imageIndex = (index % 5) + 1;

    const placeElement = document.createElement('div');
    placeElement.className = 'place-card';
    placeElement.dataset.price = place.price;

    placeElement.innerHTML = `
      <img src="/images/${place.id}.jpg" alt="${place.title}">
      <h3>${place.title}</h3>
      <p>$${place.price} per night</p>
      <a href="place.html?id=${place.id}" class="details-button" id="view-details">View Details</a>
    `;

    placesListElement.appendChild(placeElement);
  });
}

/**
 * Initialise le filtre de prix avec les options
 */
function initializePriceFilter() {
  const priceFilter = document.getElementById('price-filter');
  if (!priceFilter) return;

  priceFilter.innerHTML = '';

  // Options de filtrage de prix
  const options = [
    { value: 'all', text: 'All Prices' },
    { value: '10', text: 'Up to $10' },
    { value: '50', text: 'Up to $50' },
    { value: '100', text: 'Up to $100' }
  ];

  // Créer les options du select
  options.forEach(option => {
    const optionElement = document.createElement('option');
    optionElement.value = option.value;
    optionElement.textContent = option.text;
    priceFilter.appendChild(optionElement);
  });

  // Ajouter l'écouteur d'événements pour le filtrage
  priceFilter.addEventListener('change', function () {
    filterPlacesByPrice(this.value);
  });
}

/**
 * Filtre les places par prix maximum
 * @param {string} maxPrice - Prix maximum ou 'all' pour toutes
 */
function filterPlacesByPrice(maxPrice) {
  const places = window.allPlaces;
  if (!places) return;

  if (maxPrice === 'all') {
    displayPlaces(places);
    return;
  }

  const maxPriceValue = parseInt(maxPrice);
  const filteredPlaces = places.filter(place => place.price <= maxPriceValue);
  displayPlaces(filteredPlaces);
}

// Exporter toutes les fonctions
export { checkAuthentication, fetchPlaces, displayPlaces, initializePriceFilter, filterPlacesByPrice };