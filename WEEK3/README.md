# A* Manhattan Pathfinder - AI Project 🚀
### Koya University | Software Engineering | 3rd Year (6th Semester)

This project is a visual implementation of the **A* Search Algorithm** using a 10x10 grid. It calculates the shortest path between nodes ('S' and 'G') based on **Manhattan Distance** heuristics.

---

## 👥 Team Roles & Contributions
| Member | Role | Responsibilities |
| :--- | :--- | :--- |
| **Member 1** | **Backend Engineer** | Developed the A* Algorithm logic in `main.py` and handled cost calculations. |
| **Member 2** | **UI/UX Designer** | Designed the CSS Grid, SVG connection lines, and node color schemes in `App.css`. |
| **Member 3** | **Integration Lead** | Managed React state, drag-and-drop events, and API communication in `App.js`. |

---

## 🛠️ Project Features
* **Dynamic Grid:** Interactive 10x10 board for node placement.
* **Drag-to-Connect:** Visually link nodes by dragging your mouse between them.
* **AI Logic:** Real-time pathfinding using Manhattan Heuristics ($|x1 - x2| + |y1 - y2|$).
* **Mathematical Summary:** A detailed popup showing the path sequence and the final cost (e.g., $1 + 3 + 5 = 9$).

---

## 📋 Prerequisites
Before running the project, ensure your laptop has the following software installed:
* **Python 3.12 or higher:** [Download here](https://www.python.org/downloads/)
* **Node.js (LTS Version):** [Download here](https://nodejs.org/)

---

## 📦 One-Click Setup (Quick Start)
To run this project, you only need **Python 3.12+** and **Node.js (LTS)** installed.

1.  **Download/Clone** this repository.
2.  Double-click the **`webui-user.bat`** file in the root folder.
3.  The script will automatically install all dependencies and launch the servers.

---

## 🖥️ How to Use the Demo
1.  **Set Start/Goal:** Type **'S'** in the input and click a cell. Do the same for **'G'**.
2.  **Add Intermediate Nodes:** Type any letter (A, B, C...) and click to place nodes.
3.  **Connect:** Click and hold on a node, **drag** to another node, and release.
4.  **Solve:** Click **"Find Path"**. 

---

## ⚠️ CRITICAL: Enable Pop-ups (Chrome & Edge)
By default, modern browsers like Google Chrome and Microsoft Edge block the result window. **You must enable them to see the final path calculation:**

1.  After clicking **"Find Path"**, look at the **right side of your address bar**.
2.  Click the icon that looks like a window with a red 'x' (Pop-up blocked).
3.  Select **"Always allow pop-ups and redirects from http://localhost:3000"**.
4.  Click **Done** and then click **"Find Path"** again.

---
## 📂 Project Structure

```text
/WEEK3
│
├── webui-user.bat           # Main "one-click" installer and launcher script
├── README.md                # Project documentation and setup guide
├── .gitignore               # Config to prevent pushing node_modules/venv to GitHub
│
├── /backend                 # --- BACKEND (Member 1) ---
│   ├── main.py              # A* Algorithm logic and FastAPI endpoints
│   └── requirements.txt     # List of Python libraries (fastapi, uvicorn)
│
└── /frontend                # --- FRONTEND (Member 2 & 3) ---
    ├── package.json         # List of React libraries and Ant Design
    ├── package-lock.json    # Lockfile for consistent library versions
    │
    ├── /public              # Static Assets (Member 2)
    │   ├── index.html       # The main HTML shell for the app
    │   ├── favicon.ico      # Project tab icon
    │   ├── logo192.png      # logo of React
    |   ├── logo512.png      # logo of React
    │   ├── manifest.json    # Web app metadata (updated with new icon)
    │   └── robots.txt       # Search engine instructions
    │
    └── /src                 # Source Code (Member 2 & 3)
        ├── App.js           # Member 3: Drag logic, React state, and API calls
        ├── App.css          # Member 2: Grid design and node styling
        ├── App.test.js      # Unit tests for the main App component
        ├── index.js         # Entry point for the React application
        ├── index.css        # Global CSS resets
        ├── reportWebVitals.js
        └── setupTests.js
