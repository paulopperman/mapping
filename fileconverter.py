"""
Convert shapefiles to GeoJSON for easy mapping on GitHub

based on https://gist.github.com/frankrowe/6071443

RI Projection data is in on NAD 1983 StatePlane RI FIPS 3800 Feet.  EPSG 102730
Use pyproj to transform, and don't forget to set preserve_units=True! https://github.com/jswhit/pyproj/issues/67

+proj=tmerc +lat_0=41.08333333333334 +lon_0=-71.5 +k=0.99999375 +x_0=100000 +y_0=0 +datum=NAD83 +units=us-ft +no_defs

Data sources:
RIPTA - RIPTA routes http://www.rigis.org/data/RIPTAroutes
LUSTS - Leaky underground storage tanks http://www.rigis.org/data/LUSTs
"""

import shapefile
from pyproj import Proj
from mapfile_tools import change_proj

# import path strings to the location of the shape data
from localfiles import RIPTA, LUSTS

# define projection to convert to lon-lat
NAD_1983_RI_string = '+proj=tmerc +lat_0=41.08333333333334 +lon_0=-71.5 +k=0.99999375 +x_0=100000 +y_0=0 +datum=NAD83 +units=us-ft +no_defs'
# ri_state = Proj( NAD_1983_RI_string, preserve_units=True)

reader = shapefile.Reader(LUSTS)
fields = reader.fields[1:]
field_names = [field[0] for field in fields]
buffer = []

# TODO: tuples don't get written to valid json, need to get the geo_interface changed to dict or nested lists

for sr in reader.shapeRecords():
    atr = dict(zip(field_names, sr.record))
    geom = sr.shape.__geo_interface__
    geom = change_proj(geom,NAD_1983_RI_string)
    if geom['type'] == 'Point':
        geom['coordinates'] = list(geom['coordinates'])
    buffer.append(dict(type="Feature", geometry=geom, properties=atr))

buffer = str(buffer)
# write the GeoJSON file
from json import dumps

geojson = open("test-2.geojson", "w")
geojson.write(dumps({"type": "FeatureCollection", "features": buffer}, indent=2) + "\n")
geojson.close()
