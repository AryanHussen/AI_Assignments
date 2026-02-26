# to test the files run this in terminal  ( py test_logic.py )
# Import your functions from the logic file
from logic import VacuumEnvironment, solve_vacuum

def run_test():
    # 1. Setup the 4x4 board (Rows 0, 1, 2, 3) 
    print("--- 4x4 VACUUM BOARD ---")
    env = VacuumEnvironment(size=4, obstacle_prob=0.1) 
    
    # Print the board to the screen so you can see the V and D [cite: 1]
    for row in env.grid:
        print(" ".join(row))
    
    # 2. Start the AI search [cite: 1]
    print("\n--- RUNNING BEST-FIRST SEARCH ---")
    path, total_cost = solve_vacuum(env)

    # 3. Print the final results [cite: 1]
    if path:
        print(f"SUCCESS: Path found in {len(path)-1} moves.")
        print(f"Path taken: {path}") # Shows coordinates like (0,0), (1,0)
        print(f"Total Movement Cost: {total_cost}") # Correctly follows 2/1/0 rules 
    else:
        # If no path exists, print the required error message [cite: 2, 4]
        print("RESULT: No solution because of obstacles.")

# Run the test function
if __name__ == "__main__":

    run_test()
