"""
Convert shapefiles to GeoJSON for easy mapping on GitHub

based on https://gist.github.com/frankrowe/6071443

"""

import shapefile
from localfiles import SHPPATH

reader = shapefile.Reader(SHPPATH)
fields = reader.fields[1:]
field_names = [field[0] for field in fields]
buffer = []
for sr in reader.shapeRecords():
    atr = dict(zip(field_names, sr.record))
    geom = sr.shape.__geo_interface__
    buffer.append(dict(type="Feature", geometry=geom, properties=atr))

# insert for python 3 compatibility - https://groups.google.com/forum/#!topic/geospatialpython/7bZnpHkD7ys
buffer = str(buffer)
# write the GeoJSON file
from json import dumps

geojson = open("pyshp-demo.json", "w")
geojson.write(dumps({"type": "FeatureCollection", "features": buffer}, indent=2) + "\n")
geojson.close()
