# Smart Vacuum Cleaner AI

This project is a Python-based simulation of an autonomous vacuum cleaner that uses the A* search algorithm to navigate a grid-based environment, avoid obstacles, and clean dirt. The application features a graphical user interface (GUI) built with customtkinter and automatically generates performance reports for each cleaning session.

# Features
- AI Pathfinding: Uses the A* search algorithm to find the most efficient path from the starting position to the dirt.
- Dynamic Environments: Generates a 4x4 grid with randomized obstacle and dirt placements for every run.
- Interactive GUI: A dark-themed dashboard that visualizes the vacuum's movement in real-time.
- Cost Analysis: Calculates movement costs based on direction:
  1. Up: 2 units.
  2. Down: 0 units.
  3. Left/Right: 1 unit.
- Automatic Reporting: Logs initial board states, step-by-step coordinate paths, and human-friendly movement descriptions into a solution.txt file.

# Project Structure
- gui.py: The main entry point containing the VacuumGUI class. It manages the visualization, animations, and user interface.
- logic.py: Contains the core AI logic, including the VacuumEnvironment class and the A* algorithm implementation for pathfinding.
- report_writer.py: Handles the generation of the solution.txt report, documenting the vacuum's performance and path.

# Requirements
To run this project, you need Python installed along with the following libraries:
1. customtkinter
2. Pillow (PIL)
3. tkinter (usually included with Python)

# How to Run

1. Ensure all project files (gui.py, logic.py, report_writer.py) are in the same directory.
2. Ensure you have an assets/ folder containing necessary images (e.g., floor.png) as referenced in the GUI.
3. Run the application:
    python gui.py

# How it Works
- Initialization: The VacuumEnvironment creates a grid and randomly places three obstacles and one piece of dirt.
- Solving: The solve_vacuum function triggers the A* algorithm to calculate the optimal path based on movement costs.
- Reporting: Before the animation begins, write_solution creates or appends to solution.txt with the session details.
- Animation: The GUI's animate_step method moves the vacuum along the calculated path, updating the total cost and removing dirt upon arrival.
