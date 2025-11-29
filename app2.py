from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from neo4j import GraphDatabase
import os

app = Flask(__name__)
CORS(app)

# ─── 1. CONNECT TO NEO4J ────────────────────────────────────────────────
NEO4J_URI = "neo4j://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = "Westlondon"
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))

# ─── 2. GET ALL STOPS ───────────────────────────────────────────────────
@app.route("/get_stops", methods=["GET"])
def get_stops():
    with driver.session() as session:
        q = """
        MATCH (s:Stop)
        RETURN s.id AS stop_id, s.name AS stop_name
        ORDER BY s.name
        """
        records = session.run(q)
        return jsonify([r.data() for r in records])

# ─── 3. SHORTEST PATH BETWEEN TWO STOPS ────────────────────────────────
@app.route("/shortest_path", methods=["GET"])
def shortest_path():
    origin = request.args.get("origin_stop_id")
    destination = request.args.get("destination_stop_id")
    if not origin or not destination:
        return jsonify({"error": "origin_stop_id and destination_stop_id required"}), 400

    query = """
    MATCH (start:Stop {id: $origin}), (end:Stop {id: $destination})
    MATCH p = shortestPath((start)-[:NEXT_STOP*]-(end))
    RETURN [n IN nodes(p) | n.name] AS path, length(p) AS distance
    """
    with driver.session() as session:
        result = session.run(query, origin=int(origin), destination=int(destination))
        data = [r.data() for r in result]
        return jsonify(data)

# ─── 4. TOP CENTRALITY STOPS ────────────────────────────────────────────
@app.route("/centrality", methods=["GET"])
def centrality():
    """
    Calculate degree centrality for each stop.
    - Degree centrality = number of directly connected stops
    - Works without GDS library
    Returns top 10 stops with highest centrality
    """
    query = """
    MATCH (s:Stop)-[:NEXT_STOP]->()
    RETURN s.name AS stop_name, COUNT(*) AS score
    ORDER BY score DESC
    LIMIT 10
    """
    with driver.session() as session:
        result = session.run(query)
        return jsonify([{"stop_name": r["stop_name"], "score": r["score"]} for r in result])


# ─── 5. REACHABLE STOPS WITHIN N HOPS ──────────────────────────────────
@app.route("/reachable_stops", methods=["GET"])
def reachable_stops():
    origin = request.args.get("origin_stop_id")
    hops = request.args.get("hops", 2)  # default 2 hops
    if not origin:
        return jsonify({"error": "origin_stop_id required"}), 400

    query = f"""
    MATCH (start:Stop {{id: $origin}})-[:NEXT_STOP*1..{int(hops)}]->(s:Stop)
    RETURN DISTINCT s.name AS stop_name
    ORDER BY s.name
    """
    with driver.session() as session:
        result = session.run(query, origin=int(origin))
        return jsonify([r["stop_name"] for r in result])

# ─── 6. SERVE INDEX.HTML ───────────────────────────────────────────────
@app.route("/")
def home():
    return send_from_directory("static", "index.html")

# ─── 7. RUN FLASK APP ──────────────────────────────────────────────────
if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    app.run(debug=True)
    
# ─── 8. NETWORK GRAPH DATA ─────────────────────────────────────────────
@app.route("/network_data", methods=["GET"])
def network_data():
    query = """
    MATCH (s1:Stop)-[:NEXT_STOP]->(s2:Stop)
    RETURN s1.id AS source_id, s1.name AS source_name,
           s2.id AS target_id, s2.name AS target_name
    """
    with driver.session() as session:
        result = session.run(query)
        nodes = {}
        links = []

        for r in result:
            # Add nodes
            nodes[r["source_id"]] = {"id": r["source_id"], "name": r["source_name"]}
            nodes[r["target_id"]] = {"id": r["target_id"], "name": r["target_name"]}

            # Add link
            links.append({"source": r["source_id"], "target": r["target_id"]})

        return jsonify({"nodes": list(nodes.values()), "links": links})