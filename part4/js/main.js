/**
 * Point d'entrée principal de l'application HBnB
 * Ce fichier sert à initialiser les fonctionnalités appropriées
 * en fonction de la page active
 */
// Imports statiques pour toutes les fonctions nécessaires
import { getCookie } from './utils.js';
import { initLoginForm, updateLoginButton } from './auth.js';
import { initPlaceDetailsPage } from './placeDetails.js';
import { initAddReviewPage } from './reviews.js';
import { checkAuthentication, fetchPlaces } from './places.js';

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
  // Vérifier si nous sommes sur la page d'ajout d'avis
  const reviewForm = document.getElementById('review-form');
  const placeDetailsElement = document.getElementById('place-details');
  const loginForm = document.getElementById('login-form');

  if (reviewForm && !placeDetailsElement) {
    // Nous sommes sur la page add_review.html
    initAddReviewPage();
  }
  // Vérifier si nous sommes sur la page de détails d'une place
  else if (placeDetailsElement) {
    initPlaceDetailsPage();
  }
  // Vérifier si nous sommes sur la page de login
  else if (loginForm) {
    initLoginForm();
  }
  else {
    // Page d'accueil ou autres pages
    checkAuthentication();
  }
});