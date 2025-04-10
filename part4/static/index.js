
let allPlaces = []; // Déclare une variable pour stocker tous les lieux

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
// Fonction pour récupérer les données des lieux
async function fetchPlaces() {
  try {
    const token = getCookie('token');
    const headers = token ? {'Authorization': `Bearer ${token}`} : {};
    const response = await fetch('http://localhost:5000/api/v1/places', {
      method: 'GET',
      headers: {
        ...headers,
        'Content-Type': 'application/json'
      }
    });

    if (response.ok) {
      const places = await response.json();
      allPlaces = places;  // Stocke tous les lieux dans la variable globale
      displayPlaces(allPlaces);
      populatePriceFilter(allPlaces);
    } else {
      console.error('Erreur récupération des lieux', response.statusText);
    }
  } catch (error) {
    console.error('Erreur lors de la requête pour récupérer les lieux:', error);
  }
}

// Fonction pour afficher les lieux sur la page
function displayPlaces(places) {
  const placesList = document.getElementById('places-list');
  placesList.innerHTML = '';

  if (!Array.isArray(places) || places.length === 0) {
    console.log("Aucune place disponible");
    return;
  }

  places.forEach(place => {
    if (place.title && place.price) {
      const placeDiv = document.createElement('div');
      placeDiv.classList.add('place-card');
      placeDiv.innerHTML = `
        <h2>${place.title}</h2>
        <p><strong>Price per night:</strong> $${place.price}</p>
        <a href="place.html?id=${place.id}"><button class="details-button">View Details</button></a>
      `;
      placesList.appendChild(placeDiv);
    } else {
      console.error('Place manque des propriétés nécessaires (title, price)', place);
    }
  });
}

// Ajouter le filtrage des lieux en fonction du prix
document.getElementById('price-filter').addEventListener('change', (event) => {
  const selectedPrice = event.target.value;

  const filteredPlaces = selectedPrice === 'All'
    ? allPlaces  // Si 'All' est sélectionné, on montre tous les lieux
    : allPlaces.filter(place => place.price <= selectedPrice);  // Filtrer par prix

  displayPlaces(filteredPlaces);
});

// Peupler le dropdown des prix
function populatePriceFilter(places) {
  const priceFilter = document.getElementById('price-filter');
  const priceOptions = [10, 50, 100, 'All'];

  // Ajouter chaque option dans le dropdown
  priceOptions.forEach(option => {
    const optionElement = document.createElement('option');
    optionElement.value = option;
    optionElement.textContent = option === 'All' ? 'All Prices' : `$${option}`;
    priceFilter.appendChild(optionElement);
  });
}

// Fonction pour vérifier l'authentification et récupérer les lieux
document.addEventListener('DOMContentLoaded', () => {
  const token = getCookie('token');
  fetchPlaces();
});
