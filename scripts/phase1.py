from ldp.orbit import fetch_tle, observer_geometry
from ldp.config import load_config
from skyfield.api import wgs84, load

iss=fetch_tle(25544, "data/tle/iss.tle")
print(iss)

ts=load.timescale() #its lika loaded clock
config=load_config()
obs=config["observer"] #just taking the observer section in the dictionary
observer=wgs84.latlon(obs["lat_deg"], obs["lon_deg"], obs["alt_m"])
#putting observer's real coords into a observer object

t=ts.now()
elevation_deg, range_m, range_rate_m_s=observer_geometry(iss,observer,t)

print("Time (UTC):", t.utc_strftime())
print(f"Elevation:  {elevation_deg:.1f} deg")
print(f"Range:      {range_m / 1000:.0f} km")
print(f"Range rate: {range_rate_m_s:.0f} m/s")