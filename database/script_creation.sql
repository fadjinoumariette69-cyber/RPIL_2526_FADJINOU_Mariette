-- ============================================================
-- IFRI_MentorLink — Script de création de la base de données
-- Moteur : MySQL
-- ============================================================

CREATE DATABASE IF NOT EXISTS mentorlink CHARACTER SET utf8mb4;
USE mentorlink;

-- ------------------------------------------------------------
-- Table des mentors
-- ------------------------------------------------------------
CREATE TABLE IF NOT EXISTS mentors (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    nom             VARCHAR(120) NOT NULL,
    matieres        VARCHAR(255) NOT NULL,   -- ex: "Algorithmique,Python"
    disponibilites  VARCHAR(255) NOT NULL,   -- ex: "14:00,16:00"
    filiere         VARCHAR(120),
    format          VARCHAR(50)  NOT NULL    -- "présentiel" | "en ligne" | "les deux"
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ------------------------------------------------------------
-- Données de démonstration (au moins 3 mentors, comme exigé)
-- ------------------------------------------------------------
INSERT INTO mentors (nom, matieres, disponibilites, filiere, format) VALUES
('Awa Chabi',
 'Algorithmique,Structures de données,Python',
 '14:00,16:00',
 'Licence IA',
 'en ligne'),

('Kévin Dossou',
 'Bases de données,SQL,Modélisation',
 '09:00,10:30,18:00',
 'Licence GL',
 'présentiel'),

('Sandrine Houngbo',
 'Réseaux,Sécurité,Linux',
 '13:00,15:30',
 'Licence SE&IoT',
 'les deux'),

('Marc Agbodjan',
 'Python,Intelligence artificielle,Machine Learning',
 '17:00,19:00',
 'Licence IA',
 'en ligne');