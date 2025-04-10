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

document.addEventListener('DOMContentLoaded', () => {
  const reviewForm = document.getElementById('review-form');
  const token = checkAuthentication(); // Check authentication on page load
  const placeId = getPlaceIdFromURL(); // Get place ID from the URL

  if (reviewForm) {
      reviewForm.addEventListener('submit', async (event) => {
          event.preventDefault(); // Prevent default form submission behavior

          // Get review text from the form
          const reviewText = document.getElementById('review-text').value;

          // Call the function to submit the review
          await submitReview(token, placeId, reviewText);
      });
  }
});

async function submitReview(token, placeId, reviewText) {
  const url = `http://localhost:5000/api/v1/places/${placeId}/reviews/`;
  
  const data = {
      text: reviewText,
      rating: 5 
  };

  try {
      const response = await fetch(url, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(data)
      });
      handleResponse(response);
  } catch (error) {
      alert('Erreur lors de l\'ajout du commentaire.');
      console.error(error);
  }
}

function handleResponse(response) {
  if (response.ok) {
      alert('Review ajoutée!');
      document.getElementById('review-text').value = ''; // Reset review text field
  } else {
      alert('Impossible d\'ajouter une review');
  }
}