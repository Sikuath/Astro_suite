# ==========================================================
# Astro Suite
# core/astro_ephemeris.py
#
# Calcul contexte observation astronomique
#
# FITS HEADER ->
# altitude cible
# azimut
# airmass
# soleil
# lune
# ==========================================================


from astropy.coordinates import (
    SkyCoord,
    EarthLocation,
    AltAz,
    get_body,
    get_sun
)


from astropy.time import Time


import astropy.units as u


from astroplan import Observer





# ==========================================================
# CREATION OBSERVATEUR
# ==========================================================

def build_observer(header):

    """
    Création observatoire depuis header FITS.
    """

    try:

        lat = header.get("SITELAT")
        lon = header.get("SITELONG")


        if lat is None or lon is None:

            return None



        return Observer(

            location=EarthLocation(

                lat=float(lat) * u.deg,

                lon=float(lon) * u.deg,

                height=0 * u.m

            ),

            name="Astro Suite"

        )


    except Exception:

        return None





# ==========================================================
# DATE OBSERVATION
# ==========================================================

def get_observation_time(header):


    date_obs = header.get(
        "DATE-OBS"
    )


    if not date_obs:

        return None



    try:

        return Time(

            date_obs,

            format="isot",

            scale="utc"

        )


    except Exception:

        return None





# ==========================================================
# CALCUL AIR MASS SIMPLE
# ==========================================================

def estimate_airmass(altitude):

    """
    Approximation simple de masse d'air.
    """

    try:

        alt = float(
            altitude
        )


        if alt <= 0:

            return None



        import math


        zenith_angle = 90 - alt


        value = (

            1 /

            math.cos(

                math.radians(
                    zenith_angle
                )

            )

        )


        return float(
            round(
                value,
                2
            )
        )


    except Exception:

        return None





# ==========================================================
# EPHEMERIDES COMPLETES
# ==========================================================

def build_ephemeris(header):

    """
    Construit les données observationnelles.
    """



    if not header:

        return {}



    observer = build_observer(
        header
    )


    obs_time = get_observation_time(
        header
    )



    if observer is None or obs_time is None:

        return {}



    try:


        ra = header.get(
            "RA"
        )


        dec = header.get(
            "DEC"
        )


        if ra is None or dec is None:

            return {}



        target = SkyCoord(

            ra=float(ra) * u.deg,

            dec=float(dec) * u.deg,

            frame="icrs"

        )



        frame = AltAz(

            obstime=obs_time,

            location=observer.location

        )



        # --------------------------------------------------
        # CIBLE
        # --------------------------------------------------

        target_altaz = target.transform_to(
            frame
        )



        # --------------------------------------------------
        # SOLEIL
        # --------------------------------------------------

        sun = get_sun(
            obs_time
        )


        sun_altaz = sun.transform_to(
            frame
        )



        # --------------------------------------------------
        # LUNE
        # --------------------------------------------------

        moon = get_body(

            "moon",

            obs_time,

            observer.location

        )


        moon_altaz = moon.transform_to(
            frame
        )



        moon_icrs = moon.transform_to(
            "icrs"
        )


        moon_distance = target.separation(
            moon_icrs
        )



        night = (

            float(
                sun_altaz.alt.deg
            )

            <

            -18

        )



        return {


            "target": {


                "altitude_deg":

                    float(
                        round(
                            target_altaz.alt.deg,
                            2
                        )
                    ),


                "azimuth_deg":

                    float(
                        round(
                            target_altaz.az.deg,
                            2
                        )
                    ),


                "airmass":

                    estimate_airmass(
                        target_altaz.alt.deg
                    )


            },



            "sun": {


                "altitude_deg":

                    float(
                        round(
                            sun_altaz.alt.deg,
                            2
                        )
                    ),


                "astronomical_night":

                    bool(
                        night
                    )


            },



            "moon": {


                "altitude_deg":

                    float(
                        round(
                            moon_altaz.alt.deg,
                            2
                        )
                    ),


                "azimuth_deg":

                    float(
                        round(
                            moon_altaz.az.deg,
                            2
                        )
                    ),


                "distance_target_deg":

                    float(
                        round(
                            moon_distance.deg,
                            2
                        )
                    )


            }


        }



    except Exception as e:


        return {

            "error": str(e)

        }







# ==========================================================
# TEST LOCAL
# ==========================================================

if __name__ == "__main__":


    import json



    header_test = {


        "RA":

            304.240809914361,


        "DEC":

            41.9586459458434,



        "SITELAT":

            43.1241,



        "SITELONG":

            1.61502,



        "DATE-OBS":

            "2025-08-08T23:16:00.761735"


    }



    result = build_ephemeris(

        header_test

    )



    print(

        json.dumps(

            result,

            indent=4,

            ensure_ascii=False

        )

    )