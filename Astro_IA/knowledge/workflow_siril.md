# Workflow Siril - Astro IA
# Traitement post-empilement


## Rôle de Siril dans Astro IA


Siril intervient après la création de l'image intégrée.


Les étapes d'acquisition sont considérées comme terminées :

- calibration
- masters
- alignement
- empilement


Siril est utilisé pour :

- préparation de l'image
- corrections techniques
- séparation étoiles/fond
- reconstruction finale



==================================================

# 1 - Recadrage

==================================================


Objectif :

Préparer le cadrage final avant traitement.


Actions :

- supprimer les bordures inutiles
- conserver la zone scientifique intéressante
- améliorer la composition


A éviter :

- recadrages successifs destructifs



==================================================

# 2 - Résolution astrométrique

==================================================


Objectif :

Associer précisément l'image au ciel.


Utilisations :

- calibration photométrique
- informations du champ
- cohérence des traitements


Ne constitue pas une amélioration esthétique directe.



==================================================

# 3 - Extraction du gradient

==================================================


Objectif :

Corriger les variations du fond de ciel.


Utiliser :

Extraction du gradient


Méthode :

- placer les points sur les zones neutres
- éviter les nébulosités
- éviter les galaxies
- éviter les étoiles brillantes


Résultat recherché :

- fond homogène
- conservation du signal faible



Ne jamais supprimer un gradient supposé
sans observation visuelle.



==================================================

# 4 - Suppression du bruit vert

==================================================


Objectif :

Corriger les dominantes vertes.


Utilisation :

- images couleur
- images issues de compositions RGB


Effet :

Neutralisation des dérives chromatiques.



==================================================

# 5 - Calibration photométrique

==================================================


Objectif :

Obtenir un équilibre colorimétrique cohérent.


Utiliser :

Calibration photométrique


Conditions :

- résolution astrométrique disponible


Résultat :

- couleurs plus naturelles
- meilleure cohérence des étoiles



==================================================

# 6 - Scripts externes

==================================================


Des scripts Python peuvent compléter Siril.


Exemples :


## Abberration Remover


Objectif :

Corriger certaines aberrations optiques.


---

## CosmicClarity Sharpen


Objectif :

Améliorer la finesse des détails.


Utilisation :

Modérée.

Eviter les artefacts.



---

## Veralux Silentium


Objectif :

Réduction ou amélioration contrôlée du bruit.



Règle générale :

Les scripts ne remplacent pas
une bonne séparation étoiles/fond.



==================================================

# 7 - Séparation étoiles / fond

==================================================


Siril moderne permet une séparation :


- image starless
- couche étoiles


Objectif :

Traiter séparément :

## Starless

- nébulosités
- galaxies
- structures faibles
- fond de ciel


## Etoiles

- taille
- luminosité
- saturation



Ne pas réduire les étoiles
avant cette séparation.



==================================================

# 8 - Etirement de la starless

==================================================


Objectif :

Révéler le signal faible.


Actions possibles :

- transformation d'histogramme
- étirement progressif


Attention :

Conserver :

- dynamique
- couleurs
- détails faibles



==================================================

# 9 - Retour Siril après GIMP

==================================================


Après traitement de la starless dans GIMP :


Réimporter :

- starless traitée
- couche étoiles


Objectif :

Reconstruire l'image finale.



==================================================

# 10 - Traitement du masque étoiles

==================================================


Actions possibles :

- ajustement du masque
- contrôle de la taille
- contrôle de luminosité


Objectif :

Obtenir des étoiles naturelles.



==================================================

# 11 - Correction des dominantes violettes

==================================================


Méthode possible :


- inversion image
- suppression bruit vert
- inversion retour


Objectif :

Réduire certaines dominantes chromatiques
sur les étoiles.



==================================================

# 12 - Reconstruction finale

==================================================


Fusionner :

- fond traité
- étoiles traitées


Contrôler :

- halos
- raccords
- couleurs
- saturation


Ne pas créer d'aspect artificiel.



==================================================

# 13 - Déconvolution

==================================================


Utilisation :

Optionnelle.


Conditions :

- étoiles suffisamment propres
- signal adapté


Ne jamais appliquer automatiquement.



==================================================

# Règles Astro IA Siril


Toujours privilégier :

- correction visible
- traitement modéré
- conservation du signal


Ne jamais recommander :

- refaire calibration
- refaire darks/flats/bias
- refaire alignement
- refaire empilement


Ces étapes appartiennent au prétraitement.