let allPlaces = []; // Déclare une variable pour stocker tous les lieux

document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      try {
        console.log("je passe");
        const response = await fetch('http://localhost:5000/api/v1/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ email, password })
        });

        const data = await response.json();
        if (response.ok) {
          /* stockage token dans cookie */
          document.cookie = `token=${data.access_token}; path=/`;
          /* redirection vers index.html */
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

/* fonction qui recupère le cookie par son nom */
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

console.log(getCookie('token'));

/* fonction pour vérifier l'authentification */
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

/* fonction pour récupérer les données des lieux */
async function fetchPlaces(token) {
  try {
    const response = await fetch('http://localhost:5000/api/v1/places', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (response.ok) {
      const places = await response.json();
      allPlaces = places;  // Stocke tous les lieux dans la variable globale
      console.log(allPlaces);
      displayPlaces(allPlaces);
      populatePriceFilter(allPlaces);
    } else {
      console.error('Erreur récupération des lieux', response.statusText);
    }
  } catch (error) {
    console.error('Erreur lors de la requête pour récupérer les lieux:', error);
  }
}

/* fonction pour afficher les lieux sur la page */
function displayPlaces(places) {
  const placesList = document.getElementById('places-list');
  placesList.innerHTML = '';

  if (!Array.isArray(places) || places.length === 0) {
    console.log("Aucune place disponible");
    return;
  }

  places.forEach(place => {
    console.log("Place:", place);
    if (place.title && place.price) {
      const placeDiv = document.createElement('div');
      placeDiv.classList.add('place-card');
      placeDiv.innerHTML = `
        <h2>${place.title}</h2>
        <p><strong>Price per night:</strong> $${place.price}</p>
        <a href="place.html"><button class="details-button">View Details</button></a>
      `;
      placesList.appendChild(placeDiv);
    } else {
      console.error('Place manque des propriétés nécessaires (title, price)', place);
    }
  });
}

/* Ajouter le filtrage des lieux en fonction du prix */
document.getElementById('price-filter').addEventListener('change', (event) => {
  const selectedPrice = event.target.value;

  const filteredPlaces = selectedPrice === 'All'
    ? allPlaces  // Si 'All' est sélectionné, on montre tous les lieux
    : allPlaces.filter(place => place.price <= selectedPrice);  // Filtrer par prix

  displayPlaces(filteredPlaces);
});

/* Peupler le dropdown des prix */
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

