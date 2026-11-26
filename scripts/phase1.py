from ldp.orbit import fetch_tle, observer_geometry, doppler_shift
from ldp.config import load_config
from skyfield.api import wgs84, load

config=load_config()

sat = config["satellite"]
iss = fetch_tle(sat["norad_id"], "data/tle/iss.tle") 
print(iss)

ts=load.timescale() #its lika loaded clock
obs=config["observer"] #just taking the observer section in the dictionary
observer=wgs84.latlon(obs["lat_deg"], obs["lon_deg"], obs["alt_m"])
#putting observer's real coords into a observer object

t=ts.now()
elevation_deg, range_m, range_rate_m_s=observer_geometry(iss,observer,t)

print("Time (UTC):", t.utc_strftime())
print(f"Elevation:  {elevation_deg:.1f} deg")
print(f"Range:      {range_m / 1000:.0f} km")
print(f"Range rate: {range_rate_m_s:.0f} m/s")


shift_hz=doppler_shift(sat["downlink_freq_hz"], range_rate_m_s)
print(f"Doppler at {sat['downlink_freq_hz'] / 1e6:.3f} MHz: {shift_hz:.0f} Hz")
