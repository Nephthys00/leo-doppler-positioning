from ldp.orbit import fetch_tle

iss=fetch_tle(25544, "data/tle/iss.tle")
print(iss)