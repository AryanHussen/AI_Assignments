import json # Import json to write the history to a file
import random # Import random to generate random chances and selections
import webbrowser # Import webbrowser to automatically open the UI in the default browser
import threading # Import threading to run the Flask server in the background
import time # Import time to add delays so the server has time to start
import ga # Import your custom genetic algorithm logic module
import app # type: ignore # Import your custom Flask application module


# -----------------------------
# 1. RUN GA FIRST
# -----------------------------
population = [ga.generate_individual() for _ in range(100)] # Create an initial population of 100 random grids
history = [] # Initialize an empty list to store the best grid of each generation

for generation in range(500): # Start a loop that will run for a maximum of 500 generations

    population.sort(key=ga.calculate_fitness) # Sort the entire population from lowest (best) fitness to highest (worst)

    best = population[0] # The best individual is the first one in the sorted list
    best_fitness = ga.calculate_fitness(best) # Calculate the fitness score of this best individual

    history.append({ # Add a dictionary containing this generation's best data to the history list
        "gen": generation, # Store the current generation number
        "grid": best, # Store the layout of the best grid
        "fitness": best_fitness # Store the fitness score
    })

    if best_fitness == 0: # Check if the magic square is perfectly solved (score is 0)
        break # If solved, stop the genetic algorithm loop early

    next_gen = population[:10] # Keep the top 10 best individuals unchanged for the next generation (Elitism)

    while len(next_gen) < 100: # Loop until the next generation has 100 individuals

        if random.random() < 0.2: # 20% chance to introduce completely new random genetic material
            next_gen.append(ga.generate_individual()) # Create a new random grid and add it to the next generation
        else: # 80% chance to create offspring through reproduction
            p1, p2 = random.sample(population[:50], 2) # Randomly select 2 parents from the top 50 individuals of the current population
            child = ga.crossover(p1, p2) # Combine the parents' genes to create a child

            if random.random() < 0.7: # 70% chance that the child will undergo a random mutation
                child = ga.mutate(child) # Apply the mutation function to the child

            next_gen.append(child) # Add the resulting child to the next generation pool

    population = next_gen # Replace the old population with the newly generated population


# -----------------------------
# 2. SAVE DATA
# -----------------------------
with open("history.json", "w") as f: # Open the history.json file in write mode
    json.dump(history, f, indent=2) # Write the entire history list into the file formatted with 2-space indentation


# -----------------------------
# 3. START FLASK SERVER
# -----------------------------
threading.Thread(target=app.run, daemon=True).start() # Start the Flask server in a background thread so the script doesn't block execution

time.sleep(2) # Pause the script for 2 seconds to give the Flask server time to fully start up


# -----------------------------
# 4. OPEN BROWSER
# -----------------------------
webbrowser.open("http://127.0.0.1:5000") # Open the default system web browser to the local Flask server address


# keep alive
while True: # Start an infinite loop to prevent the main script from exiting
    time.sleep(1) # Sleep for 1 second continuously (if the script exits, the daemon thread running Flask dies too)