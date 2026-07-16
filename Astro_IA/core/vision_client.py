# ==========================================================
# Astro IA
# Client Ollama Vision
# Analyse image astrophotographique LLaVA
# ==========================================================


from pathlib import Path

import ollama



# ==========================================================
# ANALYSE IMAGE AVEC LLAVA
# ==========================================================


def analyse_image(

    image_path,

    model="llava:7b"

):

    """
    Analyse visuelle d'une image PNG
    préparée pour Ollama Vision.

    Cette fonction réalise uniquement
    une observation visuelle.

    Aucune mesure scientifique :
    FWHM, HFR, seeing, suivi, bruit,
    photométrie ou résolution.
    """



    image_path = Path(

        image_path

    ).resolve()



    if not image_path.exists():

        return (

            "Image non disponible."

        )



    # ======================================================
    # PROMPT VISION
    # ======================================================


    prompt = """

Tu es Astro IA Vision.

Tu analyses une prévisualisation
étirée d'une image astrophotographique.

Cette image a été préparée pour révéler
le signal faible visible.

Tu n'as accès qu'à l'image.

Tu ne connais pas :

- le nom de l'objet
- les coordonnées
- la caméra
- la focale
- les paramètres d'acquisition


Ton rôle est uniquement une observation
visuelle de ce qui est réellement visible.


Commence obligatoirement par :

Observation visuelle uniquement.



==================================================
1 - FOND DE CIEL
==================================================


Décris :

- homogénéité du fond
- présence éventuelle de gradients lumineux
- zones plus claires ou plus sombres
- variations visibles du fond



==================================================
2 - ETOILES
==================================================


Décris uniquement visuellement :

- densité apparente d'étoiles
- différence entre étoiles brillantes et faibles
- aspect général des étoiles
- étoiles ponctuelles, diffuses ou allongées


Interdiction absolue :

Ne jamais donner :

- FWHM
- HFR
- seeing
- excentricité
- qualité de suivi
- résolution
- bruit mesuré
- photométrie



==================================================
3 - STRUCTURES ASTRONOMIQUES
==================================================


Recherche uniquement les structures
visibles dans l'image :

- amas d'étoiles apparent
- nébulosités
- extensions faibles
- zones sombres
- poussières apparentes
- zones de contraste


IMPORTANT :

Si une structure n'est pas clairement visible,
ne dis pas :

"Il n'y a pas de structure."


Utilise :

"Aucune structure clairement identifiable
sur cette prévisualisation."



==================================================
4 - DEFAUTS VISUELS
==================================================


Signale uniquement les défauts visibles :

- gradients importants
- dominante de couleur
- zones saturées
- artefacts
- traces
- problèmes évidents


Ne déduis jamais un problème
à partir d'une absence d'information.



==================================================
REGLES ABSOLUES
==================================================


Tu ne réalises aucune mesure scientifique.

Tu ne peux pas déterminer :

- qualité réelle de l'acquisition
- mise au point
- seeing
- suivi
- calibration
- sensibilité


Tu ne dois jamais identifier
un objet astronomique.


Tu ne dois jamais transformer
une observation visuelle en conclusion scientifique.


Si une information n'est pas visible :

"Non déterminable visuellement."


Réponds uniquement en français.

"""



    try:


        response = ollama.chat(

            model=model,


            messages=[

                {

                    "role": "user",

                    "content": prompt,


                    "images": [

                        str(image_path)

                    ]

                }

            ],


            options={

                "temperature": 0.1,

                "num_ctx": 4096

            }

        )


        result = response[

            "message"

        ][

            "content"

        ]



        # DEBUG TEMPORAIRE
        print(
            "=============================="
        )

        print(
            "DEBUG REPONSE LLAVA"
        )

        print(
            result
        )

        print(
            "=============================="
        )



        return result



    except Exception as e:


        return (

            f"Erreur analyse vision : {e}"

        )