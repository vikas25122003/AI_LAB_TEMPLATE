# AI Lab Templates - Comprehensive Guide

This repository contains boilerplate templates for **Machine Learning (ML)**, **Reinforcement Learning (RL)**, and **Prolog**. Each module is designed to be **configurable** and **adaptable** to different problem statements.

## 🛠️ Prerequisites

Before running any code, ensure you have the following installed:

1.  **Python 3.x**
2.  **Python Libraries**:
    ```bash
    pip install pandas numpy scikit-learn flask pyswip
    ```
3.  **SWI-Prolog** (Required only for the Prolog module):
    *   Download and install from [swi-prolog.org](https://www.swi-prolog.org/).
    *   **Important**: Add the SWI-Prolog `bin` folder to your System PATH environment variable.

---

## 1. 🤖 Machine Learning (ML)

Located in `ML/`. Contains templates for Classification, Regression, and Clustering.

### General Workflow
1.  **Data**: Place your `.csv` file in the specific algorithm folder.
2.  **Train**: Run `train.py` to learn patterns and save the model (`model.pkl`).
3.  **Web App**: Run `app.py` to launch the Flask UI for predictions.
4.  **Metrics**: Run `calc.py` to view accuracy, confusion matrices, etc.

### A. Classification (`ML/Classification`)
**Use Case**: Predicting a category (e.g., Car Recommendation "Buy/No", Spam Detection).
*   **Algorithm**: Decision Tree Classifier.
*   **Configuration (`train.py`)**:
    *   `DATASET_FILE`: Name of your CSV file.
    *   `TARGET_COLUMN`: The column name you want to predict.
*   **Configuration (`app.py`)**:
    *   `feature_names`: Update this list to match the input columns of your dataset (excluding the target).
*   **Key Features**:
    *   **Auto-Encoding**: Automatically detects text columns (e.g., "Honda", "Toyota") and converts them to numbers.
    *   **No Scaling**: Decision Trees handle unscaled data well.

### B. Regression (`ML/Regression`)
**Use Case**: Predicting a continuous number (e.g., House Price, Temperature).
*   **Algorithm**: Linear Regression.
*   **Configuration (`train.py`)**:
    *   `TARGET_COLUMN`: The continuous value column to predict.
    *   `USE_SCALING = True`: Toggles `StandardScaler`. Keep `True` for best results.
*   **Configuration (`app.py`)**:
    *   `feature_names`: Update to match your input columns.
*   **Key Features**:
    *   **Scaling**: Automatically scales inputs using `StandardScaler` and saves the scaler to `scaler.pkl`.

### C. Clustering (`ML/Clustering`)
**Use Case**: Grouping similar items (e.g., Customer Segmentation).
*   **Algorithm**: K-Means Clustering.
*   **Configuration (`train.py`)**:
    *   `K_CLUSTERS`: The number of groups (k) you want to find.
    *   `IGNORE_COLS`: List of columns to exclude from clustering (e.g., `['CustomerID', 'Name']`).
*   **Key Features**:
    *   **Scaling**: Always enabled (Critical for K-Means).
    *   **Metrics**: Calculates Silhouette Score and Inertia in `calc.py`.

---

## 2. 🎮 Reinforcement Learning (RL)

Located in `RL/`. Contains templates for Navigation and Recommendation.

### A. GridWorld Navigation (`RL/QLearning`)
**Use Case**: Pathfinding, Maze Solving, Robot Navigation.
*   **Concept**: An agent learns to move on a grid from Start to Goal avoiding Obstacles.
*   **Configuration (`environment.py`)**:
    *   `GRID_SIZE`: Dimension of the map (e.g., `5` for 5x5).
    *   `OBSTACLES`: List of `(row, col)` tuples representing walls.
    *   `START_STATE` / `GOAL_STATE`: Coordinates `(row, col)`.
    *   `step()` function: Modify rewards here (e.g., change penalty for hitting walls).
*   **Configuration (`agent.py`)**:
    *   `EPISODES`: Number of training loops. Increase for larger maps.
    *   `ALPHA` (Learning Rate), `GAMMA` (Discount Factor), `EPSILON` (Exploration).
*   **Web UI**:
    *   Automatically renders the grid based on `GRID_SIZE`.
    *   Animates the agent's path.

### B. Recommendation System (`RL/Recommendation_QLearning`)
**Use Case**: Suggesting items based on user profile + feedback (Multi-Armed Bandit style).
*   **Concept**: Agent suggests an action, User gives feedback, Agent updates strategy.
*   **Configuration (`environment.py`)**:
    *   `STATES`: List of user profiles (e.g., `['Student', 'Family']`).
    *   `ACTIONS`: List of items to recommend (e.g., `['Sedan', 'SUV']`).
    *   `REWARD_MAP`: The "Ground Truth" logic used for initial training.
*   **Interactive Mode (`app.py`)**:
    *   Select a user profile.
    *   Get a recommendation.
    *   **Click Like/Dislike**: This sends a reward (+10/-10) to the agent.
    *   **Online Learning**: The agent updates `qtable.csv` immediately. If you dislike an item enough, it stops recommending it.

---

## 3. 🦉 Prolog

Located in `Prolog/`.

### Knowledge Base (`kb.pl`)
This file contains the logic. It is pre-filled with examples of:
*   **Facts**: `parent(john, mary).`
*   **Rules**: `mortal(X) :- human(X).`
*   **Recursion**: `ancestor(X, Y).`
*   **Arithmetic**: `factorial(N, F).`
*   **Lists**: `sum_list(List, Sum).`
*   **Negation**: `\+ married(X).`
*   **Cut (!)**: Stops backtracking.

### Web Interface (`app.py`)
*   Uses `pyswip` to bridge Python and Prolog.
*   **Query**: Run any Prolog query (e.g., `ancestor(john, X)`) from the browser.
*   **Dynamic Facts**: Add new facts (e.g., `friend(me, you)`) at runtime via the UI.

---

## 🚀 Quick Start Guide

1.  **Pick a Template** (e.g., `ML/Classification`).
2.  **Replace `dataset.csv`** with your own data.
3.  **Edit `train.py`**: Set `TARGET_COLUMN` to your label name.
4.  **Run `train.py`**:
    ```powershell
    python ML/Classification/train.py
    ```
5.  **Edit `app.py`**: Update `feature_names` to match your CSV columns.
6.  **Run `app.py`**:
    ```powershell
    python ML/Classification/app.py
    ```
7.  **Open Browser**: Go to the URL shown (usually `http://127.0.0.1:5000`).
