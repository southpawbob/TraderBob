# Python (Flask) - server.py
from flask import Flask, jsonify, render_template
import networkx as nx

app = Flask(__name__)
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/graph_data')
def get_graph_data():
    # Generate graph data using NetworkX
    graph = nx.Graph()
    graph.add_edges_from([(1, 2), (2, 3), (3, 1)])
    data = nx.node_link_data(graph)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

