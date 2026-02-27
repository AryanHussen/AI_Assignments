from datetime import datetime

def write_solution(env, path, total_cost):

    with open("solution.txt", "w") as file:

        file.write("===== VACUUM CLEANER SEARCH REPORT =====\n\n")

        # Date & Time
        file.write(f"Generated on: {datetime.now()}\n\n")

        # Initial Board
        file.write("Initial Board:\n")
        for row in env.grid:
            file.write(" ".join(row) + "\n")

        file.write("\n----------------------------------------\n\n")

        if path:

            file.write("Steps to Solution:\n\n")
            for i, step in enumerate(path):
                file.write(f"Step {i+1}: {step}\n")

            file.write("\n----------------------------------------\n\n")
            file.write(f"Total Steps: {len(path)-1}\n")
            file.write(f"Total Cost: {total_cost}\n\n")
            file.write("Goal Reached Successfully.\n")

        else:
            file.write("NO SOLUTION FOUND.\n")
            file.write("Reason: Obstacles block the path.\n")