"""Plot the elevation and doppler shift of the ISS over one pass"""

import matplotlib.pyplot as plt
import numpy as np
from skyfield.api import load, wgs84

from ldp.config import load_config
from ldp.orbit import fetch_tle, observer_geometry, doppler_shift

config = load_config()
sat=config["satellite"]
obs=config["observer"]
ts=load.timescale()
iss=fetch_tle(sat["norad_id"],"data/tle/iss.tle")
observer=wgs84.latlon(obs["lat_deg"], obs["lon_deg"], obs["alt_m"])

seconds =np.arange(0,1200)
times=ts.utc(2026,11,26,10,20,seconds)

elevation_deg, range_m, range_rate_m_s=observer_geometry(iss,observer,times)
shift_hz=doppler_shift(sat["downlink_freq_hz"], range_rate_m_s)
minutes=seconds/60

fig, (ax_el, ax_dop) = plt.subplots(2, 1, sharex=True, figsize=(8, 6))

ax_el.plot(minutes, elevation_deg)
ax_el.axhline(0, color="gray", linestyle="--")
ax_el.set_ylabel("Elevation (deg)")

ax_dop.plot(minutes, shift_hz / 1000)
ax_dop.axhline(0, color="gray", linestyle="--")
ax_dop.set_ylabel("Doppler shift (kHz)")
ax_dop.set_xlabel("Minutes after 10:20 UTC")

fig.suptitle("ISS pass, 2026-11-26, downlink 145.8 MHz")
plt.show()