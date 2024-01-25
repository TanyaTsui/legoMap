import ee
import streamlit as st
import geemap.foliumap as geemap
import folium
from haversine import haversine

st.set_page_config(layout="wide")
st.title("Make your own Lego map!")
st.markdown(
    """
    Want to make your own lego map? Then use the map below to select an area of interest :) 
    """
)

# add default basemap 
m = geemap.Map()
m.add_basemap("OpenTopoMap")

# add widget for bbox coordinates
bbox = st.text_input("Enter the bounding box coordinates (format: xmin,ymin,xmax,ymax):")

if bbox:
    # get bbox coordinates
    xmin, ymin, xmax, ymax = map(float, bbox.split(','))
    bbox = ee.Geometry.Rectangle([xmin, ymin, xmax, ymax])
else: 
    bbox_default = "3.314971144228537, 50.80372101501057, 7.092053144228537, 53.55754301501057"
    xmin, ymin, xmax, ymax = map(float, bbox_default.split(',')) # default bbox coordinates
    bbox = ee.Geometry.Rectangle([xmin, ymin, xmax, ymax])

# get landcover data from Copernicus as ee.ImageCollection
dataset = ee.ImageCollection("COPERNICUS/Landcover/100m/Proba-V-C3/Global").filterDate("2019-01-01", "2019-12-31")
landcover = dataset.filter(ee.Filter.eq("system:index", "2019")).first() 
landcover = landcover.select("discrete_classification")

# get length and width of bbox in meters
bbox_length = haversine((xmin, ymin), (xmax, ymin)) * 1000
bbox_width = haversine((xmin, ymin), (xmin, ymax)) * 1000
bbox_dim = max(bbox_length, bbox_width)

# reproject and clip landcover data
landcover = landcover.reproject(crs="EPSG:4326", scale=bbox_dim/150)
landcover = landcover.clip(bbox)
m.addLayer(landcover, {}, "Landcover")

# display the map
m.to_streamlit(height=500)

# china_bbox = [73.446960, 18.197700, 135.085000, 53.560860]
# hk_bbox = [113.8259, 22.1534, 114.5025, 22.5619]
# netherlands_bbox = [3.314971144228537, 50.80372101501057, 7.092053144228537, 53.55754301501057]