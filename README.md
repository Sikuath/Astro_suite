# 🌌 Astro_suite

![Astro_suite](https://img.shields.io/badge/Astro_suite-Astrophotographie-blue)
![Python](https://img.shields.io/badge/Python-3.x-yellow)
![Streamlit](https://img.shields.io/badge/Interface-Streamlit-red)
![Siril](https://img.shields.io/badge/Traitement-Siril-purple)
![Ollama](https://img.shields.io/badge/IA-Ollama-black)

---

# 🚀 Présentation

**Astro_suite** est une suite logicielle dédiée à l'astrophotographie.

Son objectif est de proposer un environnement complet permettant d'accompagner l'astrophotographe depuis la gestion des acquisitions jusqu'au traitement final des images.

Astro_suite ne cherche pas à remplacer les logiciels astronomiques existants mais à créer une couche d'automatisation intelligente reliant plusieurs outils spécialisés :

- **Siril** pour le traitement astronomique
- **GIMP** pour le traitement final des images
- **Python** pour l'automatisation
- **Ollama** pour l'intelligence artificielle locale

L'objectif est de construire un workflow cohérent, reproductible et entièrement maîtrisé par l'utilisateur.

---

# 🌌 Workflow général

```text
📁 Gestion du projet
        ↓
🔭 Analyse des acquisitions
        ↓
🗑️ Sélection des images
        ↓
⚙️ Prétraitement automatique Siril
        ↓
🤖 Analyse Astro_IA
        ↓
🎨 Traitement Siril / GIMP
        ↓
✨ Image finale
```

---

# 🧩 Organisation générale

Astro_suite est composé de plusieurs modules complémentaires :

```
Astro_suite

├── Astro_pretraitement
│
└── Astro_IA
```

Chaque module possède son propre rôle dans le workflow astrophotographique.

---

# 🔭 Astro_pretraitement

## Gestion des acquisitions

Le module **Astro_pretraitement** constitue la première étape du traitement.

Il permet :

- création et gestion des projets
- configuration du dossier de travail
- analyse des fichiers FITS
- lecture des métadonnées
- identification des filtres
- détection automatique du type de session
- visualisation rapide des acquisitions
- rejet manuel des images
- lancement automatique des scripts Siril

---

# 🔭 Analyse automatique des fichiers FITS

Astro_suite analyse les fichiers FITS afin d'extraire :

- 🎯 objet photographié
- 📷 caméra utilisée
- 🔭 télescope
- 🎨 filtres disponibles
- ⏱️ temps d'exposition
- 🌡️ température capteur
- 📊 nombre d'images disponibles

Les informations sont récupérées depuis les entêtes FITS.

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

- navigation dans les acquisitions
- visualisation rapide des images FITS
- contrôle manuel des prises de vue
- rejet des images indésirables

Les images rejetées sont automatiquement déplacées dans un dossier dédié.

Cette étape permet :

- nettoyage des acquisitions
- conservation des originaux
- validation avant traitement Siril

---

# ⚙️ Prétraitement Siril automatisé

Astro_suite pilote Siril automatiquement grâce aux scripts.

Les sessions sont détectées selon les filtres disponibles.

---

## 🌈 SHO

Filtres :

- Hα
- OIII
- SII

Pipeline :

```text
Alignement_lights.ssf
          ↓
Traitement_SHO.ssf
```

---

## 🌈 LSHO

Filtres :

- Luminance
- Hα
- OIII
- SII

Pipeline :

```text
Alignement_lights.ssf
          ↓
Traitement_LSHO.ssf
```

---

## 🎨 LRGB

Filtres :

- Luminance
- Rouge
- Vert
- Bleu

Pipeline :

```text
Alignement_lights.ssf
          ↓
Traitement_LRGB.ssf
```

---
# 🤖 Astro_IA

## Assistant astrophotographique intelligent

Le module **Astro_IA** apporte une couche d'analyse scientifique et d'assistance au traitement.

Il permet :

- analyse des fichiers FITS
- calcul du champ photographié
- résolution astrométrique avec Siril
- identification des objets présents dans l'image
- interrogation de bases astronomiques
- analyse visuelle par intelligence artificielle
- génération automatique d'un rapport

---

# 🧠 Intelligence artificielle locale

Astro_IA fonctionne avec des modèles exécutés localement grâce à **Ollama**.

Aucune image n'est envoyée vers un service distant.

Architecture :

```text
Image FITS
    |
    |
    +--> Siril
    |       |
    |       +--> Résolution astrométrique
    |       +--> Analyse du champ
    |
    +--> LLaVA
    |       |
    |       +--> Analyse visuelle
    |
    +--> Astro Expert / Qwen
            |
            +--> Rapport scientifique
```

---

# 👁️ Analyse visuelle LLaVA

Le module vision utilise LLaVA afin d'obtenir une analyse visuelle de l'image.

Il permet :

- observation générale de l'image
- identification de structures visibles
- analyse qualitative
- aide à l'interprétation

Cette analyse complète les données astronomiques issues de Siril.

---

# 🔬 Analyse scientifique Astro_IA

Le modèle scientifique exploite :

- les métadonnées FITS
- les informations Siril
- le champ photographié
- les objets détectés
- les données SIMBAD
- l'observation visuelle LLaVA

Il génère un rapport contenant :

- contexte d'acquisition
- analyse astronomique
- conseils de traitement
- suggestions pour la suite du workflow

---

# 📄 Gestion des rapports IA

Chaque projet possède son propre historique.

Organisation :

```text
x_projects/

└── Objet_20260717_153000/

    ├── reports/

    │   ├── rapport_IA.txt
    │   └── rapport_IA.json

    ├── workflow.json
    └── project.json
```

Le rapport conserve :

- date d'analyse
- objet photographié
- paramètres d'acquisition
- informations FITS
- champ photographié
- analyse visuelle
- rapport scientifique

---

# 🧭 Workflow astrophotographique

Astro_suite intègre un suivi manuel des étapes de traitement.

Le workflow est enregistré dans chaque projet et permet de reprendre une session interrompue.

---

## A - Siril

```
☐ Recadrage image

☐ Résolution astrométrique

☐ Extraction de gradient

☐ Suppression du bruit vert

☐ Étalonnage des couleurs par photométrie

☐ Abberration Remover (script Python)

☐ CosmicClarity_Sharpen (script Python)

☐ Veralux_Silentium (script Python)

☐ Création de la Starless

☐ Étirement de la Starless
```

---

## B - GIMP

```
☐ Traitement de la Starless

☐ Ajustement du niveau des couleurs

☐ Réduction du bruit

☐ Renforcement des couleurs

☐ Rehaussement des couleurs

☐ Traitement par courbes

☐ Filtre passe-haut

☐ Balance des couleurs
```

---

## C - Siril

```
☐ Travail du masque d'étoiles

☐ Suppression des zones violettes

☐ Inversion / suppression bruit vert / inversion

☐ Recomposition Starless / masque d'étoiles

☐ Déconvolution éventuelle
```

---

## D - GIMP

```
☐ Finition finale
```

---

# 📁 Gestion des projets

Chaque session astrophotographique possède son propre espace de travail.

Exemple :

```text
x_projects/

└── NGC7000_20260717_153000/

    ├── fits/
    │
    ├── previews/
    │
    ├── reports/
    │
    ├── exports/
    │
    ├── logs/
    │
    ├── workflow.json
    │
    └── project.json
```

---

# 💾 Sauvegarde du projet

Le fichier `project.json` conserve :

```json
{
    "project_id": "NGC7000_20260717_153000",
    "object": "NGC7000",
    "created": "2026-07-17T15:30:00",
    "status": "created"
}
```

Le fichier `workflow.json` conserve l'avancement :

```json
{
    "section": "A - Siril",
    "steps": [
        {
            "id": "gradient",
            "name": "Extraction de gradient",
            "done": true
        }
    ]
}
```

---

# 🖥️ Interface utilisateur

Astro_suite utilise **Streamlit** pour proposer une interface locale moderne.

Fonctionnalités :

- gestion des projets
- navigation entre modules
- affichage FITS
- suivi workflow
- consultation rapports IA
- interface transparente
- thème astrophotographique

---
# 🧩 Architecture du projet

Organisation générale :

```text
Astro_suite

│
├── Astro_pretraitement
│
│   ├── app.py
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
│   │   ├── Traitement_SHO.ssf
│   │   ├── Traitement_LSHO.ssf
│   │   └── Traitement_LRGB.ssf
│   │
│   └── ui
│       ├── sidebar.py
│       └── theme.py
│
│
├── Astro_IA
│
│   ├── app.py
│   │
│   ├── core
│   │   ├── fits_io.py
│   │   ├── siril_runner.py
│   │   ├── siril_analyser.py
│   │   ├── ollama_client.py
│   │   ├── vision_client.py
│   │   ├── simbad_client.py
│   │   ├── workflow_manager.py
│   │   └── project_manager.py
│   │
│   ├── ui
│   │   ├── pages
│   │   ├── sidebar.py
│   │   └── theme.py
│   │
│   └── reports
│
│
└── README.md
```

---

# 🛠️ Technologies utilisées

## Langage

- Python 3.x

---

## Interface

- Streamlit

---

## Astronomie

- Siril
- FITS
- Astropy
- SIMBAD

---

## Intelligence artificielle

- Ollama
- Qwen
- LLaVA

---

## Traitement image

- Siril
- GIMP

---

## Gestion système

- pathlib
- shutil
- subprocess
- JSON

---

# 🎯 Objectifs du projet

Astro_suite a été développé pour :

- automatiser les tâches répétitives
- réduire les erreurs de manipulation
- conserver une méthode de traitement reproductible
- faciliter les longues sessions astrophotographiques
- garder un historique complet des projets
- accompagner l'utilisateur dans ses choix de traitement

---

# 🔮 Évolutions prévues

Les prochaines versions pourront intégrer :

## Analyse automatique des acquisitions

- mesure FWHM des étoiles
- estimation de la qualité des images
- détection automatique des mauvais Lights
- classement automatique des acquisitions

---

## Automatisation Siril avancée

- génération automatique de scripts
- adaptation des paramètres selon la session
- gestion complète :
  - darks
  - flats
  - offsets

---

## Intelligence artificielle avancée

- assistant de traitement GIMP
- analyse comparative avant/après
- suggestions personnalisées selon l'objet
- bibliothèque de traitements réussis

---

# 🌌 Philosophie du projet

Astro_suite repose sur plusieurs principes :

## 🔓 Logiciels libres

Le projet privilégie :

- Siril
- GIMP
- Python
- outils locaux

---

## 🖥️ Traitement local

Les images restent sur la machine de l'utilisateur.

L'intelligence artificielle fonctionne localement grâce à Ollama.

---

## 🎛️ Contrôle utilisateur

L'IA propose.

L'astrophotographe décide.

Astro_suite ne remplace pas l'expérience humaine mais permet de mieux exploiter les outils disponibles.

---

# 🌠 Vision du projet

Créer un véritable atelier numérique astrophotographique :

```text
Observer
    ↓
Capturer
    ↓
Comprendre
    ↓
Préparer
    ↓
Traiter
    ↓
Créer
```

---

# 👨‍🚀 Astro_suite

Développé par **Sikuath**

Licence MIT © 2026

---

## 📜 Licence

Ce projet est distribué sous licence MIT.

Vous êtes libre de :

- utiliser le logiciel
- modifier le code
- redistribuer le projet

Sous réserve de conserver les mentions de licence.

---

# 🌌 Astro_suite

**Observer • Comprendre • Prétraiter • Créer**