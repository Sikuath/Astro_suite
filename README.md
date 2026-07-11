# 🌌 Astro_suite

![Astro_suite](https://img.shields.io/badge/Astro_suite-Astrophotographie-blue)
![Python](https://img.shields.io/badge/Python-3.x-yellow)
![Streamlit](https://img.shields.io/badge/Interface-Streamlit-red)
![Siril](https://img.shields.io/badge/Traitement-Siril-purple)

## 🚀 Présentation

**Astro_suite** est une suite logicielle dédiée à l'astrophotographie.

Son objectif est de proposer un environnement complet permettant d'accompagner l'astrophotographe depuis la gestion des acquisitions jusqu'au traitement final des images.

La suite automatise les tâches répétitives tout en s'appuyant sur des logiciels spécialisés reconnus comme **Siril**.

Workflow général :

```
📁 Gestion du projet
        ↓
🔭 Sélection des acquisitions
        ↓
🗑️ Vérification des rejets
        ↓
⚙️ Prétraitement automatique Siril
        ↓
✨ Traitement final LRGB / SHO
```

---

# ✨ Fonctionnalités

## 📁 Gestion de projet

Astro_suite permet de centraliser une session astrophotographique :

- configuration du dossier Lights
- configuration du chemin Siril
- organisation automatique des fichiers
- sauvegarde des paramètres du projet

---

# 🔭 Analyse automatique des acquisitions

La suite analyse les fichiers FITS afin d'identifier automatiquement :

- 🎯 l'objet photographié
- 📷 la caméra utilisée
- 🎨 les filtres disponibles
- 📊 le nombre d'images

Les informations sont récupérées directement depuis les entêtes FITS lorsque celles-ci sont disponibles.

Exemple :

```json
{
  "target": "IC 1805",
  "camera": "ZWO ASI2600MM Pro",
  "filters": {
    "H": 31,
    "O": 31,
    "S": 31
  },
  "type": "SHO",
  "files": 93
}
```

---

# 🗑️ Sélection et contrôle des Lights

Avant le prétraitement, Astro_suite permet :

- visualisation rapide des images FITS
- navigation dans les acquisitions
- rejet manuel des images indésirables

Les images rejetées sont déplacées automatiquement dans un dossier dédié.

Une étape de contrôle permet ensuite :

- d'afficher les images rejetées
- de restaurer une image supprimée par erreur
- de valider la sélection finale

---

# ⚙️ Prétraitement Siril automatisé

Astro_suite détecte automatiquement le type de session.

## 🌈 SHO

Détection :

- Hα
- OIII
- SII

Pipeline :

```
Alignement_lights.ssf
          ↓
Traitement_SHO.ssf
```

---

## 🌈 LSHO

Détection :

- Luminance
- Hα
- OIII
- SII

Pipeline :

```
Alignement_lights.ssf
          ↓
Traitement_LSHO.ssf
```

---

## 🎨 LRGB

Détection :

- Luminance
- Rouge
- Vert
- Bleu

Pipeline :

```
Alignement_lights.ssf
          ↓
Traitement_LRGB.ssf
```

---

# 🖥️ Console de traitement intégrée

Le traitement Siril est directement piloté depuis l'interface.

La console affiche :

- lancement des scripts
- messages Siril
- erreurs éventuelles
- état d'avancement du pipeline

L'utilisateur n'a pas besoin de lancer manuellement les scripts.

---

# 🗂️ Organisation automatique des fichiers

Après traitement, Astro_suite organise les couches :

```
Projet
│
├── L
├── R
├── G
├── B
├── H
├── O
├── S
│
├── x_temp
│
└── scripts
```

Cette organisation facilite les étapes suivantes du traitement.

---

# 🧩 Architecture du projet

```
Astro_suite
│
├── Astro_pretraitement
│
│   ├── app.py
│   │
│   ├── pages
│   │   ├── 01_Project.py
│   │   ├── 02_Preview.py
│   │   ├── 03_Check.py
│   │   ├── 04_Pretraitement.py
│   │   └── 05_Traitement.py
│   │
│   ├── core
│   │   ├── config.py
│   │   ├── fits_loader.py
│   │   ├── fits_metadata.py
│   │   ├── preview.py
│   │   ├── reject.py
│   │   └── session_analyzer.py
│   │
│   ├── scripts
│   │   ├── Alignement_lights.ssf
│   │   ├── Traitement_LRGB.ssf
│   │   ├── Traitement_SHO.ssf
│   │   └── Traitement_LSHO.ssf
│   │
│   └── ui
│       ├── sidebar.py
│       └── theme.py
│
└── README.md
```

---

# 🛠️ Technologies utilisées

## Interface

- Python
- Streamlit

## Astronomie

- Siril
- FITS
- Astropy

## Gestion des fichiers

- pathlib
- shutil
- subprocess

---

# 🎯 Objectifs

Astro_suite a été développé pour :

- simplifier les traitements astrophotographiques répétitifs
- réduire les erreurs de manipulation
- automatiser les étapes longues
- proposer un workflow clair et reproductible
- rendre les traitements avancés plus accessibles

---

# 🔮 Évolutions possibles

Les futures évolutions pourront inclure :

- analyse automatique de la qualité des images
- mesure FWHM des étoiles
- détection automatique des mauvaises acquisitions
- gestion des darks, flats et offsets
- automatisation complète acquisition → image finale
- historique des sessions traitées

---

# 🌌 Philosophie du projet

Astro_suite ne cherche pas à remplacer les logiciels astronomiques existants.

Son objectif est de créer une couche d'automatisation intelligente permettant de connecter les différents outils astrophotographiques dans un workflow simple, fiable et efficace.

---

# 👨‍🚀 Astro_suite

**Observer • Capturer • Trier • Prétraiter • Créer**

📄 Licence

MIT License © 2026

© 2026 Sikuath