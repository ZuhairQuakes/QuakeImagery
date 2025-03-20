# Earthquake Impact Visualization Tool

This Python tool integrates **USGS earthquake data** and **NASA satellite imagery** to visualize and analyze the impact of earthquakes on the environment. It fetches earthquake data, overlays it on satellite imagery, and provides insights into environmental changes caused by seismic activity.

---

## Features

- **Earthquake Data Integration**:
  - Fetches earthquake data from the USGS API.
  - Filters data by date range, magnitude, and region.

- **Satellite Imagery Integration**:
  - Fetches satellite imagery from NASA Earthdata or Google Earth Engine.
  - Overlays earthquake locations on the imagery.

- **Interactive Visualization**:
  - Creates an interactive map using `folium`.
  - Displays earthquake locations and satellite imagery.

- **Environmental Impact Analysis**:
  - Analyzes changes in land cover, vegetation, or surface deformation.

---

## Prerequisites

Before using this tool, ensure you have the following installed:

- **Python 3.8 or higher**
- **Required Python Libraries**:
  - `pandas`
  - `numpy`
  - `folium`
  - `rasterio`
  - `geopandas`
  - `matplotlib`
