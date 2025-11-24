import subprocess
import sys
import ast
import os

class AStarSearch:
    def __init__(self, graph, heuristics):
        self.graph = graph
        self.heuristics = heuristics

    def algorithm(self, start, goal):
        # 1. Generate Prolog Facts
        prolog_code = ":- dynamic edge/3, h/2.\n"
        
        # Convert Graph to Prolog Facts
        for node, neighbors in self.graph.items():
            for neighbor, cost in neighbors:
                # Escape strings to handle spaces/special chars
                prolog_code += f"edge('{node}', '{neighbor}', {cost}).\n"
        
        # Convert Heuristics
        for node, h_val in self.heuristics.items():
            prolog_code += f"h('{node}', {h_val}).\n"
            
        # 2. Include Solver and Define Goal
        # We use absolute path to ensure Prolog finds the solver
        solver_path = os.path.abspath("astar_solver.pl").replace("\\", "/")
        prolog_code += f":- consult('{solver_path}').\n"
        prolog_code += f"run :- solve_astar('{start}', '{goal}').\n"
        
        # 3. Write to temp file
        temp_file = "temp_astar.pl"
        with open(temp_file, "w") as f:
            f.write(prolog_code)
            
        # 4. Run SWI-Prolog
        try:
            # Command: swipl -s temp_astar.pl -g run -t halt
            result = subprocess.run(
                ["swipl", "-s", temp_file, "-g", "run", "-t", "halt"],
                capture_output=True, text=True
            )
            
            output = result.stdout
            # Parse "RESULT:['a','b']:10"
            if "RESULT:" in output:
                res_str = output.split("RESULT:")[1].strip()
                path_str, cost_str = res_str.split(":")
                
                # Convert string representation to Python objects
                # Prolog returns [rock_beach, white_town] (unquoted atoms)
                # We manually parse this to avoid ast.literal_eval errors on unquoted names
                clean_path = path_str.strip().strip("[]")
                if clean_path:
                    # Split by comma, strip whitespace and potential quotes
                    path = [x.strip().strip("'").strip('"') for x in clean_path.split(",")]
                else:
                    path = []
                
                cost = float(cost_str)
                return path, cost
            else:
                print("Prolog Output:", output)
                print("Prolog Error:", result.stderr)
                return None, float('inf')
                
        except FileNotFoundError:
            print("❌ Error: 'swipl' (SWI-Prolog) is not installed or not in PATH.")
            print("Please install SWI-Prolog to run this logic.")
            return None, float('inf')
        except Exception as e:
            print(f"Error running Prolog: {e}")
            return None, float('inf')

# ==========================================
#  USER CONFIGURATION SECTION (EDIT HERE)
# ==========================================

# 1. Define the Graph (Adjacency List)
# Format: 'Node': [('Neighbor', Cost), ...]
# Scenario: Pondicherry Racing (Cost = Distance or Risk Level)
my_graph = {
    'rock_beach':      [('white_town', 5), ('marina', 8)],
    'white_town':      [('rock_beach', 5), ('auroville', 12), ('pims_curve', 7)],
    'auroville':       [('white_town', 12), ('pondy_university', 4)],
    'marina':          [('rock_beach', 8), ('chunnabar', 10)],
    'pims_curve':      [('white_town', 7), ('pondy_university', 6)],
    'pondy_university':[('auroville', 4), ('pims_curve', 6), ('ptu', 3)],
    'chunnabar':       [('marina', 10), ('serenity_beach', 15)],
    'ptu':             [('pondy_university', 3)],
    'serenity_beach':  [('chunnabar', 15)]
}

# 2. Define Heuristics (Straight line distance approximation to Goal)
# Scenario: Estimated distance to 'ptu' (the Finish Line)
my_heuristics = {
    'rock_beach': 20,
    'white_town': 15,
    'auroville': 5,
    'marina': 18,
    'pims_curve': 8,
    'pondy_university': 2,
    'chunnabar': 25,
    'serenity_beach': 30,
    'ptu': 0  # Goal always has 0 heuristic
}

# 3. Define Start and Goal
start_node = 'rock_beach'
goal_node = 'ptu'

# ==========================================
#  MAIN EXECUTION (DO NOT EDIT BELOW)
# ==========================================
if __name__ == "__main__":
    solver = AStarSearch(my_graph, my_heuristics)
    print(f"Starting A* Search from {start_node} to {goal_node}...\n")
    
    path, cost = solver.algorithm(start_node, goal_node)
    
    if path:
        print("✅ Optimal Path Found:")
        print(" -> ".join(path))
        print(f"Total Cost (Risk/Distance): {cost}")
    else:
        print("❌ No path found.")
