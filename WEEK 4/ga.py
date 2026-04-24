import random # Import the random module to generate random numbers and choices

TARGET = 15 # Define the magic constant for a 3x3 magic square

def calculate_fitness(grid): # Function to evaluate how close a grid is to a perfect magic square
    score = 0 # Initialize the penalty score to 0 (lower is better, 0 is perfect)

    for i in range(0, 9, 3): # Loop through the starting indices of the 3 rows (0, 3, 6)
        score += abs(sum(grid[i:i+3]) - TARGET) # Add the absolute difference between the row's sum and 15 to the score

    for i in range(3): # Loop through the starting indices of the 3 columns (0, 1, 2)
        score += abs(sum(grid[i::3]) - TARGET) # Add the absolute difference between the column's sum and 15 to the score

    score += abs(grid[0] + grid[4] + grid[8] - TARGET) # Add penalty for the main diagonal (top-left to bottom-right)
    score += abs(grid[2] + grid[4] + grid[6] - TARGET) # Add penalty for the anti-diagonal (top-right to bottom-left)

    return score # Return the final calculated fitness score

def generate_individual(): # Function to create a random new 3x3 grid
    return random.sample(range(1, 10), 9) # Return a list of 9 unique numbers randomly chosen from 1 to 9

def crossover(p1, p2): # Function to combine two parent grids to create a child
    point = random.randint(1, 7) # Choose a random split point between index 1 and 7
    child = p1[:point] # The child inherits the first part from parent 1

    for gene in p2: # Loop through the numbers in parent 2
        if gene not in child: # Check if the number is not already in the child
            child.append(gene) # If it's missing, add it to the child to preserve ordering from parent 2

    return child # Return the newly created child grid

def mutate(ind): # Function to randomly alter an individual to maintain genetic diversity
    if random.random() < 0.7: # 70% chance that a mutation will occur
        a, b = random.sample(range(9), 2) # Pick two random distinct indices from 0 to 8
        ind[a], ind[b] = ind[b], ind[a] # Swap the numbers at those two indices

    return ind # Return the mutated individual