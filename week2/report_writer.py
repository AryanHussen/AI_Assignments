from datetime import datetime
import os

def write_solution(env, path, total_cost):
    # Check if file exists and has content to avoid leading empty lines on first run
    file_exists = os.path.exists("solution.txt") and os.path.getsize("solution.txt") > 0

    with open("solution.txt", "a") as file:
        # Start writing after 5 empty lines if the file isn't empty
        if file_exists:
            file.write("\n" * 5)

        file.write("========================================\n")
        file.write("        SMART VACUUM CLEANER REPORT     \n")
        file.write("========================================\n\n")

        file.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write(f"Grid Size: {env.size} x {env.size}\n\n")

        # ---------- MATRIX VIEW ----------
        file.write("1) INITIAL BOARD (Grid View)\n")
        file.write("----------------------------------------\n")

        for row in env.grid:
            file.write("   " + "  ".join(row) + "\n")

        file.write("\n")

        if path:
            # ---------- COORDINATE VIEW ----------
            file.write("2) PATH WITH POSITIONS\n")
            file.write("----------------------------------------\n")

            for i, step in enumerate(path):
                file.write(f"Step {i+1}: Position {step}\n")

            file.write("\n")

            # ---------- HUMAN FRIENDLY EXPLANATION ----------
            file.write("3) CLEANING JOURNEY (Simple Explanation)\n")
            file.write("----------------------------------------\n")

            for i in range(1, len(path)):
                prev = path[i-1]
                curr = path[i]

                if curr[0] < prev[0]:
                    direction = "moved UP"
                elif curr[0] > prev[0]:
                    direction = "moved DOWN"
                elif curr[1] < prev[1]:
                    direction = "moved LEFT"
                else:
                    direction = "moved RIGHT"

                file.write(f"Move {i}: The vacuum {direction}.\n")

            file.write("\n----------------------------------------\n")
            file.write(f"Total Moves: {len(path)-1}\n")
            file.write(f"Total Cost : {total_cost}\n\n")
            file.write("RESULT: Goal Reached Successfully.\n")
        else:
            file.write("RESULT: No Solution Found.\n")
            file.write("Reason: Obstacles blocked all possible paths.\n")

        file.write("\n========================================\n")
