import os
import sys
import pickle
import pandas as pd
import importlib.util
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder

# ==========================================
#  CONFIGURATION (Toggle True/False)
# ==========================================
SHOW_ASTAR          = True
SHOW_AOSTAR         = True
SHOW_CLASSIFICATION = True
SHOW_REGRESSION     = True
SHOW_CLUSTERING     = True
SHOW_RL             = True

# ==========================================
#  HELPER FUNCTIONS
# ==========================================
def get_target_column(folder):
    """Dynamically import TARGET_COLUMN from train.py in the specified folder."""
    try:
        script_path = os.path.join('ML', folder, 'train.py')
        if not os.path.exists(script_path): return None
        
        spec = importlib.util.spec_from_file_location("train_config", script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return getattr(module, 'TARGET_COLUMN', None)
    except Exception as e:
        print(f"   Warning: Could not read config from {folder}/train.py: {e}")
        return None

# ==========================================
#  COMPARISON LOGIC
# ==========================================

def run_astar():
    print("\n" + "="*40)
    print(" 1. A* SEARCH ALGORITHM")
    print("="*40)
    print("Type: Symbolic AI / Pathfinding")
    print("Metric: Total Path Cost (Distance/Risk)")
    
    try:
        # Change dir to find Prolog files
        original_cwd = os.getcwd()
        target_dir = os.path.join(original_cwd, 'A_and_ao')
        if os.path.exists(target_dir):
            os.chdir(target_dir)
            if target_dir not in sys.path:
                sys.path.append(target_dir)
            
            try:
                from a_star import AStarSearch, my_graph, my_heuristics, start_node, goal_node
                
                print(f"Scenario: Path from '{start_node}' to '{goal_node}'")
                solver = AStarSearch(my_graph, my_heuristics)
                path, cost = solver.algorithm(start_node, goal_node)
                
                if path:
                    print(f"✅ Result: Path found with cost {cost}")
                    print(f"   Route: {' -> '.join(path)}")
                else:
                    print("❌ Result: No path found.")
            except ImportError:
                print("Could not import a_star.py")
            except Exception as e:
                print(f"Error during execution: {e}")
                
            # Cleanup
            os.chdir(original_cwd)
        else:
            print("Folder 'A_and_ao' not found.")
    except Exception as e:
        print(f"Error running A*: {e}")
        os.chdir(original_cwd) # Safety

def run_aostar():
    print("\n" + "="*40)
    print(" 2. AO* SEARCH ALGORITHM")
    print("="*40)
    print("Type: Symbolic AI / AND-OR Graph Search")
    print("Metric: Solution Graph Cost")
    
    try:
        original_cwd = os.getcwd()
        target_dir = os.path.join(original_cwd, 'A_and_ao')
        if os.path.exists(target_dir):
            os.chdir(target_dir)
            if target_dir not in sys.path:
                sys.path.append(target_dir)
            
            try:
                from ao_star import AOStarSearch, my_and_or_graph, my_heuristics, start_node
                
                print(f"Scenario: Strategy for '{start_node}'")
                solver = AOStarSearch(my_and_or_graph, my_heuristics, start_node)
                solver.ao_star(start_node, False)
                
                print(f"✅ Result: Min Cost {solver.min_cost}")
                print(f"   Structure: {solver.solution_structure}")
            except ImportError:
                print("Could not import ao_star.py")
            except Exception as e:
                print(f"Error during execution: {e}")
            
            os.chdir(original_cwd)
    except Exception as e:
        print(f"Error running AO*: {e}")
        os.chdir(original_cwd)

def run_ml_classification():
    print("\n" + "="*40)
    print(" 3. ML CLASSIFICATION")
    print("="*40)
    print("Type: Supervised Learning (Decision Tree)")
    print("Metric: Accuracy / Class Prediction")
    
    model_path = os.path.join('ML', 'Classification', 'model.pkl')
    dataset_path = os.path.join('ML', 'Classification', 'dataset.csv')
    
    if os.path.exists(model_path):
        try:
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            print(f"✅ Model Loaded: {model}")
            
            # Calculate Metrics on Dataset
            target_col = get_target_column('Classification')
            if target_col and os.path.exists(dataset_path):
                df = pd.read_csv(dataset_path)
                X = df.drop(columns=[target_col])
                y = df[target_col]
                
                # Simple preprocessing for evaluation
                for col in X.columns:
                    if X[col].dtype == 'object':
                        le = LabelEncoder()
                        X[col] = le.fit_transform(X[col])
                
                y_pred = model.predict(X)
                acc = accuracy_score(y, y_pred)
                print(f"   Training Accuracy: {acc:.2%}")
                print(f"   Tree Depth: {model.get_depth()}")
                print(f"   Leaves: {model.get_n_leaves()}")
            else:
                print("   (Dataset or Config not found, skipping metrics)")
                
        except Exception as e:
            print(f"Error loading model or calculating metrics: {e}")
    else:
        print("❌ Model not found. Run 'train.py' in ML/Classification first.")

def run_ml_regression():
    print("\n" + "="*40)
    print(" 4. ML REGRESSION")
    print("="*40)
    print("Type: Supervised Learning (Linear Regression)")
    print("Metric: Mean Squared Error / R2 Score")
    
    model_path = os.path.join('ML', 'Regression', 'model.pkl')
    scaler_path = os.path.join('ML', 'Regression', 'scaler.pkl')
    dataset_path = os.path.join('ML', 'Regression', 'dataset.csv')
    
    if os.path.exists(model_path):
        try:
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            print("✅ Model Loaded.")
            
            # Calculate Metrics
            target_col = get_target_column('Regression')
            if target_col and os.path.exists(dataset_path):
                df = pd.read_csv(dataset_path)
                X = df.drop(columns=[target_col])
                y = df[target_col]
                
                for col in X.columns:
                    if X[col].dtype == 'object':
                        le = LabelEncoder()
                        X[col] = le.fit_transform(X[col])
                
                # Apply scaling if available
                if os.path.exists(scaler_path):
                    with open(scaler_path, 'rb') as f:
                        scaler = pickle.load(f)
                    X = scaler.transform(X)
                
                y_pred = model.predict(X)
                mse = mean_squared_error(y, y_pred)
                r2 = r2_score(y, y_pred)
                print(f"   Mean Squared Error (MSE): {mse:.4f}")
                print(f"   R2 Score: {r2:.4f}")
                print(f"   Coefficients: {model.coef_}")
            else:
                print("   (Dataset or Config not found, skipping metrics)")
                
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("❌ Model not found.")

def run_ml_clustering():
    print("\n" + "="*40)
    print(" 5. ML CLUSTERING")
    print("="*40)
    print("Type: Unsupervised Learning (K-Means)")
    print("Metric: Inertia / Cluster Assignment")
    
    model_path = os.path.join('ML', 'Clustering', 'model.pkl')
    if os.path.exists(model_path):
        try:
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            print(f"✅ Model Loaded. Clusters: {model.n_clusters}")
            print(f"   Inertia (Sum of squared distances): {model.inertia_:.4f}")
            print(f"   Iterations to converge: {model.n_iter_}")
            print(f"   Cluster Centers Shape: {model.cluster_centers_.shape}")
        except:
            print("Error loading model.")
    else:
        print("❌ Model not found.")

def run_rl():
    print("\n" + "="*40)
    print(" 6. REINFORCEMENT LEARNING")
    print("="*40)
    print("Type: Q-Learning")
    print("Metric: Cumulative Reward / Q-Table Convergence")
    
    qtable_path = os.path.join('RL', 'QLearning', 'qtable.csv')
    if os.path.exists(qtable_path):
        print("✅ Q-Table Found.")
        try:
            df = pd.read_csv(qtable_path, header=None)
            print(f"   State-Action Space: {df.shape}")
            print(f"   Max Q-Value Learned: {df.max().max()}")
        except:
            print("   Could not parse Q-Table.")
    else:
        print("❌ Q-Table not found.")

def main():
    print("AI LAB EXPERIMENT - COMPARATIVE ANALYSIS")
    
    if SHOW_ASTAR: run_astar()
    if SHOW_AOSTAR: run_aostar()
    if SHOW_CLASSIFICATION: run_ml_classification()
    if SHOW_REGRESSION: run_ml_regression()
    if SHOW_CLUSTERING: run_ml_clustering()
    if SHOW_RL: run_rl()
    
    print("\n" + "="*40)
    print(" COMPARISON SUMMARY")
    print("="*40)
    print("1. Symbolic (A*/AO*): Exact, explainable, requires complete knowledge (Graph).")
    print("2. ML (Class/Reg): Statistical, generalizes to new data, requires training data.")
    print("3. RL (Q-Learning): Adaptive, learns from interaction, requires environment simulation.")

if __name__ == "__main__":
    main()
