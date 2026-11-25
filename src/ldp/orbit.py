"""Orbit utilities: TLE loading, satellite geometry and Doppler prediction."""
from pathlib import Path

from skyfield.api import EarthSatellite, load

CELESTRAK_URL = "https://celestrak.org/NORAD/elements/gp.php"

def fetch_tle(norad_id: int, path: str, max_age_days:float=1.0) -> EarthSatellite: 
#load a satellite from a local TLE file, download it if it is not present or too old
    if not load.exists(path) or load.days_old(path) > max_age_days:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        url = f"{CELESTRAK_URL}?CATNR={norad_id}&FORMAT=TLE"

        try:
            load.download(url, filename=path)
        except Exception as error:
            print("Download failed, using the saved TLE:", error)

    return load.tle_file(path)[0]