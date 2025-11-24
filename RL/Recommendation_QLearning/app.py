from flask import Flask, render_template, request, jsonify
from agent import QLearningAgent
from environment import STATES, ACTIONS, REWARD_MAP
import os

app = Flask(__name__)

Q_TABLE_FILE = 'qtable.csv'
agent = QLearningAgent(STATES, ACTIONS)
agent.load(Q_TABLE_FILE)

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendation = None
    context = None
    
    if request.method == 'POST':
        context = request.form.get('context')
        
        # Get recommendation based on trained agent
        recommendation = agent.choose_action(context, train=False)
        
    return render_template('index.html', 
                           states=STATES, 
                           recommendation=recommendation, 
                           context=context)

@app.route('/feedback', methods=['POST'])
def feedback():
    """
    Allows the web user to provide feedback (Reward) which updates the model in real-time!
    """
    data = request.json
    context = data['context']
    action = data['action']
    feedback_type = data['feedback'] # 'like' or 'dislike'
    
    # Define reward based on user feedback
    reward = 10 if feedback_type == 'like' else -10
    
    # Online Learning: Update the agent immediately
    agent.learn(context, action, reward)
    
    # Save the updated brain
    agent.save(Q_TABLE_FILE)
    
    return jsonify({'status': 'success', 'new_q_value': agent.q_table.loc[context, action]})

if __name__ == '__main__':
    app.run(debug=True, port=5004)
