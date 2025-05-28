 function toggleSpinner(show) {
    const spinner = document.getElementById('spinner');
    spinner.style.display = show ? 'block' : 'none';
}
    // Base URL de votre API Django Ninja
    // let API_BASE_URL = 'http://127.0.0.1:8000/auth/auth'; // <-- URL mise à jour
       const API_BASE_URL = 'https://gwork.onrender.com/auth/auth'
    // Variables globales pour latitude et longitude
    let latitude, longitude,lat3,lng3;

    // Éléments du DOM
    const messageArea = document.getElementById('message-area');
    const registerTravailleurForm = document.getElementById('register-travailleur-form');
    const registerEmployeurForm = document.getElementById('register-employeur-form');
    const loginForm = document.getElementById('login-form');
    const dashboardSection = document.getElementById('dashboard-section');
    const userProfileInfo = document.getElementById('user-profile-info');
    const adminActions = document.getElementById('admin-actions');
    const userListContainer = document.getElementById('user-list-container');
 document.addEventListener('DOMContentLoaded', () => {
      const map3 = L.map('map3').setView([3.8480, 11.5021], 13);

   // Ajout de la couche de tuiles
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap contributors'
        }).addTo(map3);
    const marker = L.marker([3.8480, 11.5021]).addTo(map3);
     // Ajout de la couche de tuiles
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap contributors'
        }).addTo(map3);

    // Écouter l'événement de clic pour récupérer la latitude et la longitude
    map3.on('click', function(e) {
        lat3 = e.latlng.lat;
        lng3 = e.latlng.lng;
//chatgpt.com/c/6830921b-92f4-800b-8c74-0b265383bf3c
        // Déplacer le marqueur à la nouvelle position
        marker.setLatLng([lat3, lng3]);

  });
});
   document.addEventListener('DOMContentLoaded', () => {
      const map = L.map('map').setView([3.8480, 11.5021], 13);
L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; OpenStreetMap &copy; CARTO',
      subdomains: 'abcd',
      maxZoom: 19
    }).addTo(map);
     // Ajout de la couche de tuiles
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);
    const marker = L.marker([3.8480, 11.5021]).addTo(map);
    

    // Écouter l'événement de clic pour récupérer la latitude et la longitude
    map.on('click', function(e) {
        latitude = e.latlng.lat;
        longitude = e.latlng.lng;

        // Déplacer le marqueur à la nouvelle position
        marker.setLatLng([latitude, longitude]);

        // Afficher les coordonnées dans l'élément HTML
        document.getElementById('coordinates').textContent = `Latitude: ${latitude}, Longitude: ${longitude}`;
    });
});
    // Boutons de navigation
    document.getElementById('show-register-travailleur').addEventListener('click', () => showSection('register-travailleur-form'));
    document.getElementById('show-register-employeur').addEventListener('click', () => showSection('register-employeur-form'));
    document.getElementById('show-login').addEventListener('click', () => showSection('login-form'));
    document.getElementById('show-dashboard').addEventListener('click', () => {
        showSection('dashboard-section');
        fetchUserProfile(); // Charger le profil utilisateur au chargement du tableau de bord
    });
    document.getElementById('logout-btn').addEventListener('click', handleLogout);
    document.getElementById('list-users-btn').addEventListener('click', fetchUserList);

    // --- Fonctions utilitaires UI ---
    function showMessage(message, type = 'success') {
        messageArea.textContent = message;
        messageArea.classList.remove('hidden', 'bg-green-100', 'text-green-800', 'bg-red-100', 'text-red-800', 'bg-yellow-100', 'text-yellow-800');
        if (type === 'success') {
            messageArea.classList.add('bg-green-100', 'text-green-800');
        } else if (type === 'error') {
            messageArea.classList.add('bg-red-100', 'text-red-800');
        } else {
            messageArea.classList.add('bg-yellow-100', 'text-yellow-800');
        }
        setTimeout(() => {
            messageArea.classList.add('hidden');
        }, 5000);
    }

    function showSection(sectionId) {
        // Masquer toutes les sections
        registerTravailleurForm.classList.add('hidden');
        registerEmployeurForm.classList.add('hidden');
        loginForm.classList.add('hidden');
        dashboardSection.classList.add('hidden');
        messageArea.classList.add('hidden'); // Masquer les messages précédents

        // Afficher la section demandée
        document.getElementById(sectionId).classList.remove('hidden');
    }

    function getAuthToken() {
        return localStorage.getItem('access_token');
    }

    function setAuthToken(token) {
        localStorage.setItem('access_token', token);
    }

    function removeAuthToken() {
        localStorage.removeItem('access_token');
    }

 async function handleRegister(event, userType) {
    toggleSpinner(true);
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    // Vérification des coordonnées (latitude et longitude)
    if ((typeof latitude === 'undefined' || typeof longitude === 'undefined') && (typeof lat3 === 'undefined' || typeof lng3 === 'undefined')) {
        showMessage('Veuillez cliquer sur la carte pour sélectionner un emplacement.', 'error');
        toggleSpinner(false);
        return;
    }

    // Ajouter les coordonnées (latitude et longitude)
    if (typeof latitude !== 'undefined' && typeof longitude !== 'undefined') {
        formData.append("latitude", latitude);
        formData.append("longitude", longitude);
    }

    // Ajouter les coordonnées supplémentaires (lat3, lng3)
    if (typeof lat3 !== 'undefined' && typeof lng3 !== 'undefined') {
        formData.append("lat3", lat3);
        formData.append("lng3", lng3);
    }

    // Ajouter la zone de préférence (si disponible)
    if (POLYGON_COORDINATES.length > 0) {
        formData.append("zone_preference", JSON.stringify(POLYGON_COORDINATES));
    }

    // Vérification des boutons radio pour le type de contrat
    const contratRadios = form.querySelectorAll('input[name="type_contrat_souhaite"]');
    
    // Vérifier si les boutons radio existent dans le DOM
    if (contratRadios.length > 0) {
        let contratSelected = false;

        // Vérification si au moins un bouton radio est sélectionné
        contratRadios.forEach(radio => {
            if (radio.checked) {
                contratSelected = true;
            }
        });

        // Si aucun bouton radio n'est sélectionné, afficher un message mais ne bloquer pas l'envoi du formulaire
        if (!contratSelected) {
            console.log('Aucun contrat sélectionné');
        } else {
            // Si un bouton radio est sélectionné, récupérer ses valeurs et les ajouter au formData
            const contratFields = form.querySelectorAll('input[name="type_contrat_souhaite"]:checked');
            const contratValues = Array.from(contratFields).map(input => input.value);
            formData.delete("type_contrat_souhaite");  // Nettoyer les anciennes valeurs
            formData.append("type_contrat_souhaite", contratValues);  // Ajouter les valeurs sélectionnées
        }
    } else {
        // Si les boutons radio n'existent pas dans le DOM, afficher un message de debug
        console.log('Aucun bouton radio "type_contrat_souhaite" trouvé dans le formulaire.');
    }

    // Gestion spécifique pour l'employeur
    if (userType === 'employeur') {
        const logoFile = form.querySelector('input[name="logo_file"]').files[0];
        if (logoFile) {
            formData.append('logo_file', logoFile);
        }

        const secteurActivite = form.querySelector('input[name="secteur_activite"]')?.value;
        const adresseEntreprise = form.querySelector('input[name="adresse_physique_entreprise"]')?.value;
        const siteWeb = form.querySelector('input[name="site_web"]')?.value;
        const presentationEntreprise = form.querySelector('textarea[name="presentation_entreprise"]')?.value;
        const cultureEntreprise = form.querySelector('textarea[name="culture_entreprise"]')?.value;
        const besoinsMainOeuvre = form.querySelector('textarea[name="besoins_main_oeuvre_specifiques"]')?.value;
        const contactRecrutement = form.querySelector('textarea[name="informations_contact_recrutement"]')?.value;

        // Ajouter les informations spécifiques à l'employeur au FormData
        if (secteurActivite) formData.append('secteur_activite', secteurActivite);
        if (adresseEntreprise) formData.append('adresse_physique_entreprise', adresseEntreprise);
        if (siteWeb) formData.append('site_web', siteWeb);
        if (presentationEntreprise) formData.append('presentation_entreprise', presentationEntreprise);
        if (cultureEntreprise) formData.append('culture_entreprise', cultureEntreprise);
        if (besoinsMainOeuvre) formData.append('besoins_main_oeuvre_specifiques', besoinsMainOeuvre);
        if (contactRecrutement) formData.append('informations_contact_recrutement', contactRecrutement);
formData.append('est_entreprise_verifiee', false);
      
    }

    try {
        const response = await fetch(`${API_BASE_URL}/register/${userType}`, {
            method: 'POST',
            body: formData,  // Laissez le navigateur gérer les headers (multipart/form-data)
        });
     
        const data = await response.json();
        toggleSpinner(false);

        if (response.ok) {
            showMessage(`Inscription réussie pour ${data.email}.`, 'success');
            form.reset();
            showSection('login-form');
            showTooltip();
        } else {
            showMessage(`Erreur d'inscription: ${data.detail || JSON.stringify(data)}`, 'error');
        }
    } catch (error) {
        console.error('Erreur réseau ou inattendue:', error);
        showMessage('Une erreur est survenue lors de l\'inscription.', 'error');
    }
}


