# Property Tax Analysis vs LVT in Python

# This file is initial analysis, not for web hosting quite yet.

import pandas as pd
import geopandas as gpd
import os

# --- Constants for Calculation ---
MILLAGE_RATE = 69.138606  # Cincinnati rate in mills ($ per $1000 of assessed value)
ASSESSMENT_RATIO = 0.35  # Hamilton County Assessment Ratio (35% of FMV)

## 1. Data Loading and Joining
print("Loading data...")

# A. Load Attribute Data (CSV)
csv_path = "data/parcels/Quarterly_Open_Data_-5284588662096697165.csv"
try:
    df_attr = pd.read_csv(csv_path, encoding='latin1', low_memory=False)
except FileNotFoundError:
    print(f"Error: CSV file not found at {csv_path}. Please check the path.")
    exit()

# B. Load Geographic Data (Shapefile)
# GeoPandas only needs the path to the .shp file to load the entire shapefile set
shapefile_dir = "data/parcels/shape/"
shapefile_name = None

# Find the .shp file in the directory
for file in os.listdir(shapefile_dir):
    if file.endswith(".shp"):
        shapefile_name = file
        break

if not shapefile_name:
    print(f"Error: No .shp file found in {shapefile_dir}. Please check the directory contents.")
    exit()

shp_path = os.path.join(shapefile_dir, shapefile_name)

try:
    gdf_geo = gpd.read_file(shp_path)
except Exception as e:
    print(f"Error loading shapefile: {e}")
    exit()

print(f"Loaded {len(df_attr)} attribute records and {len(gdf_geo)} geographic features.")

# C. Prepare for Joining
# We need a common key to join the attribute data (df_attr) with the geographic data (gdf_geo).
# Assuming the unique parcel identifier is present in both datasets. 
# Common names for this field include 'PARCEL_ID', 'APN', 'FID', or similar.
# **ACTION REQUIRED:** You will need to inspect your files to confirm the column name