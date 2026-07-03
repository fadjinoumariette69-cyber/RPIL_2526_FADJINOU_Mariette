document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("formRecherche");
  const resultatsSection = document.getElementById("resultats");

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const matiere = document.getElementById("matiere").value.trim();
    const horaire = document.getElementById("horaire").value.trim();
    const filiere = document.getElementById("filiere").value.trim();

    if (!matiere || !horaire) {
      afficherMessage("Merci de renseigner au moins une matière et un horaire.", "erreur");
      return;
    }

    afficherChargement();

    try {
      const mentors = await rechercherMentors({ matiere, horaire, filiere });
      afficherResultats(mentors);
    } catch (error) {
      console.error("Erreur lors de la recherche de mentors :", error);
      afficherMessage("Une erreur est survenue lors de la recherche. Veuillez réessayer.", "erreur");
    }
  });

  /**
   * Envoie les critères de recherche au backend et retourne la liste des mentors compatibles.
   * @param {{matiere: string, horaire: string, filiere: string}} criteres
   * @returns {Promise<Array>}
   */
  async function rechercherMentors(criteres) {
    const reponse = await fetch("/api/match", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(criteres)
    });

    if (!reponse.ok) {
      throw new Error(`Erreur serveur : ${reponse.status}`);
    }

    const donnees = await reponse.json();
    return donnees.mentors || [];
  }

  /**
   * Affiche un indicateur de chargement pendant la recherche.
   */
  function afficherChargement() {
    resultatsSection.innerHTML = `
      <div class="etat-recherche">
        <p>Recherche des mentors compatibles en cours...</p>
      </div>
    `;
  }

  /**
   * Affiche un message simple (erreur ou information) dans la zone de résultats.
   * @param {string} texte
   * @param {"erreur"|"info"} type
   */
  function afficherMessage(texte, type) {
    resultatsSection.innerHTML = `
      <div class="etat-recherche ${type === "erreur" ? "etat-erreur" : "etat-info"}">
        <p>${texte}</p>
      </div>
    `;
  }

  /**
   * Construit et affiche les cartes de résultats à partir de la liste de mentors.
   * @param {Array<Object>} mentors
   */
  function afficherResultats(mentors) {
    if (!mentors || mentors.length === 0) {
      afficherMessage("Aucun mentor compatible trouvé pour ces critères. Essayez d'élargir votre recherche.", "info");
      return;
    }

    const cartesHTML = mentors
      .map((mentor) => construireCarteMentor(mentor))
      .join("");

    resultatsSection.innerHTML = `
      <h2 class="resultats-titre">Mentors compatibles (${mentors.length})</h2>
      <div class="resultats-liste">
        ${cartesHTML}
      </div>
    `;
  }

  /**
   * Génère le HTML d'une carte mentor à partir des données renvoyées par le backend.
   * @param {Object} mentor
   * @returns {string}
   */
  function construireCarteMentor(mentor) {
    const matieresCommunes = Array.isArray(mentor.matieres_communes)
      ? mentor.matieres_communes.join(", ")
      : mentor.matieres_communes;

    return `
      <article class="carte-mentor">
        <div class="carte-mentor-entete">
          <h3>${echapperHTML(mentor.nom)}</h3>
          <span class="score-badge">${mentor.score}%</span>
        </div>
        <p><strong>Matières en commun :</strong> ${echapperHTML(matieresCommunes)}</p>
        <p><strong>Disponibilités :</strong> ${echapperHTML(mentor.disponibilites)}</p>
        <p><strong>Format :</strong> ${echapperHTML(mentor.format)}</p>
      </article>
    `;
  }

  /**
   * Échappe les caractères HTML sensibles pour éviter toute injection dans le DOM.
   * @param {string} texte
   * @returns {string}
   */
  function echapperHTML(texte) {
    if (texte === undefined || texte === null) return "";
    const div = document.createElement("div");
    div.textContent = texte;
    return div.innerHTML;
  }
});