import subprocess
import os

# ==============================================================================
#   1. MAP CONFIGURATION (The Graph)
# ==============================================================================
# Define the connections and costs (Distance/Risk)
my_graph = {
    'rock_beach':       [('white_town', 2), ('beach_road', 3)],
    'white_town':       [('auroville_forest', 5)],
    'beach_road':       [('marina', 4)],
    'auroville_forest': [('pondy_university', 6)],
    'marina':           [('pims_curve', 7)],
    'pims_curve':       [('ring_road', 3)],
    'pondy_university': [('ptu', 2)],
    'ring_road':        [('chunnabar_bridge', 4)],
    'ptu':              [('serenity_beach', 3)],
    'chunnabar_bridge': [('serenity_beach', 5)],
    'serenity_beach':   [] 
}

START_NODE = 'rock_beach'
GOAL_NODE  = 'serenity_beach'

# ==============================================================================
#   2. CUSTOM PROLOG LOGIC (The "Brain")
# ==============================================================================
# PASTE ANY FACTS OR RULES HERE BASED ON THE QUESTION.
# You can define 'is_valid_step(X)' to filter paths.

CUSTOM_PROLOG_CODE = """
% --- FACTS (From Question) ---
enemy(pims_curve).
loot(white_town).
windy(beach_road).

% --- RULES (From Question) ---

% Example Constraint: "Avoid enemies"
% If I uncomment the line below, the solver will SKIP pims_curve!
% is_valid_step(X) :- \\+ enemy(X).

% Example Constraint: "Only go to windy places if you are brave"
% is_valid_step(X) :- windy(X), write('Warning: Windy! '), nl.

"""

# ==============================================================================
#   EXECUTION LOGIC (Do not edit)
# ==============================================================================
def run_prolog():
    filename = "temp_recursion.pl"
    with open(filename, "w") as f:
        # 1. Write Graph
        for node, neighbors in my_graph.items():
            for neighbor, cost in neighbors:
                n1, n2 = str(node).lower().replace(" ", "_"), str(neighbor).lower().replace(" ", "_")
                f.write(f"edge({n1}, {n2}, {cost}).\n")
        
        # 2. Write Custom Code
        f.write("\n% --- USER CUSTOM CODE ---\n")
        f.write(CUSTOM_PROLOG_CODE)
        
        # 3. Run Solver
        f.write("\n:- consult('recursion_solver.pl').\n")
        s, g = str(START_NODE).lower().replace(" ", "_"), str(GOAL_NODE).lower().replace(" ", "_")
        f.write(f":- find_all_paths({s}, {g}).\n:- halt.\n")

    try:
        subprocess.run(["swipl", "-q", "-s", filename])
    except:
        print("❌ Error: SWI-Prolog not found.")
    finally:
        if os.path.exists(filename): os.remove(filename)

if __name__ == "__main__":
    run_prolog()
