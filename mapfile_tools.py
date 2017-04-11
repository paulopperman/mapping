"""
Some home-rolled utility functions for working with shapefiles
"""
from pyproj import Proj


def change_proj(geom, projection):
    # convert geojson geometry coordinates from projection to lat lon
    # projection is a proj4 string
    p = Proj(projection, preserve_units=True)
    geo_type = geom['type'] # get the type of geometry to allow for proper iterating
    if geo_type == 'Point':
        x,y = geom['coordinates']
        lon, lat = p(x, y, inverse=True)
        c = list([lon,lat])
    else:  # this currently is tested for a MultiLineString
        buffer = []
        for part in geom['coordinates']:
            x, y = list(zip(*list(part)))
            lons, lats = p(x, y, inverse=True)
            line_seg_coords = list(zip(lons, lats))
            buffer.append(line_seg_coords)
        c = list(buffer)

    new_geom = {'type':geo_type,'coordinates':c}

    return new_geom
