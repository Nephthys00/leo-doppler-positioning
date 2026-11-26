"""Orbit utilities: TLE loading, satellite geometry and Doppler prediction."""
from pathlib import Path

from skyfield.api import EarthSatellite, load

CELESTRAK_URL = "https://celestrak.org/NORAD/elements/gp.php"

def fetch_tle(norad_id: int, path: str, max_age_days:float=1.0) -> EarthSatellite: 
    """Load a satellite from a local TLE file, download it if it is not present or too old."""
    if not load.exists(path) or load.days_old(path) > max_age_days:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        url = f"{CELESTRAK_URL}?CATNR={norad_id}&FORMAT=TLE"

        try:
            load.download(url, filename=path)
        except Exception as error:
            print("Download failed, using the saved TLE:", error)

    return load.tle_file(path)[0]



from skyfield.timelib import Time
from skyfield.toposlib import GeographicPosition

def observer_geometry(satellite: EarthSatellite, observer: GeographicPosition, times: Time) -> tuple:
    """Return elevation (deg), range (m) and range rate (m/s) of a satellite seen from an observer."""
    topocentric= (satellite-observer).at(times) #a vector from the observer to the satellite
    elevation, _, distance, _, _, range_rate = topocentric.frame_latlon_and_rates(observer) 
    #Returns (elevation, azimuth, distance, elevation rate, azimuth rate, range rate); we keep 3
    return elevation.degrees, distance.m, range_rate.m_per_s