function showTooltip() {
  const overlay = document.getElementById('tooltip-overlay');
  overlay.classList.remove('hidden');
  document.body.style.overflow = 'hidden'; // Bloque le scroll
}

document.getElementById('close-tooltip').addEventListener('click', () => {
  const overlay = document.getElementById('tooltip-overlay');
  overlay.classList.add('hidden');
  document.body.style.overflow = ''; // Restaure le scroll
});
    registerTravailleurForm.addEventListener('submit', (event) => handleRegister(event, 'travailleur'));
    registerEmployeurForm.addEventListener('submit', (event) => handleRegister(event, 'employeur'));

    async function handleLogin(event) {
    event.preventDefault();
    toggleSpinner(true);

    const formData = new FormData(loginForm);
    const payload = Object.fromEntries(formData.entries());

    try {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });

        let data;
        try {
            data = await response.json();
        } catch (jsonError) {
            console.warn("⚠️ Impossible d’analyser JSON", jsonError);
            data = { detail: 'Erreur inattendue du serveur.' };
        }

        if (response.ok) {
            setAuthToken(data.access_token);
            showMessage('Connexion réussie !', 'success');
            loginForm.reset();
            showSection('dashboard-section');
            fetchUserProfile();
        } else {
            showMessage(`Erreur: ${data.detail || 'Erreur inconnue'}`, 'error');
        }

    } catch (error) {
        console.error('❌ Erreur réseau ou serveur', error);
        showMessage('Erreur réseau.', 'error');
    } finally {
        toggleSpinner(false);
    }
}

    loginForm.addEventListener('submit', handleLogin);

    async function handleLogout() {
        const token = getAuthToken();
        if (!token) {
            showMessage('Vous n\'êtes pas connecté.', 'info');
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/logout`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });

            const data = await response.json();

            if (response.ok) {
                removeAuthToken();
                showMessage('Déconnexion réussie.', 'success');
                showSection('login-form'); // Rediriger vers la page de connexion
            } else {
                showMessage(`Erreur de déconnexion: ${data.detail || JSON.stringify(data)}`, 'error');
            }
        } catch (error) {
            console.error('Erreur réseau ou inattendue:', error);
            showMessage('Une erreur est survenue lors de la déconnexion.', 'error');
        }
    }

    async function fetchUserProfile() {
        const token = getAuthToken();
        if (!token) {
            showMessage('Veuillez vous connecter pour voir votre profil.', 'info');
            showSection('login-form');
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/me`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });

            const data = await response.json();

            if (response.ok) {
                document.getElementById('profile-id').textContent = data.id_utilisateur;
                document.getElementById('profile-email').textContent = data.email;
                document.getElementById('profile-verified').textContent = data.est_email_verifie ? 'Oui' : 'Non';
                document.getElementById('profile-admin').textContent = data.est_administrateur ? 'Oui' : 'Non';

                if (data.est_administrateur) {
                    adminActions.classList.remove('hidden');
                } else {
                    adminActions.classList.add('hidden');
                }
                userListContainer.innerHTML = ''; // Clear previous list
            } else {
                showMessage(`Erreur de chargement du profil: ${data.detail || JSON.stringify(data)}`, 'error');
                removeAuthToken(); // Token invalide, déconnecter l'utilisateur
                showSection('login-form');
            }
        } catch (error) {
            console.error('Erreur réseau ou inattendue:', error);
            showMessage('Une erreur est survenue lors du chargement du profil.', 'error');
            removeAuthToken();
            showSection('login-form');
        }
    }

    async function fetchUserList() {
        const token = getAuthToken();
        if (!token) {
            showMessage('Veuillez vous connecter en tant qu\'administrateur.', 'info');
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/users/`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });

            const data = await response.json();

            if (response.ok) {
                userListContainer.innerHTML = '<h4 class="text-lg font-medium text-gray-700">Liste des utilisateurs:</h4>';
                if (data.users && data.users.length > 0) {
                    data.users.forEach(user => {
                        const userDiv = document.createElement('div');
                        userDiv.className = 'flex items-center justify-between p-2 bg-white rounded-md shadow-sm';
                        userDiv.innerHTML = `
                            <span><strong>${user.email}</strong> (ID: ${user.id_utilisateur}) - Admin: ${user.est_administrateur ? 'Oui' : 'Non'}</span>
                            <button data-user-id="${user.id_utilisateur}" class="delete-user-btn ml-4 px-3 py-1 bg-red-500 text-white rounded-md hover:bg-red-600 transition">Supprimer</button>
                        `;
                        userListContainer.appendChild(userDiv);
                    });
                    // Ajouter les écouteurs d'événements aux boutons de suppression
                    document.querySelectorAll('.delete-user-btn').forEach(button => {
                        button.addEventListener('click', (event) => handleDeleteUser(event.target.dataset.userId));
                    });
                } else {
                    userListContainer.innerHTML += '<p>Aucun utilisateur trouvé.</p>';
                }
            } else {
                showMessage(`Erreur lors du listage des utilisateurs: ${data.detail || JSON.stringify(data)}`, 'error');
            }
        } catch (error) {
            console.error('Erreur réseau ou inattendue:', error);
            showMessage('Une erreur est survenue lors du listage des utilisateurs.', 'error');
        }
    }

    async function handleDeleteUser(userId) {
        if (!confirm(`Êtes-vous sûr de vouloir supprimer l'utilisateur avec l'ID ${userId} ?`)) {
            return; // Annuler la suppression
        }

        const token = getAuthToken();
        if (!token) {
            showMessage('Veuillez vous connecter en tant qu\'administrateur.', 'info');
            return;
        }

        try {
            const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });

            const data = await response.json();

            if (response.ok) {
                showMessage(`Utilisateur ${userId} supprimé avec succès.`, 'success');
                fetchUserList(); // Rafraîchir la liste après suppression
            } else {
                showMessage(`Erreur lors de la suppression de l'utilisateur: ${data.detail || JSON.stringify(data)}`, 'error');
            }
        } catch (error) {
            console.error('Erreur réseau ou inattendue:', error);
            showMessage('Une erreur est survenue lors de la suppression de l\'utilisateur.', 'error');
        }
    }
    // Variable globale pour stocker les coordonnées
        let POLYGON_COORDINATES = [];
        
        // Initialisation de la carte
        const map2 = L.map('map2').setView([3.8480, 11.5021], 15);
        
        // Ajout de la couche de tuiles
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap contributors'
        }).addTo(map2);

        // Variables pour les éléments
        let drawnPolygon = null;
        let isDrawing = false;
        
        // Références aux boutons et éléments
        const drawPolygonButton = document.getElementById('drawPolygon');
        const editPolygonButton = document.getElementById('editPolygon');
        const clearPolygonButton = document.getElementById('clearPolygon');
        const showCoordinatesButton = document.getElementById('showCoordinates');
        const exportCoordinatesButton = document.getElementById('exportCoordinates');
        const coordinatesOutput = document.getElementById('coordinatesOutput');
        const polygonStats = document.getElementById('polygonStats');

        // Fonction pour sauvegarder les coordonnées dans la variable globale
       function savePolygonCoordinates(polygon) {
    if (polygon && polygon.getLatLngs && polygon.getLatLngs().length > 0) {
        const latlngs = polygon.getLatLngs()[0];
        POLYGON_COORDINATES = latlngs.map(latlng => ({
            latitude: parseFloat(latlng.lat.toFixed(6)),
            longitude: parseFloat(latlng.lng.toFixed(6))
        }));
        updateDisplay();
        console.log("Coordonnées sauvegardées dans POLYGON_COORDINATES:", POLYGON_COORDINATES);
    } else {
        POLYGON_COORDINATES = [];
        updateDisplay();
    }
}

