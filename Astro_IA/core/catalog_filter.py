# ==========================================================
# Astro IA
# Catalogue Filter
# Filtrage objets Siril pour analyse IA
# ==========================================================


import re



# ==========================================================
# TYPES OBJETS INTERESSANTS
# ==========================================================


DEEP_SKY_TYPES = [

    "galaxy",
    "gx",

    "nebula",
    "neb",

    "planetarynebula",
    "planetary nebula",
    "pn",

    "opencluster",
    "open cluster",
    "oc",

    "globularcluster",
    "globular cluster",
    "gc",

    "cluster"

]



STAR_TYPES = [

    "star",
    "variable",
    "variable star",
    "v*"

]



# ==========================================================
# OBJETS CATALOGUES
# ==========================================================


CATALOG_PATTERNS = [

    r"^M\s*\d+",
    r"^NGC\s*\d+",
    r"^IC\s*\d+",

    r"^SH2[- ]?\d+",
    r"^SH\s*2[- ]?\d+",

    r"^LBN\s*\d+",
    r"^LDN\s*\d+"

]



# ==========================================================
# NORMALISATION TEXTE
# ==========================================================


def normalize(value):


    if value is None:

        return ""


    return (

        str(value)

        .lower()

        .replace("_", "")

        .replace("-", "")

        .replace(" ", "")

    )



# ==========================================================
# MAGNITUDE
# ==========================================================


def get_magnitude(obj):


    keys = [

        "MAG",
        "mag",

        "MAGNITUDE",
        "Magnitude",

        "VMAG",
        "Vmag",

        "V_MAG",

        "FLUX"

    ]


    for key in keys:


        if key in obj:


            try:

                return float(obj[key])


            except:

                pass



    return None



# ==========================================================
# TYPE OBJET
# ==========================================================


def get_type(obj):


    keys = [

        "TYPE",
        "type",

        "OTYPE",
        "otype",

        "OBJTYPE",

        "ObjectType",

        "CLASS"

    ]


    for key in keys:


        if key in obj:

            return str(obj[key])



    return "Unknown"



# ==========================================================
# NOM
# ==========================================================


def get_name(obj):


    keys = [

        "NAME",

        "name",

        "MAIN_ID",

        "MAINID",

        "ID",

        "identifier",

        "OBJECT"

    ]


    for key in keys:


        if key in obj:


            value = str(obj[key])


            if value.strip():

                return value.strip()



    return "Unknown"



# ==========================================================
# DETECTION ETOILE PROBABLE
# ==========================================================


def looks_like_star(obj):


    name = get_name(obj).upper()


    mag = get_magnitude(obj)



    # Catalogue Gaia / HD / BD / TYC
    # avec position + magnitude
    # = très probablement étoile


    star_catalogs = [

        "HD",

        "BD",

        "TYC",

        "GSC",

        "UCAC",

        "GAIA"

    ]



    for catalog in star_catalogs:


        if name.startswith(catalog):

            return True



    return False



# ==========================================================
# OBJET CATALOGUE
# ==========================================================


def is_catalog_object(obj):


    name = get_name(obj).upper().strip()



    for pattern in CATALOG_PATTERNS:


        if re.match(pattern, name):

            return True



    return False



# ==========================================================
# DEEP SKY
# ==========================================================


def is_deep_sky(obj):


    obj_type = normalize(get_type(obj))



    for t in DEEP_SKY_TYPES:


        if normalize(t) in obj_type:

            return True



    return False



# ==========================================================
# ETOILES
# ==========================================================


def is_star(obj):


    obj_type = normalize(get_type(obj))



    for t in STAR_TYPES:


        if normalize(t) in obj_type:

            return True



    return looks_like_star(obj)



# ==========================================================
# SCORE IA
# ==========================================================


def object_score(obj):


    score = 0



    if is_catalog_object(obj):

        score += 100



    if is_deep_sky(obj):

        score += 60



    mag = get_magnitude(obj)



    if mag is not None:


        if mag < 8:

            score += 30


        elif mag < 12:

            score += 25


        elif mag < 16:

            score += 10



    if is_star(obj):

        score -= 20



    return score



# ==========================================================
# FILTRAGE PRINCIPAL
# ==========================================================


def filter_catalog(

    objects,

    max_mag=16.0,

    max_objects=50

):


    filtered = []



    for obj in objects:



        mag = get_magnitude(obj)



        if mag is not None:


            if mag > max_mag:

                continue



        if (

            is_deep_sky(obj)

            or

            is_catalog_object(obj)

            or

            (
                is_star(obj)
                and
                mag is not None
                and
                mag < 8
            )

        ):


            filtered.append(obj)



    filtered.sort(

        key=object_score,

        reverse=True

    )



    return filtered[:max_objects]



# ==========================================================
# RESUME POUR OLLAMA
# ==========================================================


def create_ai_summary(objects):


    if not objects:


        return (

            "Aucun objet remarquable "
            "détecté par Siril."

        )



    lines = []



    for obj in objects:


        name = get_name(obj)

        obj_type = get_type(obj)

        mag = get_magnitude(obj)

        score = object_score(obj)



        if mag is not None:


            lines.append(

                f"- {name} | "
                f"type={obj_type} | "
                f"mag={mag:.2f} | "
                f"score={score}"

            )


        else:


            lines.append(

                f"- {name} | "
                f"type={obj_type} | "
                f"score={score}"

            )



    return "\n".join(lines)