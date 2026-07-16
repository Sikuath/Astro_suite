# Astro IA

# Bibliothèque des défauts visuels

Ce document constitue une bibliothèque de référence.

Il ne décrit PAS le contenu de l'image analysée.

Il décrit uniquement les défauts susceptibles d'être rencontrés
en astrophotographie et la manière de les interpréter.

Astro IA doit utiliser cette bibliothèque uniquement lorsque
le défaut est explicitement observé par LLaVA.

Si LLaVA ne mentionne pas un défaut, Astro IA ne doit jamais :

- supposer sa présence ;
- le décrire ;
- proposer une correction spécifique basée sur ce défaut.

Cette bibliothèque sert uniquement de référence pour
interpréter une observation déjà confirmée.

---

# Gradient de fond de ciel

## Aspect visuel

* fond plus clair d'un côté de l'image
* variation progressive de luminosité
* variation progressive de couleur
* absence de limite nette

## Causes possibles

* pollution lumineuse
* Lune
* extinction atmosphérique
* retrait de gradient incomplet

## Traitement conseillé

Siril :

* Extraction du gradient

---

# Vignettage résiduel

## Aspect visuel

* coins plus sombres
* centre plus lumineux
* forme généralement circulaire

## Peut être confondu avec

* gradient

## Traitement conseillé

Siril :

* correction du fond
* extraction du gradient

---

# Dominante verte

## Aspect visuel

* fond verdâtre
* étoiles légèrement vertes
* nébulosités avec teinte verte anormale

## Traitement conseillé

Siril :

* Suppression du bruit vert

Puis :

* étalonnage photométrique

---

# Dominante magenta

## Aspect visuel

* fond rose ou violet
* étoiles violacées
* halos magenta

## Traitement conseillé

* balance des couleurs
* correction locale

---

# Dominante bleue

## Aspect visuel

* image globalement froide
* fond bleu
* étoiles blanches tirant vers le bleu

## Traitement conseillé

* calibration photométrique
* balance des couleurs

---

# Bruit de luminance

## Aspect visuel

* grain gris
* texture irrégulière
* présent principalement dans le fond

## Traitement conseillé

* réduction de bruit modérée

---

# Bruit chromatique

## Aspect visuel

* pixels rouges
* pixels verts
* pixels bleus

répartis aléatoirement.

## Traitement conseillé

* réduction du bruit couleur

---

# Bruit vert

## Aspect visuel

* petits pixels verts
* dominante verte localisée

## Traitement conseillé

Siril :

* Suppression du bruit vert

---

# Étoiles saturées

## Aspect visuel

* cœur entièrement blanc
* disparition de la couleur
* halos possibles

## Traitement conseillé

* réduction des étoiles
* traitement séparé étoiles/fond

---

# Étoiles trop dominantes

## Aspect visuel

* étoiles attirant davantage le regard que le sujet principal
* masquage du signal faible

## Traitement conseillé

* création d'une starless
* réduction des étoiles
* recomposition finale

---

# Étoiles allongées

## Aspect visuel

* étoiles ovales
* direction commune
* légère traînée

## Causes possibles

* suivi
* flexion
* vent
* problème mécanique

## Important

Ne jamais conclure à un défaut de suivi sans mesure.

Écrire :

« Aspect compatible avec une légère ovalisation. »

---

# Coma

## Aspect visuel

* étoiles en forme de petite comète
* déformation croissante vers les coins

## Traitement conseillé

* recadrage éventuel

Ne jamais conclure à un mauvais correcteur.

---

# Tilt

## Aspect visuel

* un coin net
* un coin flou
* qualité variable selon la position

## Important

Le tilt ne peut pas être confirmé visuellement seul.

---

# Halos autour des étoiles

## Aspect visuel

* anneaux lumineux
* auréoles
* contour brillant

## Causes possibles

* filtre
* traitement excessif
* recomposition imparfaite

## Traitement conseillé

* correction locale
* recomposition des étoiles

---

# Déconvolution excessive

## Aspect visuel

* anneaux autour des étoiles
* contours artificiels
* texture peu naturelle

## Traitement conseillé

* réduire l'intensité de la déconvolution

---

# Suraccentuation (Sharpen excessif)

## Aspect visuel

* détails artificiels
* contours trop marqués
* aspect granuleux

## Traitement conseillé

* diminuer le renforcement

---

# Fond de ciel écrasé

## Aspect visuel

* fond entièrement noir
* disparition des faibles extensions
* perte de détails

## Traitement conseillé

* reprendre l'étirement
* diminuer le point noir

---

# Fond de ciel trop clair

## Aspect visuel

* image peu contrastée
* fond gris clair
* manque de profondeur

## Traitement conseillé

* ajustement des niveaux
* courbes

---

# Couleurs trop saturées

## Aspect visuel

* couleurs très vives
* étoiles irréalistes
* nébulosités artificielles

## Traitement conseillé

* réduire la saturation globale ou locale

---

# Recomposition étoiles / starless imparfaite

## Aspect visuel

* raccords visibles
* halos
* contours anormaux
* différences de luminosité

## Traitement conseillé

* reprendre la fusion
* vérifier les masques

---

# Règles générales

Astro IA ne doit jamais transformer une ressemblance visuelle en diagnostic certain.

Toujours distinguer :

* observation visuelle ;
* hypothèse ;
* mesure scientifique.

Les mesures telles que FWHM, HFR, SNR, excentricité ou seeing ne peuvent être affirmées que si elles sont réellement calculées.

En cas de doute, utiliser la formulation :

« Aspect compatible avec… Une vérification complémentaire est recommandée. »
