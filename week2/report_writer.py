from datetime import datetime

def write_solution(env, path, total_cost):

    with open("solution.txt", "w") as file:

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
