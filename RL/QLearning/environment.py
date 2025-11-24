import numpy as np

# ==========================================
# ENVIRONMENT CONFIGURATION
# ==========================================
GRID_SIZE = 5 # 5x5 Grid
START_STATE = (0, 0)
GOAL_STATE = (4, 4)
OBSTACLES = [(1, 1), (2, 2), (3, 1), (1, 3)]
ACTIONS = ['UP', 'DOWN', 'LEFT', 'RIGHT']

class GridWorld:
    def __init__(self):
        self.grid_size = GRID_SIZE
        self.state = START_STATE
        self.goal = GOAL_STATE
        self.obstacles = OBSTACLES
        self.actions = ACTIONS
        
    def reset(self):
        self.state = START_STATE
        return self.state_to_index(self.state)
    
    def state_to_index(self, state):
        # Converts (row, col) to a single integer index 0..24
        return state[0] * self.grid_size + state[1]
        
    def index_to_state(self, index):
        # Converts single integer index back to (row, col)
        return (index // self.grid_size, index % self.grid_size)

    def step(self, action_idx):
        """
        Takes an action index (0: UP, 1: DOWN, 2: LEFT, 3: RIGHT)
        Returns: next_state_idx, reward, done
        """
        row, col = self.state
        action = self.actions[action_idx]
        
        new_row, new_col = row, col
        
        if action == 'UP':
            new_row = max(0, row - 1)
        elif action == 'DOWN':
            new_row = min(self.grid_size - 1, row + 1)
        elif action == 'LEFT':
            new_col = max(0, col - 1)
        elif action == 'RIGHT':
            new_col = min(self.grid_size - 1, col + 1)
            
        next_state = (new_row, new_col)
        
        # Check for Goal
        if next_state == self.goal:
            self.state = next_state
            return self.state_to_index(next_state), 10, True # Reward 10, Done
            
        # Check for Obstacles
        if next_state in self.obstacles:
            # Option A: Hit obstacle and die
            # self.state = next_state
            # return self.state_to_index(next_state), -10, True
            
            # Option B: Hit obstacle and bounce back (stay in same place) with penalty
            return self.state_to_index(self.state), -5, False
            
        # Normal Step
        self.state = next_state
        return self.state_to_index(next_state), -1, False # Small penalty to encourage shortest path
