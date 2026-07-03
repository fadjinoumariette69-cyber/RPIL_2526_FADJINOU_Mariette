document.addEventListener('DOMContentLoaded', () => {
    const formulaire = document.getElementById('formulaire-matching');
    const conteneur = document.getElementById('resultats');

    if (!formulaire) return;

    formulaire.addEventListener('submit', (e) => {
        // Bloque impérativement le rechargement de la page
        e.preventDefault(); 

        // Récupération rigoureuse des trois valeurs saisies
        const donnees = {
            matiere: document.getElementById('matiere').value.trim(),
            horaire: document.getElementById('horaire').value.trim(),
            filiere: document.getElementById('filiere').value.trim()
        };

        // Envoi vers le serveur Flask
        fetch('/api/match', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(donnees)
        })
        .then(response => response.json())
        .then(data => {
            if (data.erreur) {
                conteneur.innerHTML = `<div class="alert alert-danger">${data.erreur}</div>`;
                return;
            }

            conteneur.innerHTML = ""; 

            if (!data.mentors || data.mentors.length === 0) {
                conteneur.innerHTML = "<div class='alert alert-warning'>Aucun mentor trouvé dans la plage horaire (± 1h).</div>";
                return;
            }

            // Affichage dynamique sous forme de cartes Bootstrap structurées
            data.mentors.forEach(mentor => {
                const carte = document.createElement('div');
                carte.className = 'card my-3 p-3 shadow-sm';
                
                carte.innerHTML = `
                    <div class="card-body">
                        <h4 class="card-title d-flex justify-content-between align-items-center">
                            ${mentor.nom} 
                            <span class="badge bg-success">${mentor.score}% de compatibilité</span>
                        </h4>
                        <p class="card-text mt-3"><strong>Matières partagées :</strong> ${mentor.matieres_communes.join(', ')}</p>
                        <p class="card-text"><strong>Toutes ses disponibilités :</strong> ${mentor.disponibilites}</p>
                        <p class="card-text"><strong>Format de cours :</strong> <span class="badge bg-secondary">${mentor.format}</span></p>
                    </div>
                `;
                conteneur.appendChild(carte);
            });
        })
        .catch(error => {
            console.error("Erreur Fetch :", error);
            conteneur.innerHTML = "<div class='alert alert-danger'>Erreur critique : connexion impossible au serveur backend.</div>";
        });
    });
});
