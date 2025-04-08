document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');

  if(loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;

      try {
        console.log("je passe");
        const response = await fetch('http://localhost:5000/api/v1/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type' : 'application/json'
          },
          body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        if (response.ok) {
          /*stockage token dans cookie */
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
});