from flask import Flask, render_template, request, jsonify
from pyswip import Prolog

app = Flask(__name__)

# Initialize Prolog
prolog = Prolog()
try:
    prolog.consult("kb.pl")
except Exception as e:
    print(f"Error loading Prolog file: {e}")
    print("Ensure SWI-Prolog is installed and in your system PATH.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    """
    Executes a raw Prolog query received from the frontend.
    Example: mortal(X) or ancestor(john, Y)
    """
    query_str = request.form.get('query')
    results = []
    
    try:
        # pyswip returns a generator of dictionaries
        # e.g. [{'X': 'socrates'}, {'X': 'plato'}]
        for soln in prolog.query(query_str):
            results.append(soln)
            
        # If results is empty but query succeeded (true/false query like 'mortal(socrates)')
        if not results:
            # We can't easily distinguish between "False" and "True but no variables" 
            # with simple list check in pyswip without catching StopIteration or checking bool
            # But for this template, we return the list. 
            # If the list is empty, it might mean false OR true with no vars.
            # A robust app would handle this better.
            pass
            
    except Exception as e:
        return jsonify({'error': str(e)})
    
    return jsonify({'results': results})

@app.route('/add_fact', methods=['POST'])
def add_fact():
    """
    Demonstrates Dynamic Predicates (assertz)
    """
    fact = request.form.get('fact') # e.g., friend(alice, bob)
    try:
        prolog.assertz(fact)
        return jsonify({'status': 'success', 'message': f'Added fact: {fact}'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    # NOTE: You must have SWI-Prolog installed for pyswip to work!
    # Download: https://www.swi-prolog.org/download/stable
    app.run(debug=True, port=5005)
