# IFRI MentorLink — Plateforme de Mentorat

**IFRI MentorLink** est une plateforme permet de connecter instantanément les mentorés avec les mentors les plus compatibles en fonction de leurs besoins pédagogiques et de leurs disponibilités.

## Fonctionnalités Clés

L'application repose sur un algorithme intelligent exécuté côté serveur (Back-end) qui respecte strictement les exigences du cahier des charges :
1. **Filtre de compétences** : Exclusion automatique des mentors n'ayant aucune matière demandée en commun avec l'étudiant.
2. **Tolérance Horaire de ± 1 heure** : Seuls les mentors disponibles dans une plage maximale de 60 minutes avant ou après l'heure souhaitée sont proposés.
3. **Calcul de Score de Compatibilité (Sur 100)** :
   * **60 points** basés sur le taux de couverture des matières demandées.
   * **30 points** basés sur la proximité horaire exacte (plus l'écart est faible, plus le score est haut).
   * **10 points** de bonus si la filière du mentor correspond à celle demandée.
4. **Tri Dynamique** : Les profils correspondants sont affichés en temps réel sous forme de cartes, classés du plus compatible au moins compatible.

## Technologies Utilisées

* **Front-end** : HTML, CSS personnalisé, JavaScript (Fetch API pour les requêtes asynchrones), Bootstrap  pour le design adaptatif.
* **Back-end** : Python , Framework Flask (Architecture MVC légère).
* **Base de Données** : MySQL (géré localement via **XAMPP**), interfacé avec Flask-SQLAlchemy et PyMySQL.

## Structure du Projet

Conformément aux normes exigées pour le dépôt, le projet est structuré comme suit :

```text
RPIL_2526_FADJINOU_Mariette/
├── backend/
│   ├── app.py                      # Serveur Flask & Algorithme de matching
│   └── requirements.txt            # Dépendances Python du projet
│
├── frontend/
│   ├── templates/
│   │   └── index.html              # Interface utilisateur (Formulaire)
│   └── static/
│       ├── css/
│       │   └── style.css           # Design de la plateforme
│       ├── js/
│       │   └── script.js           # Gestion des requêtes Fetch & Affichage dynamique
│       └── images/
│           └── logo.png            # Logo de l'application
│
├── database/
│   └── script_creation.sql         # Script d'export de la base de données
│
├── .gitignore                      # Exclusion du dossier venv/ et des caches
└── README.md                       # Guide d'utilisation du projet
```

## Installation et Lancement Local

Suivez ces étapes pour exécuter le projet sur votre machine de test.

### 1. Configuration de la Base de Données (XAMPP)
1. Lancez **XAMPP Control Panel** et démarrez les modules **Apache** et **MySQL**.
2. Accédez à `http://localhost/phpmyadmin/`.
3. Créez une nouvelle base de données nommée `mentorlink` avec l'encodage `utf8mb4_general_ci`.

### 2. Configuration du Back-end (Flask)
1. Ouvrez votre terminal dans le dossier `backend/` du projet :
   ```bash
   cd backend
   ```
2. Créez et activez votre environnement virtuel :
   ```bash
   python -m venv venv
   # Sur Windows (PowerShell) :
   .\venv\Scripts\activate
   ```
3. Installez l'ensemble des dépendances requises :
   ```bash
   pip install -r requirements.txt
   ```
4. Initialisez et peuplez automatiquement la base de données avec les données de démonstration :
   ```bash
   flask --app app.py init-db
   ```
   *(Un message confirmant l'insertion de 4 mentors de test s'affichera)*.

### 3. Lancement de l'Application
1. Démarrez le serveur serveur local Flask :
   ```bash
   python app.py
   ```
2. Ouvrez votre navigateur internet et accédez à l'adresse suivante : **`http://127.0.0.1:5000`**

## Jeu de Test

Pour valider le fonctionnement de la tolérance horaire et du bonus de filière :
* **Saisie** : Matières = `Python` | Horaire = `15:00` | Filière = `Licence IA`
* **Résultat** : La mentor **Awa Chabi** s'affichera en premier (disponible à 16:00, écart de 60 minutes validé, bonus filière appliqué).
* **Saisie** : Matières = `Python` | Horaire = `16:30`
* **Résultat** : Les mentors **Awa Chabi** (dispo 16h) et **Marc Agbodjan** (dispo 17h) s'afficheront simultanément à l'écran, triés selon leur score de proximité horaire.

