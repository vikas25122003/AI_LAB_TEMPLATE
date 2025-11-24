import subprocess
import sys
import ast
import os

class AOStarSearch:
    def __init__(self, graph, heuristics, start_node):
        self.graph = graph
        self.heuristics = heuristics
        self.start_node = start_node
        self.solution_graph = {} # Not used in Prolog version but kept for compatibility
        self.min_cost = 0
        self.solution_structure = ""

    def ao_star(self, v, backtracking):
        # This method now acts as the bridge to Prolog
        
        # 1. Generate Prolog Facts
        prolog_code = ":- dynamic branch/2, h/2.\n"
        
        # Convert AND-OR Graph to Prolog Facts
        # Python: 'A': [[('B', 1), ('C', 1)], [('D', 1)]]
        # Prolog: branch('A', ['B'-1, 'C'-1]). branch('A', ['D'-1]).
        for node, or_branches in self.graph.items():
            for and_branch in or_branches:
                # and_branch is list of (Child, Cost)
                children_str_list = []
                for child, cost in and_branch:
                    children_str_list.append(f"'{child}'-{cost}")
                
                children_prolog = "[" + ", ".join(children_str_list) + "]"
                prolog_code += f"branch('{node}', {children_prolog}).\n"
        
        # Convert Heuristics
        for node, h_val in self.heuristics.items():
            prolog_code += f"h('{node}', {h_val}).\n"
            
        # 2. Include Solver
        solver_path = os.path.abspath("aostar_solver.pl").replace("\\", "/")
        prolog_code += f":- consult('{solver_path}').\n"
        prolog_code += f"run :- solve_aostar('{v}').\n"
        
        # 3. Write temp file
        temp_file = "temp_aostar.pl"
        with open(temp_file, "w") as f:
            f.write(prolog_code)
            
        # 4. Run SWI-Prolog
        try:
            result = subprocess.run(
                ["swipl", "-s", temp_file, "-g", "run", "-t", "halt"],
                capture_output=True, text=True
            )
            
            output = result.stdout
            # Parse "RESULT:Cost:TreeString"
            if "RESULT:" in output:
                res_str = output.split("RESULT:")[1].strip()
                # Split only on first colon to separate cost from tree
                parts = res_str.split(":", 1)
                if len(parts) == 2:
                    self.min_cost = float(parts[0])
                    self.solution_structure = parts[1]
                    # Update heuristics for compatibility
                    self.heuristics[v] = self.min_cost
            else:
                print("Prolog Output:", output)
                print("Prolog Error:", result.stderr)
                
        except FileNotFoundError:
            print("❌ Error: 'swipl' (SWI-Prolog) is not installed.")
        except Exception as e:
            print(f"Error running Prolog: {e}")

    def get_solution_structure(self, node, level=0):
        # In Prolog version, we get the structure string directly
        # We wrap it in a list to match the expected interface of app.py
        return [str(self.solution_structure)]

    def print_solution(self, node, level=0):
        print(self.solution_structure)

# ==========================================
#  USER CONFIGURATION SECTION (EDIT HERE)
# ==========================================

# 1. Define the AND-OR Graph
# Format: 'Node': [[('Child1', EdgeCost), ('Child2', EdgeCost)], [('Child3', EdgeCost)]]
# Explanation: To solve 'Node', you must solve (Child1 AND Child2) OR (Child3)
# Scenario: Battle Royale Survival Strategy
# "To survive (root), I can (Loot AND Hide) OR (Fight)"
my_and_or_graph = {
    'survive': [
        [('loot_white_town', 2), ('hide_forest', 3)], # Option A: Defensive
        [('fight_rock_beach', 10)]                    # Option B: Aggressive
    ],
    'loot_white_town': [
        [('find_medkit', 1)], [('find_ammo', 2)]      # Sub-options
    ],
    'hide_forest': [
        [('stay_quiet', 1)]                           # Leaf node
    ],
    'fight_rock_beach': [
        [('win_duel', 5)]                             # Leaf node
    ]
    # Note: Leaf nodes are those not defined as keys or have empty lists
}

# 2. Define Heuristics (Estimated Cost to Complete)
# Leaf nodes must have specific values. Intermediate nodes can start at 0.
my_heuristics = {
    'survive': 0,
    'loot_white_town': 0,
    'hide_forest': 0,
    'fight_rock_beach': 0,
    'find_medkit': 2,
    'find_ammo': 4,
    'stay_quiet': 1,
    'win_duel': 20  # High cost/risk
}

start_node = 'survive'

# ==========================================
#  MAIN EXECUTION (DO NOT EDIT BELOW)
# ==========================================
if __name__ == "__main__":
    print(f"Starting AO* Search Strategy for: {start_node}\n")
    solver = AOStarSearch(my_and_or_graph, my_heuristics, start_node)
    solver.ao_star(start_node, False)

    print("\n✅ Final Optimal Strategy:")
    print(f"Minimum Cost to '{start_node}': {solver.heuristics[start_node]}")
    print("-" * 40)
    solver.print_solution(start_node)
    print("-" * 40)
