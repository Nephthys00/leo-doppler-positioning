"""Print the current  position of the ISS from fresh TLE"""
import requests
from skyfield.api import EarthSatellite, load, wgs84 
#earthsatellite for creating a satellite object which takes the TLE data
#load for loading the timescale and other data
#wgs84 is the accurate model of earth's shape and size

URL="https://celestrak.org/NORAD/elements/gp.php"

response= requests.get(URL, params={"CATNR":25544, "FORMAT":"TLE"},timeout=20)
#it gets the TLE data for the ISS from Celestrak from the URl I gave
response.raise_for_status()
print(response.text)

lines = response.text.strip().splitlines() #splitlines() splits the text into a list of lines
#strip() removes any leading or trailing whitespace from the text
ts=load.timescale() #load the timescale from skyfield
iss=EarthSatellite(lines[1], lines[2], lines[0].strip(), ts  )
print(iss)

t=ts.now() #get the current time
position=iss.at(t) #where are you at t? get the position of the ISS at the current time
lat, lon =wgs84.latlon_of(position)
height = wgs84.height_of(position)
#as we dont know where the ISS is at the moment, we use the last location of the ISS and its time to
#calculate the current position of the ISS using the TLE data and its orbit

print("Time (UTC):",t.utc_strftime())
print(f"Latitude: {lat.degrees:.2f} deg")
print(f"Longitude: {lon.degrees:.2f} deg")
print(f"Height: {height.km:.1f} km")
