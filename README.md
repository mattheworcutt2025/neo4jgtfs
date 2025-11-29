# neo4jgtfs
# Transit Graph Analytics — Neo4j Component

This project is part of the **Public Transit Data Platform** final project. This repository contains the Neo4j graph analytics component, including a web-based interface for exploring transit stops, routes, and network metrics.

## Project Overview

- **Purpose:** Analyze a transit network as a graph. Perform queries like shortest paths, reachable stops, and centrality.
- **Tech Stack:**
  - **Neo4j**: Graph database for modeling stops and connections
  - **HTML/CSS/JS**: Front-end interface with D3.js visualizations
  - **D3.js**: Force-directed graph visualization
  - **Python**: For integration, data cleaning, and running Cypher queries

## Folder Structure

> Note: `index.html` references files in `/static`. Make sure to keep the structure when cloning.

## Features

- **Autocomplete**: Search for origin and destination stops
- **Queries:**
  - Shortest path between two stops
  - Stops reachable within N hops
  - Top central stops (centrality)
- **Visualization:** Dynamic graph with zoom, drag, and layout
- **Responsive UI**: Works on desktop browsers

## Getting Started

1. **Run Neo4j**  
   Make sure your Neo4j instance is running and loaded with the transit data:
   - Nodes: `Stop`  
   - Relationships: `CONNECTED_TO` (edges between stops)

2. **Start a local server** (optional)  
   For testing `index.html` with fetch requests, you may need a local server (e.g., using Python):
   ```bash
   python -m http.server 8000
   ```
   Then open `http://localhost:8000` in a browser.

3. **Check API endpoints** (if using Flask or Python backend)  
   Example endpoints:
   - `/get_stops` — returns all stops
   - `/shortest_path` — shortest path between two stops
   - `/reachable_stops` — stops within N hops
   - `/centrality` — top central stops

4. **Open `index.html`**  
   Use your browser to interact with the network.

## Dependencies

- [Neo4j](https://neo4j.com/)  
- [D3.js v7](https://d3js.org/) (CDN included in HTML)  
- Optional: Python 3.x for API integration

## Usage

- Select query type: Shortest Path, Reachable Stops, or Centrality
- Input origin/destination stops
- Click **Run Query** to visualize results
- Graph supports drag and zoom

## Notes

- Ensure Neo4j is running with the correct dataset
- If using a backend, update the fetch URLs in `index.html`
- Use `/static` folder for local JS/CSS

## Authors

- [Your Name] — Neo4j & front-end implementation  
- Team Project — Public Transit Data Platform

## License

This project is for academic purposes and course submission only.
