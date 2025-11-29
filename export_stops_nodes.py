# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 11:41:24 2025

@author: Matthew
"""

# export_stops_nodes.py
#stop_nodes.csv- ready for import
#stop_map.csv integer mapping for relationship creation
import csv
import os
import zipfile

# -----------------------------
# PATHS
# -----------------------------
zip_path = r"C:\Users\Matthew\OneDrive\Desktop\MMA\MGTA 603- Data Mgmt & Org\dataset.zip"
extract_to = r"C:\Users\Matthew\OneDrive\Desktop\MMA\MGTA 603- Data Mgmt & Org\gtfs"
output_folder = r"C:\Users\Matthew\OneDrive\Desktop\MMA\MGTA 603- Data Mgmt & Org\Final Project\data"

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

nodes_out = os.path.join(output_folder, 'stops_nodes.csv')
map_out   = os.path.join(output_folder, 'stop_map.csv')

# -----------------------------
# EXTRACT GTFS
# -----------------------------
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_to)

print("Extracted GTFS files to:", extract_to)

# -----------------------------
# PROCESS STOPS
# -----------------------------
infile = os.path.join(extract_to, 'stops.txt')

with open(infile, newline='', encoding='utf-8') as inf, \
     open(nodes_out, 'w', newline='', encoding='utf-8') as nof, \
     open(map_out, 'w', newline='', encoding='utf-8') as mof:

    r = csv.DictReader(inf)
    node_writer = csv.writer(nof)
    map_writer = csv.writer(mof)

    node_writer.writerow([':ID(Stop)', 'stop_id', 'name', 'lat:FLOAT', 'lon:FLOAT'])
    map_writer.writerow(['stop_id', 'int_id'])

    idx = 0
    for row in r:
        stop_id = row.get('stop_id')
        name = row.get('stop_name', '')
        lat = row.get('stop_lat', '')
        lon = row.get('stop_lon', '')

        node_writer.writerow([idx, stop_id, name, lat, lon])
        map_writer.writerow([stop_id, idx])
        idx += 1

print("wrote", nodes_out, "and", map_out)