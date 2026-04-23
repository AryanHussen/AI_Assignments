# 🧩 Magic Square Solver — Genetic Algorithm (GA)

A Python-based project that solves the **3×3 Magic Square puzzle** using a **Genetic Algorithm (GA)**.  
The system evolves candidate solutions over generations, stores results in a JSON file, and visualizes them through a web interface powered by Flask.

---

## 🎯 Problem Definition

### 🔢 Grid
- Size: **3 × 3**

### 🔐 Constraints
- Use integers from **1 to 9**
- **No duplicates allowed**

### 🎯 Objective
- Each **row, column, and diagonal** must sum to:

15
---

## ⚙️ System Architecture

The project follows a **modular MVC-like structure**, divided into clear responsibilities:

### 🧠 1. Algorithm Engineer (`ga.py`)
Handles all Genetic Algorithm logic.

**Responsibilities:**
- Fitness function calculation
- Population initialization
- Selection, crossover, mutation
- Generating new generations

---

### 🔄 2. Orchestrator (`main.py`)
Controls execution flow and system coordination.

**Responsibilities:**
- Running the GA loop
- Saving results to `history.json`
- Starting the Flask server (background thread)
- Automatically launching the browser

---

### 🌐 3. Web Developer (`app.py` & `templates/index.html`)
Handles backend API and frontend UI.

**Responsibilities:**
- Flask routes:
  - `/` → Main interface
  - `/data` → JSON data endpoint
- Fetching data using JavaScript (`fetch()`)
- Rendering dynamic 3×3 grids in the browser

---

## 📁 Project Structure

```text
magic_square_ga/
│
├── ga.py               # Genetic Algorithm logic
├── main.py             # Execution controller
├── app.py              # Flask backend
├── history.json        # Saved generations
│
└── templates/
    └── index.html      # Frontend UI
```
---

## 🛠️ Requirements

Make sure you have:

- **Python 3.x**
- **pip** (Python package manager)

### 📦 Install Dependencies

bash
pip install Flask



### 🚀 Run the Project

Open terminal / command prompt
Navigate to project folder:
cd path/to/magic_square_ga
Run the program:
python main.py
The browser will open automatically.


### 🛑 Stop the Program

To stop execution at any time:

Ctrl + C
