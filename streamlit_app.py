#!/usr/bin/env python
# coding: utf-8

# In[3]:


import requests
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import rasterio
from rasterio.plot import show
from joblib import Memory  # For caching
import geopandas as gpd  # For geographic features
import streamlit as st
from streamlit_folium import folium_static  # To display Folium maps in Streamlit


# In[4]:


# Initialize caching
memory = Memory(location='./cache', verbose=0)


# ##  Fetch Earthquake Data from USGS API

# In[5]:


def fetch_earthquake_data(start_time, end_time, min_magnitude):
    """
    Fetches earthquake data from the USGS API.
    
    Parameters:
        start_time (str): Start date in YYYY-MM-DD format.
        end_time (str): End date in YYYY-MM-DD format.
        min_magnitude (float): Minimum magnitude of earthquakes to fetch.
    
    Returns:
        pd.DataFrame: Earthquake data.
    """
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": "geojson",
        "starttime": start_time,
        "endtime": end_time,
        "minmagnitude": min_magnitude
    }
    response = requests.get(url, params=params)
    data = response.json()
    return pd.json_normalize(data['features'])


# ##  Load Satellite Imagery with Caching

# In[6]:


@memory.cache
def load_satellite_imagery(satellite_image_path):
    """
    Loads satellite imagery from a GeoTIFF file.
    
    Parameters:
        satellite_image_path (str): Path to the GeoTIFF file.
    
    Returns:
        np.ndarray: Satellite image data.
    """
    with rasterio.open(satellite_image_path) as src:
        return src.read(1)


# ## Add Satellite Imagery to the Map

# In[7]:


def add_satellite_imagery(map, satellite_image_path):
    """
    Adds satellite imagery to the Folium map.
    
    Parameters:
        map (folium.Map): The Folium map object.
        satellite_image_path (str): Path to the GeoTIFF file.
    """
    if satellite_image_path:
        image = load_satellite_imagery(satellite_image_path)  # Use cached function
        with rasterio.open(satellite_image_path) as src:
            bounds = src.bounds
            folium.raster_layers.ImageOverlay(
                image=image,  # Use the cached image
                bounds=[[bounds.bottom, bounds.left], [bounds.top, bounds.right]],
                opacity=0.6,
                interactive=True,
                cross_origin=False,
                zindex=1,
            ).add_to(map)
    else:
        print("Skipping satellite imagery for quick testing.")


# ## Create an Interactive Map

# In[8]:


def create_interactive_map(earthquake_data):
    """
    Creates an interactive Folium map with earthquake markers.
    
    Parameters:
        earthquake_data (pd.DataFrame): Earthquake data.
    
    Returns:
        folium.Map: The Folium map object.
    """
    map = folium.Map(location=[-25, 135], zoom_start=4)
    marker_cluster = MarkerCluster().add_to(map)
    for _, row in earthquake_data.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"Magnitude: {row['properties.mag']}, Depth: {row['depth']} km",
            icon=folium.Icon(color='red')
        ).add_to(marker_cluster)
    return map


# In[9]:


# Streamlit app
def main():
    st.title("Earthquake Impact Visualization Tool")
    st.write("Visualize earthquake data and its environmental impact using satellite imagery.")

    # Sidebar for user inputs
    st.sidebar.header("User Inputs")
    start_time = st.sidebar.text_input("Start Date (YYYY-MM-DD)", "2013-01-01")
    end_time = st.sidebar.text_input("End Date (YYYY-MM-DD)", "2023-01-31")
    min_magnitude = st.sidebar.number_input("Minimum Magnitude", value=6.0)
    satellite_image_path = st.sidebar.text_input("Path to Satellite Imagery (GeoTIFF)", "NE1_LR_LC_SR.tif")

    # Fetch earthquake data
    if st.sidebar.button("Fetch Earthquake Data"):
        st.write("Fetching earthquake data...")
        earthquake_data = fetch_earthquake_data(start_time, end_time, min_magnitude)

        # Extract latitude, longitude, and depth
        earthquake_data['latitude'] = earthquake_data['geometry.coordinates'].apply(lambda x: x[1])
        earthquake_data['longitude'] = earthquake_data['geometry.coordinates'].apply(lambda x: x[0])
        earthquake_data['depth'] = earthquake_data['geometry.coordinates'].apply(lambda x: x[2])

        # Display earthquake data
        st.write("Earthquake Data Preview:")
        st.dataframe(earthquake_data.head())

        # Create the interactive map
        st.write("Creating interactive map...")
        map = create_interactive_map(earthquake_data)

        # Add satellite imagery
        add_satellite_imagery(map, satellite_image_path)

#         # Add geographic features
#         add_geographic_features(map)

        # Display the map
        st.write("Interactive Map:")
        folium_static(map)

        # Save the map to an HTML file
        map.save("earthquake_map_with_imagery.html")
        st.success("Map saved as earthquake_map_with_imagery.html")

# Run the Streamlit app
if __name__ == "__main__":
    main()


# In[ ]:




