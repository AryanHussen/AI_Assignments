Smart Vacuum Cleaner AI
A pathfinding simulation that uses the A* algorithm to guide a vacuum cleaner through a grid to clean dirt while avoiding obstacles. The system calculates the most efficient path based on movement costs and generates a detailed report of the cleaning journey.

How It Works
The system runs through a logic-driven pipeline:

Environment Generation – Creates a 4x4 grid with a starting position, randomly placed obstacles, and a target dirt location.

*Pathfinding (A Algorithm)** – Calculates the optimal path from the start to the dirt using a heuristic-based search that considers varying movement costs.

Cost Evaluation – Assigns specific costs to movements: moving UP costs 2, moving DOWN costs 0, and horizontal moves cost 1.

Report Generation – Automatically records the grid layout, step-by-step coordinates, and human-friendly directions into a text file.

GUI Visualization – Provides a dark-mode interface where users can watch the vacuum move in real-time or restart the simulation with a new environment.

Prerequisites
Python 3.12

pip

Tkinter (usually included with Python)

Installation
1. Clone the repository
  git clone <your repo link>
  cd AI-assignments-repo/week1/project1/vacuum-cleaner
2. Install the required libraries
    py -3.12 -m pip install customtkinter Pillow

Usage
Run the main application:
  python gui.py

Project Structure
  project1/vacuum-cleaner/
   gui.py              Main GUI — handles visualization and animation
   logic.py            AI Logic — contains the environment setup and A* algorithm
   report_writer.py    Reporting — writes the solution details to a text file
   solution.txt        Generated report — contains the history of cleaning paths
   assets/             Images — contains floor and obstacle icons for the UI
