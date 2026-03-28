# Import the datetime class from the datetime module to capture the current timestamp for the report header
from datetime import datetime
# Import the os module to interact with the file system (check file existence and size)
import os

# Define the function that writes one complete solution report entry to solution.txt
def write_solution(env, path, total_cost):
    # Check if file exists and has content to avoid leading empty lines on first run
    # os.path.exists checks if the file is present; os.path.getsize checks it's not empty (size > 0 bytes)
    file_exists = os.path.exists("solution.txt") and os.path.getsize("solution.txt") > 0

    # Open solution.txt in append mode ("a") — creates the file if it doesn't exist, never overwrites existing content
    with open("solution.txt", "a") as file:
        # Start writing after 5 empty lines if the file isn't empty
        # This adds visual separation between consecutive report entries
        if file_exists:
            # Write 5 newline characters to create blank lines before the new entry
            file.write("\n" * 5)

        # Write the top decorative border line of the report
        file.write("========================================\n")
        # Write the centered report title
        file.write("        SMART VACUUM CLEANER REPORT     \n")
        # Write the bottom decorative border line followed by a blank line
        file.write("========================================\n\n")

        # Write the current date and time formatted as YYYY-MM-DD HH:MM:SS
        file.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        # Write the grid dimensions (e.g., "4 x 4") followed by a blank line
        file.write(f"Grid Size: {env.size} x {env.size}\n\n")

        # ---------- MATRIX VIEW ----------
        # Write the section header for the visual grid display
        file.write("1) INITIAL BOARD (Grid View)\n")
        # Write a separator line under the section header
        file.write("----------------------------------------\n")

        # Loop through each row in the 2D grid (list of cell symbols like '.', '#', 'D')
        for row in env.grid:
            # Write 3 spaces for indentation, then join each cell symbol with 2 spaces, then newline
            file.write("   " + "  ".join(row) + "\n")

        # Write a blank line after the grid to visually separate it from the next section
        file.write("\n")

        # Only write path-related sections if a valid solution path was found (path is not empty/None)
        if path:
            # ---------- COORDINATE VIEW ----------
            # Write the section header for the raw coordinate path listing
            file.write("2) PATH WITH POSITIONS\n")
            # Write a separator line under the section header
            file.write("----------------------------------------\n")

            # Loop through each step in the path list, with i as the 0-based index and step as the (row, col) tuple
            for i, step in enumerate(path):
                # Write the step number (1-based by adding 1 to i) and its (row, col) coordinate
                file.write(f"Step {i+1}: Position {step}\n")

            # Write a blank line after all steps to separate from the next section
            file.write("\n")

            # ---------- HUMAN FRIENDLY EXPLANATION ----------
            # Write the section header for the plain-English movement descriptions
            file.write("3) CLEANING JOURNEY (Simple Explanation)\n")
            # Write a separator line under the section header
            file.write("----------------------------------------\n")

            # Loop from index 1 to end of path — we always need index i-1 (previous) and i (current)
            for i in range(1, len(path)):
                # Get the cell coordinates the vacuum came from
                prev = path[i-1]
                # Get the cell coordinates the vacuum is moving to
                curr = path[i]

                # If the current row index is smaller than previous, the vacuum moved toward row 0 (upward)
                if curr[0] < prev[0]:
                    # Label this move as upward
                    direction = "moved UP"
                # If the current row index is larger, the vacuum moved toward higher row numbers (downward)
                elif curr[0] > prev[0]:
                    # Label this move as downward
                    direction = "moved DOWN"
                # If rows are equal and the column decreased, the vacuum moved toward column 0 (leftward)
                elif curr[1] < prev[1]:
                    # Label this move as leftward
                    direction = "moved LEFT"
                # If rows are equal and the column increased, the vacuum moved toward higher columns (rightward)
                else:
                    # Label this move as rightward
                    direction = "moved RIGHT"

                # Write a human-readable sentence describing this individual move (e.g., "Move 1: The vacuum moved RIGHT.")
                file.write(f"Move {i}: The vacuum {direction}.\n")

            # Write a separator line after all moves to close the section
            file.write("\n----------------------------------------\n")
            # Write the total number of moves (path length minus 1 because path includes the starting position)
            file.write(f"Total Moves: {len(path)-1}\n")
            # Write the total accumulated movement cost passed into the function
            file.write(f"Total Cost : {total_cost}\n\n")
            # Write the success result message indicating all reachable dirt was cleaned
            file.write("RESULT: Goal Reached Successfully.\n")
        else:
            # If path is empty, no solution was found — write the failure result message
            file.write("RESULT: No Solution Found.\n")
            # Explain the reason why no path exists (obstacles completely block all routes)
            file.write("Reason: Obstacles blocked all possible paths.\n")

        # Write the closing decorative border line to mark the end of this report entry
        file.write("\n========================================\n")