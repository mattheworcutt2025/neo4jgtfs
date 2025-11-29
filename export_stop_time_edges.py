# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 13:12:18 2025

@author: Matthew
"""

# export_stop_time_edges.py
import csv
import os

# -----------------------------
# FILE PATHS
# -----------------------------
gtfs_folder = r"C:\Users\Matthew\OneDrive\Desktop\MMA\MGTA 603- Data Mgmt & Org\gtfs"
output_folder = r"C:\Users\Matthew\OneDrive\Desktop\MMA\MGTA 603- Data Mgmt & Org\Final Project\data"

stop_times_file = os.path.join(gtfs_folder, "stop_times.txt")
stop_map_file   = os.path.join(output_folder, "stop_map.csv")
edges_out       = os.path.join(output_folder, "stop_time_rels.csv")

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# -----------------------------
# LOAD stop_map
# -----------------------------
stop_map = {}
with open(stop_map_file, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        stop_map[row['stop_id']] = int(row['int_id'])

print("Loaded stop_map with", len(stop_map), "stops")

# -----------------------------
# CREATE EDGES
# -----------------------------
with open(edges_out, 'w', newline='', encoding='utf-8') as outf:
    writer = csv.writer(outf)
    writer.writerow([':START_ID(Stop)', ':END_ID(Stop)', 'trip_id', 'departure_time', 'arrival_time'])

    with open(stop_times_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        current_trip = None
        stops_in_trip = []

        for row in reader:
            trip_id = row['trip_id']
            stop_id = row['stop_id']
            arrival_time = row['arrival_time']
            departure_time = row['departure_time']

            if trip_id != current_trip:
                for i in range(len(stops_in_trip)-1):
                    s1 = stops_in_trip[i]
                    s2 = stops_in_trip[i+1]
                    writer.writerow([s1['int_id'], s2['int_id'], s1['trip_id'], s1['departure_time'], s2['arrival_time']])
                stops_in_trip = []
                current_trip = trip_id

            stops_in_trip.append({
                'trip_id': trip_id,
                'stop_id': stop_id,
                'int_id': stop_map[stop_id],
                'arrival_time': arrival_time,
                'departure_time': departure_time
            })

        for i in range(len(stops_in_trip)-1):
            s1 = stops_in_trip[i]
            s2 = stops_in_trip[i+1]
            writer.writerow([s1['int_id'], s2['int_id'], s1['trip_id'], s1['departure_time'], s2['arrival_time']])

print("Wrote stop_time_rels.csv to", edges_out)