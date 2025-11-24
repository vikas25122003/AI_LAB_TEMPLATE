class AOStarSearch:
    def __init__(self, graph, heuristics, start_node):
        self.graph = graph
        self.heuristics = heuristics
        self.start_node = start_node
        self.solution_graph = {}

    def compute_minimum_cost(self, v):
        minimum_cost = float('inf')
        cost_to_child_list = {}
        
        # Iterate over possible AND/OR branches
        # graph[v] is a list of lists. Inner lists are AND conditions.
        # e.g. [[A, B], [C]] means (A AND B) OR (C)
        for path in self.graph.get(v, []):
            path_cost = 0
            node_list = []
            for child_node, weight in path:
                # Cost = Edge Weight + Heuristic of child (recursive update)
                path_cost += weight + self.heuristics.get(child_node, 0)
                node_list.append(child_node)
            
            if path_cost < minimum_cost:
                minimum_cost = path_cost
                cost_to_child_list[minimum_cost] = node_list
                
        return minimum_cost, cost_to_child_list

    def ao_star(self, v, backtracking):
        # print(f"Processing Node: {v} | Current Heuristic: {self.heuristics[v]}")
        
        # Compute cost for current node based on children
        min_cost, child_dict = self.compute_minimum_cost(v)
        
        # Update heuristic and solution graph
        self.heuristics[v] = min_cost
        
        if min_cost < float('inf'):
            best_children = child_dict[min_cost]
            self.solution_graph[v] = best_children
            
            if v != self.start_node:
                backtracking = True 

            # Recursive step: Expand best children
            for child in best_children:
                self.ao_star(child, backtracking)

    def get_solution_structure(self, node, level=0):
        """
        Returns the solution tree structure as a list of strings for display.
        """
        output = []
        indent = "  " * level
        arrow = "-> " if level > 0 else ""
        cost = self.heuristics.get(node, 0)
        output.append(f"{indent}{arrow}{node} (Cost: {cost})")
        
        if node in self.solution_graph:
            children = self.solution_graph[node]
            for child in children:
                output.extend(self.get_solution_structure(child, level + 1))
        return output

    def print_solution(self, node, level=0):
        """
        Recursively prints the solution tree in a readable format.
        """
        lines = self.get_solution_structure(node, level)
        for line in lines:
            print(line)

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
