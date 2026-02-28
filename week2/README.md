🧹 Smart Vacuum Cleaner AI
📌 Introduction

Smart Vacuum Cleaner AI is a Python-based simulation of an intelligent vacuum cleaner operating in a grid environment. The system uses the A* (A-Star) search algorithm to find the optimal path from a starting position to a dirt location while avoiding randomly placed obstacles.

The project features:

A graphical user interface built with Tkinter and CustomTkinter

A dynamic grid-based environment

Intelligent pathfinding using A* search

Custom movement costs

Automatic report generation after each run

📂 Table of Contents

Introduction

Features

Project Structure

Installation

Dependencies

Usage

Movement Cost Rules

Report Generation

Example Output

Troubleshooting

Contributors

License

✨ Features

🗺️ 4x4 grid environment (configurable)

🚧 Random obstacle placement

🧽 Random dirt placement

🧠 A* search algorithm for optimal pathfinding

🎨 Modern dark-themed GUI

📊 Real-time cost tracking during animation

📝 Automatic detailed solution report (solution.txt)

🔄 Restart functionality with new random environment

📁 Project Structure
Smart-Vacuum-AI/
│
├── gui.py              # GUI and animation logic
├── logic.py            # Environment and A* algorithm
├── report_writer.py    # Solution report generator
├── assets/
│   ├── floor.png
│   ├── obstacle.png
│   ├── dirt.png
│   └── vacuum.png
└── solution.txt        # Auto-generated cleaning reports
⚙️ Installation
1️⃣ Clone the repository
git clone https://github.com/your-username/smart-vacuum-ai.git
cd smart-vacuum-ai
2️⃣ Install required dependencies
pip install customtkinter pillow
📦 Dependencies

Python 3.8+

tkinter

customtkinter

Pillow

heapq (built-in)

random (built-in)

datetime (built-in)

os (built-in)

▶️ Usage

Run the application:

python gui.py
Controls

Start Cleaning → Begins the vacuum animation

Restart → Generates a new random grid and new solution

💰 Movement Cost Rules

The vacuum cleaner uses custom movement costs:

Direction	Cost
⬆️ Up	2
⬇️ Down	0
⬅️ Left	1
➡️ Right	1

These costs influence the A* path selection and total solution cost.

🧠 Algorithm Used

The system implements the A* Search Algorithm, which combines:

g(n) → Actual movement cost

h(n) → Manhattan distance heuristic

f(n) = g(n) + h(n)

The algorithm guarantees the optimal path if one exists.

📝 Report Generation

After each run (including restart), a detailed report is automatically appended to:

solution.txt

The report includes:

Timestamp

Grid layout (matrix view)

Step-by-step path coordinates

Human-readable movement explanation

Total moves

Total cost

Success or failure result

Multiple runs are separated clearly inside the file.

📊 Example Output (Report Snippet)
SMART VACUUM CLEANER REPORT
Date: 2026-02-28 14:30:11
Grid Size: 4 x 4

1) INITIAL BOARD
.  .  #  .
.  #  .  .
.  .  .  #
.  .  .  .

2) PATH WITH POSITIONS
Step 1: Position (0,0)
Step 2: Position (1,0)
Step 3: Position (2,0)
...
🛠 Troubleshooting
❗ Images Not Loading

Ensure the assets/ folder exists and contains:

floor.png

obstacle.png

dirt.png

vacuum.png

❗ Module Not Found Error

Install missing libraries using:

pip install customtkinter pillow
❗ No Solution Found

If obstacles completely block the dirt location, the system will:

Display no movement

Log "No Solution Found" in the report

👨‍💻 Contributors

Developed as an Artificial Intelligence pathfinding simulation project.

You may add contributor names here.

📜 License

This project is open-source and available under the MIT License.
