# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 14:00:22 2025

@author: Matthew
"""
from neo4j import GraphDatabase
import csv
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# CONFIG
# -----------------------------
NEO4J_URI = "neo4j://127.0.0.1:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "Westlondon"

DATA_FOLDER = r"C:\Users\Matthew\OneDrive\Desktop\MMA\MGTA 603- Data Mgmt & Org\Final Project\data"

STOPS_FILE = f"{DATA_FOLDER}\\stops_nodes.csv"
STOP_MAP_FILE = f"{DATA_FOLDER}\\stop_map.csv"
EDGES_FILE = f"{DATA_FOLDER}\\stop_time_rels.csv"

# -----------------------------
# CONNECT TO NEO4J
# -----------------------------
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

# -----------------------------
# LOAD NODES
# -----------------------------
with driver.session() as session:
    print("Loading Stop nodes into Neo4j...")
    with open(STOPS_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            session.run(
                "MERGE (:Stop {id:$id, name:$name, lat:$lat, lon:$lon})",
                id=int(row[':ID(Stop)']),
                name=row['name'],
                lat=float(row['lat:FLOAT']),
                lon=float(row['lon:FLOAT'])
            )
    print("Finished loading Stop nodes.")


# -----------------------------
# LOAD EDGES (BATCHED)
# -----------------------------
BATCH_SIZE = 50000  # you can adjust this based on memory/performance
count = 0
batch = []

with driver.session() as session:
    print("Loading NEXT_STOP edges into Neo4j (batched)...")
    with open(EDGES_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            batch.append({
                'start': int(row[':START_ID(Stop)']),
                'end': int(row[':END_ID(Stop)']),
                'trip': row['trip_id'],
                'dep': row['departure_time'],
                'arr': row['arrival_time']
            })
            count += 1

            if len(batch) >= BATCH_SIZE:
                session.run("""
                    UNWIND $rows AS row
                    MATCH (a:Stop {id: row.start}), (b:Stop {id: row.end})
                    MERGE (a)-[:NEXT_STOP {
                        trip_id: row.trip,
                        departure_time: row.dep,
                        arrival_time: row.arr
                    }]->(b)
                """, rows=batch)
                batch = []
                print(f"Processed {count} edges...")

        # process remaining edges
        if batch:
            session.run("""
                UNWIND $rows AS row
                MATCH (a:Stop {id: row.start}), (b:Stop {id: row.end})
                MERGE (a)-[:NEXT_STOP {
                    trip_id: row.trip,
                    departure_time: row.dep,
                    arrival_time: row.arr
                }]->(b)
            """, rows=batch)
            print(f"Processed {count} edges (final batch)")

print("Finished loading NEXT_STOP edges.")


# -----------------------------
# SAMPLE ANALYSIS: Top 10 busiest stop-to-stop segments
# -----------------------------
with driver.session() as session:
    print("Running sample query: busiest edges...")
    query = """
    MATCH (a:Stop)-[r:NEXT_STOP]->(b:Stop)
    RETURN a.name AS from_stop, b.name AS to_stop, COUNT(r) AS trips
    ORDER BY trips DESC
    LIMIT 10
    """
    rows = session.run(query).data()

# Convert to DataFrame and plot
df = pd.DataFrame(rows)
plt.figure(figsize=(10,6))
df.plot(kind="bar", x="from_stop", y="trips", legend=False)
plt.title("Top 10 Busiest Stop-to-Stop Segments")
plt.xlabel("From Stop")
plt.ylabel("Number of Trips")
plt.tight_layout()
plt.show()

# -----------------------------
# CLOSE DRIVER
# -----------------------------
driver.close()
print("Neo4j connection closed.")
