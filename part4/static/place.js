// place.js
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
// Fonction pour extraire l'ID de la place à partir de l'URL
function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  const id = params.get('id');  // Récupère l'ID à partir des paramètres de l'URL
  console.log('ID extrait de l\'URL:', id);

  if (!id) {
    console.error('Aucun ID trouvé dans l\'URL');
    return null;  // Retourne null si l'ID n'est pas valide
  }

  return id;
}

// Fonction pour récupérer les détails d'une place
async function fetchPlaceDetails(token, placeId) {
  try {
    const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (response.ok) {
      const place = await response.json();
      displayPlaceDetails(place);  // Affiche les détails du lieu
    } else {
      console.error('Erreur lors de la récupération des détails du lieu:', response.statusText);
    }
  } catch (error) {
    console.error('Erreur de requête:', error);
  }
}

// Fonction pour afficher les détails du lieu dans la page
function displayPlaceDetails(place) {
  const placeDetailsSection = document.getElementById('places-list');

  if (!placeDetailsSection) {
    console.error("L'élément pour afficher les détails n'a pas été trouvé.");
    return;
  }

  const reviewsHTML = place.reviews && place.reviews.length
    ? place.reviews.map(r => `<li><strong>${r.user}:</strong> ${r.text} (${r.rating}/5)</li>`).join('')
    : '<li>Aucune review pour le moment.</li>';

  placeDetailsSection.innerHTML = `
    <h1>${place.title}</h1>
    <p><strong>Description:</strong> ${place.description}</p>
    <p><strong>Price:</strong> $${place.price}</p>
    <p><strong>Amenities:</strong> ${place.amenities.join(', ')}</p>
    <p><strong>Reviews:</strong></p>
    <ul>${reviewsHTML}</ul>
  `;
}


async function fetchPlaceReviews(token, placeId) {
  try {
    const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}/reviews`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (response.ok) {
      const review = await response.json();
      displayPlaceReviews(review);  // Affiche les détails du lieu
    } else {
      console.error('Erreur lors de la récupération des détails du lieu:', response.statusText);
    }
  } catch (error) {
    console.error('Erreur de requête:', error);
  }
}

function displayPlaceReviews(reviews) {
  reviewsList.innerHTML = 
  `
  <h1> ${reviews.title} </h1>
  <p><strong>Review</strong> ${reviews.description}</p>
    <ul>
      ${place.reviews.map(review => `<li>${review}</li>`).join('')}
    </ul>
  `
}

// Fonction pour vérifier l'authentification et récupérer les détails de la place
document.addEventListener('DOMContentLoaded', () => {
  const placeId = getPlaceIdFromURL();  // Récupère l'ID de la place depuis l'URL
  const token = getCookie('token');     // Récupère le token depuis le cookie

  if (placeId && token) {
    fetchPlaceDetails(token, placeId);  // Appel pour récupérer et afficher les détails du lieu
    fetchPlaceReviews(token, placeId)
  }
});
