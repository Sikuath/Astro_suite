# 🤖 Astro_IA

Assistant local d'analyse et d'accompagnement pour l'astrophotographie.

Astro_IA est une application développée en Python avec Streamlit permettant d'analyser une image astrophotographique, d'exploiter les informations scientifiques contenues dans les fichiers FITS et de générer un rapport d'aide au traitement grâce à une intelligence artificielle locale.

Le projet a pour objectif de créer un véritable **assistant astrophotographique personnel**, capable d'accompagner l'utilisateur depuis l'analyse du champ jusqu'aux étapes finales de traitement dans Siril et GIMP.

---

# 🌌 Objectifs du projet

Astro_IA vise à répondre à une problématique simple :

> "Après avoir capturé une image astronomique, comment savoir quoi observer et quelles étapes appliquer pour obtenir le meilleur résultat ?"

L'application combine :

- analyse scientifique des données FITS
- reconnaissance du champ photographié
- interrogation de catalogues astronomiques
- analyse visuelle par intelligence artificielle
- génération d'un rapport personnalisé
- suivi d'un workflow de traitement reproductible

Le tout fonctionne **localement** afin de conserver les données astrophotographiques privées.

---

# ✨ Fonctionnalités principales

## 📷 Analyse des images FITS

Astro_IA récupère les informations contenues dans les fichiers FITS :

- objet photographié
- coordonnées célestes
- instrument utilisé
- télescope
- focale
- taille des pixels
- temps de pose
- gain caméra
- température capteur

Ces informations servent de base à l'analyse scientifique.

---

# 🔭 Analyse astronomique du champ

Grâce à Siril, Astro_IA peut effectuer :

- résolution astrométrique
- identification des objets présents dans le champ
- récupération des informations célestes

Les objets détectés sont ensuite filtrés selon différents critères.

---

# 🌠 Catalogue astronomique

Les objets détectés peuvent être enrichis grâce aux données SIMBAD :

- nom des objets
- type d'objet
- informations astronomiques
- contexte scientifique

Ces données servent ensuite à alimenter l'analyse IA.

---

# 🧠 Intelligence artificielle locale

Astro_IA utilise des modèles IA exécutés localement avec Ollama.

Deux types d'analyse sont réalisés :

## 👁️ Analyse visuelle

Modèle utilisé :

- LLaVA

Son rôle :

- observer l'image
- détecter les structures visibles
- identifier les défauts apparents
- fournir une première analyse visuelle

---

## 🔬 Analyse scientifique

Modèle utilisé :

- Astro-expert basé sur Qwen

Son rôle :

- interpréter les données FITS
- analyser le contexte astronomique
- proposer des pistes de traitement
- générer un rapport personnalisé

---

# 📄 Rapport IA

Chaque analyse produit un rapport sauvegardé dans le projet.

Le rapport contient :

- contexte d'acquisition
- informations FITS
- champ photographié
- objets détectés
- analyse visuelle LLaVA
- recommandations Astro IA

Formats sauvegardés :

# 📄 Licence

MIT License © 2026

© 2026 Sikuath