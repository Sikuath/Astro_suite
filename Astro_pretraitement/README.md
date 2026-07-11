# 🔭 Astro_Pretraitement

## Assistant de prétraitement astrophotographique automatisé

**Astro_Pretraitement** est une application développée avec **Streamlit** permettant d'automatiser et de sécuriser la préparation des images astronomiques avant traitement final.

L'objectif est de proposer un workflow simple :

**Acquisition → Sélection → Vérification → Prétraitement Siril → Traitement final**

L'application analyse automatiquement une session d'imagerie, identifie le type de traitement nécessaire (SHO, LSHO ou LRGB) et pilote les scripts **Siril** adaptés.

---

# ✨ Fonctionnalités principales

## 📁 Gestion du projet

L'utilisateur définit :

* le dossier contenant les images **Lights**
* le dossier des images rejetées
* le chemin vers l'exécutable Siril

La configuration est sauvegardée automatiquement afin de retrouver le projet lors des prochaines utilisations.

---

# 🔭 Workflow complet

## 1️⃣ Configuration du projet

La première étape permet de définir :

* 📂 dossier des acquisitions
* 🗑️ dossier des images rejetées
* ⚙️ paramètres nécessaires au traitement

Une fois le projet chargé, l'application prépare automatiquement les étapes suivantes.

---

## 2️⃣ Sélection des meilleures acquisitions

Cette étape permet de parcourir rapidement les fichiers FITS :

* affichage des prévisualisations
* navigation dans les images
* rejet manuel des images présentant :

  * défaut de suivi
  * passage nuageux
  * satellite
  * problème de guidage
  * défaut d'exposition

Les images rejetées sont déplacées dans un dossier dédié.

---

## 3️⃣ Vérification des rejets

Avant le prétraitement, l'utilisateur peut :

* contrôler les images mises de côté
* restaurer une image si nécessaire

Aucune suppression définitive n'est réalisée.

---

# 4️⃣ Analyse automatique de la session

Astro_Pretraitement analyse les fichiers FITS et récupère les informations utiles :

* 🎯 objet photographié
* 📷 caméra utilisée
* 🎨 filtres présents
* 📊 nombre d'images par couche

Les informations sont récupérées :

* depuis les noms de fichiers
* depuis les métadonnées FITS lorsque disponibles

Exemple :

```json
{
  "target": "IC 1805",
  "camera": "ZWO ASI2600MM Pro",
  "filters": {
    "H":31,
    "O":31,
    "S":31
  },
  "type":"SHO",
  "files":93
}
```

---

# 🧠 Détection automatique du traitement

L'application détermine automatiquement le pipeline nécessaire.

## 🌈 SHO

Détecté lorsque les couches suivantes sont présentes :

* Hα
* OIII
* SII

Pipeline utilisé :

```
Alignement → Tri des couches → Traitement SHO
```

---

## 🌈 LSHO

Détecté lorsque :

* Luminance
* Hα
* OIII
* SII

sont disponibles.

Pipeline utilisé :

```
Alignement → Tri des couches → Traitement LSHO
```

---

## 🎨 LRGB

Détecté lorsque :

* Luminance
* Rouge
* Vert
* Bleu

sont disponibles.

Pipeline utilisé :

```
Alignement → Tri des couches → Traitement LRGB
```

---

# 5️⃣ Prétraitement Siril automatisé

L'application pilote Siril en ligne de commande.

Le pipeline réalise automatiquement :

## Étape 1 — Alignement

Lancement du script :

```
Alignement_lights.ssf
```

Les fichiers sont préparés par Siril.

---

## Étape 2 — Organisation automatique des couches

Les images sont réparties automatiquement :

```
L/
R/
G/
B/
H/
O/
S/
```

en fonction du filtre détecté.

---

## Étape 3 — Nettoyage temporaire

Le dossier :

```
x_temp
```

est automatiquement nettoyé après utilisation.

---

## Étape 4 — Traitement final

Selon l'analyse de la session :

```
Traitement_SHO.ssf
Traitement_LSHO.ssf
Traitement_LRGB.ssf
```

est lancé automatiquement.

---

# 🖥️ Console intégrée

Une console Streamlit affiche en temps réel :

* lancement des scripts Siril
* progression du traitement
* messages Siril
* erreurs éventuelles

L'utilisateur garde une visibilité complète sur le traitement.

---

# 🛠️ Technologies utilisées

* Python
* Streamlit
* Astropy
* Siril CLI
* FITS
* JSON

---

# 📂 Organisation du projet

Structure simplifiée :

```
Astro_pretraitement/

│
├── app.py
│
├── pages/
│   ├── 01_Project.py
│   ├── 02_Preview.py
│   ├── 03_Check.py
│   ├── 04_Pretraitement.py
│   └── 05_Traitement.py
│
├── core/
│   ├── config.py
│   ├── fits_loader.py
│   ├── fits_metadata.py
│   ├── preview.py
│   ├── reject.py
│   └── session_analyzer.py
│
├── scripts/
│   ├── Alignement_lights.ssf
│   ├── Traitement_SHO.ssf
│   ├── Traitement_LSHO.ssf
│   └── Traitement_LRGB.ssf
│
└── ui/
    ├── sidebar.py
    └── theme.py
```

---

# 🎯 Objectif du projet

Astro_Pretraitement a été conçu pour transformer une suite d'opérations répétitives en un workflow simple :

> Choisir ses images → vérifier → lancer → laisser Siril travailler.

L'application permet de réduire les manipulations manuelles tout en conservant le contrôle de l'utilisateur à chaque étape.

---

## 🔭 Astro Suite

Projet personnel d'automatisation astrophotographique.

📄 Licence

MIT License © 2026

© 2026 Sikuath
