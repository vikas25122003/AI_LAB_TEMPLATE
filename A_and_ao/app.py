from flask import Flask, render_template, request, jsonify
import json
from a_star import AStarSearch
from ao_star import AOStarSearch

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_astar', methods=['POST'])
def run_astar():
    try:
        data = request.json
        graph_raw = data.get('graph')
        heuristics = data.get('heuristics')
        start = data.get('start')
        goal = data.get('goal')

        # Convert JSON graph to Python tuples
        # JSON: "A": [["B", 6], ["F", 3]]
        # Python: "A": [("B", 6), ("F", 3)]
        graph = {}
        for node, neighbors in graph_raw.items():
            graph[node] = [(n, w) for n, w in neighbors]

        solver = AStarSearch(graph, heuristics)
        path, cost = solver.algorithm(start, goal)
        
        if path:
            return jsonify({'status': 'success', 'path': path, 'cost': cost})
        else:
            return jsonify({'status': 'error', 'message': 'No path found'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/run_aostar', methods=['POST'])
def run_aostar():
    try:
        data = request.json
        graph_raw = data.get('graph')
        heuristics = data.get('heuristics')
        start = data.get('start')

        # Convert JSON graph to Python tuples for AO*
        # JSON: "A": [[["B", 1], ["C", 1]], [["D", 1]]]
        # Python: "A": [[("B", 1), ("C", 1)], [("D", 1)]]
        graph = {}
        for node, or_branches in graph_raw.items():
            graph[node] = []
            for and_branch in or_branches:
                graph[node].append([(n, w) for n, w in and_branch])

        solver = AOStarSearch(graph, heuristics, start)
        solver.ao_star(start, False)
        
        # Get solution structure as list of strings
        output_lines = solver.get_solution_structure(start)
        output_str = "\n".join(output_lines)
        min_cost = solver.heuristics[start]
        
        return jsonify({
            'status': 'success', 
            'output': output_str,
            'min_cost': min_cost
        })

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5006)
