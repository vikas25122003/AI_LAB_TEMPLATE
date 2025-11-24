import heapq

class AStarSearch:
    def __init__(self, graph, heuristics):
        self.graph = graph
        self.heuristics = heuristics

    def get_neighbors(self, node):
        return self.graph.get(node, [])

    def get_heuristic(self, node):
        return self.heuristics.get(node, 1000) # Default high value if unknown

    def algorithm(self, start, goal):
        # Ensure goal heuristic is 0 (Critical for A*)
        self.heuristics[goal] = 0 
        
        # Priority Queue stores tuples: (f_cost, g_cost, current_node, path)
        open_list = [(0 + self.get_heuristic(start), 0, start, [start])]
        closed_set = set()

        while open_list:
            # Pop the node with the lowest f_cost
            f, g, current, path = heapq.heappop(open_list)

            if current == goal:
                return path, g  # Return path and total cost

            if current in closed_set:
                continue
            
            closed_set.add(current)

            for neighbor, weight in self.get_neighbors(current):
                if neighbor not in closed_set:
                    new_g = g + weight
                    new_f = new_g + self.get_heuristic(neighbor)
                    new_path = path + [neighbor]
                    heapq.heappush(open_list, (new_f, new_g, neighbor, new_path))
        
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
