from flask import Flask, render_template, jsonify
import pandas as pd
import numpy as np
from environment import GridWorld, ACTIONS, GRID_SIZE, OBSTACLES, GOAL_STATE, START_STATE

app = Flask(__name__)

Q_TABLE_FILE = 'qtable.csv'

def get_best_path():
    # Load Q-Table
    try:
        df = pd.read_csv(Q_TABLE_FILE)
        q_table = df.values
    except FileNotFoundError:
        return None

    env = GridWorld()
    # Reset to start
    state_idx = env.reset()
    
    # Store path as list of [row, col] lists for JSON serialization
    path = [list(env.state)] 
    
    steps = 0
    done = False
    
    while not done and steps < 50: # Safety limit
        # Choose best action
        action_idx = np.argmax(q_table[state_idx])
        
        # Step
        next_state_idx, reward, done = env.step(action_idx)
        
        state_idx = next_state_idx
        path.append(list(env.index_to_state(state_idx)))
        steps += 1
        
    return path

@app.route('/')
def index():
    # Pre-calculate grid state to simplify template logic
    grid = []
    for r in range(GRID_SIZE):
        row_data = []
        for c in range(GRID_SIZE):
            cell_type = ''
            if (r, c) in OBSTACLES:
                cell_type = 'obstacle'
            elif (r, c) == GOAL_STATE:
                cell_type = 'goal'
            elif (r, c) == START_STATE:
                cell_type = 'start'
            
            row_data.append({
                'r': r, 
                'c': c, 
                'type': cell_type
            })
        grid.append(row_data)

    return render_template('index.html', 
                           grid=grid,
                           grid_size=GRID_SIZE)

@app.route('/run_simulation')
def run_simulation():
    path = get_best_path()
    if path is None:
        return jsonify({'error': 'Model not trained. Run agent.py first.'})
    return jsonify({'path': path})

if __name__ == '__main__':
    app.run(debug=True, port=5003)