map2.on('draw:created', function (e) {
    const type = e.layerType;
    const layer = e.layer;

    if (type === 'polygon') {
        savePolygonCoordinates(layer);
        map2.addLayer(layer);
    }
});


        // Fonction pour mettre à jour l'affichage
        function updateDisplay() {
            if (POLYGON_COORDINATES.length > 0) {
                coordinatesOutput.textContent = JSON.stringify(POLYGON_COORDINATES, null, 2);
                polygonStats.textContent = `Polygone avec ${POLYGON_COORDINATES.length} points`;
                
                // Calculer l'aire approximative
                if (POLYGON_COORDINATES.length >= 3) {
                    const area = calculatePolygonArea(POLYGON_COORDINATES);
                    polygonStats.textContent += ` - Aire: ~${area.toFixed(2)} m²`;
                }
                
                // Activer les boutons
                editPolygonButton.disabled = false;
                clearPolygonButton.disabled = false;
                exportCoordinatesButton.disabled = false;
            } else {
                coordinatesOutput.textContent = "Aucun polygone dessiné.";
                polygonStats.textContent = "Aucun polygone dessiné";
                
                // Désactiver les boutons
                editPolygonButton.disabled = true;
                clearPolygonButton.disabled = true;
                exportCoordinatesButton.disabled = true;
            }
        }

        // Fonction pour calculer l'aire approximative d'un polygone
        function calculatePolygonArea(coordinates) {
            if (coordinates.length < 3) return 0;
            
            let area = 0;
            for (let i = 0; i < coordinates.length; i++) {
                const j = (i + 1) % coordinates.length;
                area += coordinates[i].lat * coordinates[j].lng;
                area -= coordinates[j].lat * coordinates[i].lng;
            }
            return Math.abs(area * 111319.9 * 111319.9 / 2); // Conversion approximative en m²
        }

        // Gestionnaire pour dessiner un polygone
        drawPolygonButton.addEventListener('click', function() {
            if (isDrawing) return;
            
            // Supprimer le polygone existant
            if (drawnPolygon) {
                map2.removeLayer(drawnPolygon);
                drawnPolygon = null;
            }
            
            isDrawing = true;
            drawPolygonButton.disabled = true;
            
            // Créer un nouveau polygone
            const points = [];
            let tempPolygon = null;
            
            // Gestionnaire de clic pour ajouter des points
            function onMapClick(e) {
                points.push([e.latlng.lat, e.latlng.lng]);
                
                // Supprimer le polygone temporaire précédent
                if (tempPolygon) {
                    map2.removeLayer(tempPolygon);
                }
                
                // Créer un polygone temporaire pour la visualisation
                if (points.length >= 3) {
                    tempPolygon = L.polygon(points, {
                        color: 'blue',
                        fillColor: 'lightblue',
                        fillOpacity: 0.5
                    }).addTo(map2);
                } else if (points.length >= 2) {
                    tempPolygon = L.polyline(points, {color: 'blue'}).addTo(map2);
                }
                
                // Marquer les points
                L.circleMarker(e.latlng, {
                    radius: 5,
                    color: 'red',
                    fillColor: 'red',
                    fillOpacity: 1
                }).addTo(map2);
            }
            
            // Gestionnaire de double-clic pour terminer le dessin
            function onMapDoubleClick(e) {
                if (points.length >= 3) {
                    // Supprimer le polygone temporaire
                    if (tempPolygon) {
                        map2.removeLayer(tempPolygon);
                    }
                    
                    // Créer le polygone final
                    drawnPolygon = L.polygon(points, {
                        color: 'green',
                        fillColor: 'lightgreen',
                        fillOpacity: 0.5
                    }).addTo(map2);
                    
                    // Permettre l'édition
                    drawnPolygon.on('click', function() {
                        if (!drawnPolygon.editing.enabled()) {
                            drawnPolygon.editing.enable();
                        }
                    });
                    
                    // Sauvegarder les coordonnées
                    savePolygonCoordinates(drawnPolygon);
                    
                    // Gestionnaire pour les modifications
                    drawnPolygon.on('edit', function() {
                        savePolygonCoordinates(drawnPolygon);
                    });
                }
                
                // Nettoyer
                map2.off('click', onMapClick);
                map2.off('dblclick', onMapDoubleClick);
                isDrawing = false;
                drawPolygonButton.disabled = false;
                
                // Supprimer les marqueurs temporaires
                map2.eachLayer(function(layer) {
                    if (layer instanceof L.CircleMarker && layer !== drawnPolygon) {
                        map2.removeLayer(layer);
                    }
                });
            }
            
            // Attacher les gestionnaires d'événements
            map2.on('click', onMapClick);
            map2.on('dblclick', onMapDoubleClick);
            
            // Instruction pour l'utilisateur
            alert('Cliquez sur la carte pour ajouter des points au polygone. Double-cliquez pour terminer.');
        });

        // Gestionnaire pour modifier le polygone
        editPolygonButton.addEventListener('click', function() {
            if (drawnPolygon) {
                if (drawnPolygon.editing.enabled()) {
                    drawnPolygon.editing.disable();
                    editPolygonButton.textContent = '✏️ Modifier Polygone';
                } else {
                    drawnPolygon.editing.enable();
                    editPolygonButton.textContent = '✅ Terminer Modification';
                }
            }
        });

        // Gestionnaire pour effacer le polygone
        clearPolygonButton.addEventListener('click', function() {
            if (drawnPolygon) {
                map2.removeLayer(drawnPolygon);
                drawnPolygon = null;
                POLYGON_COORDINATES = [];
                updateDisplay();
                editPolygonButton.textContent = '✏️ Modifier Polygone';
            }
        });

        // Gestionnaire pour afficher les coordonnées
        showCoordinatesButton.addEventListener('click', function() {
            if (POLYGON_COORDINATES.length > 0) {
                alert('Coordonnées (stockées dans POLYGON_COORDINATES):\n' + 
                      JSON.stringify(POLYGON_COORDINATES, null, 2));
            } else {
                alert('Aucun polygone dessiné.');
            }
        });

        // Gestionnaire pour exporter les coordonnées
        exportCoordinatesButton.addEventListener('click', function() {
            if (POLYGON_COORDINATES.length > 0) {
                const dataStr = JSON.stringify(POLYGON_COORDINATES, null, 2);
                const dataBlob = new Blob([dataStr], {type: 'application/json'});
                const url = URL.createObjectURL(dataBlob);
                const link = document.createElement('a');
                link.href = url;
                link.download = 'polygon_coordinates.json';
                link.click();
                URL.revokeObjectURL(url);
            }
        });

        // Initialisation de l'affichage
        updateDisplay();

        // Fonction globale pour accéder aux coordonnées depuis la console
        window.getPolygonCoordinates = function() {
            return POLYGON_COORDINATES;
        };

        console.log('Carte initialisée. Variable globale POLYGON_COORDINATES disponible.');
        console.log('Utilisez getPolygonCoordinates() pour accéder aux coordonnées depuis la console.');
  

    // --- Initialisation ---
    // Afficher le formulaire de connexion par défaut au chargement
    showSection('login-form');