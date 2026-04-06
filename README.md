# 📁 Application d’Archivage de Documents

Application web développée avec Flask permettant de gérer, organiser et archiver des documents de manière structurée (documents reçus et envoyés).


---

## 📌 Description

Cette application permet de téléverser, stocker, organiser et filtrer des documents dans un système local.

Les fichiers sont classés automatiquement selon leur type :
- 📥 Documents reçus
- 📤 Documents envoyés

Chaque document est associé à des métadonnées (titre, date, chemin) stockées en base de données.

---

## ✨ Fonctionnalités

- 📤 Upload de fichiers avec titre et date
- 📥 Téléchargement de documents
- 🗑️ Suppression des fichiers et des entrées en base
- 📂 Organisation automatique des fichiers (reçu / envoyé)
- 📊 Dashboard avec :
  - Nombre total de documents
  - Taille totale du stockage
- 🔍 Filtrage avancé :
  - Par mot-clé
  - Par jour, mois et année
- 🧾 Gestion des métadonnées
- 🛡️ Sécurisation des noms de fichiers (secure_filename)

---

## 🛠️ Technologies utilisées

- Python
- Flask
- SQLite
- SQLAlchemy
- HTML / CSS
- Werkzeug

---

## 🧱 Structure du projet
