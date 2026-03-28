# Import the standard tkinter library, used here specifically for the Canvas widget
import tkinter as tk
# Import customtkinter, a modern UI framework built on top of tkinter with better styling
import customtkinter as ctk
# Import VacuumEnvironment (creates the grid world) and solve_vacuum (the AI pathfinding solver) from the logic module
from logic import VacuumEnvironment, solve_vacuum
# Import Image to open and resize image files, and ImageTk to convert them into a format tkinter can display
from PIL import Image, ImageTk
# Import the report-writing function that saves the solution details to solution.txt
from report_writer import write_solution

# Set the global color scheme of all CTk widgets to dark mode (dark background, light text)
ctk.set_appearance_mode("dark")
# Set the default accent color for buttons and interactive elements to blue
ctk.set_default_color_theme("blue")


# Define the main application class, inheriting from CTk which acts as the root window
class VacuumGUI(ctk.CTk):

    # Class-level constant: the pixel size of each square cell in the grid
    CELL_SIZE = 120
    # Class-level constant: the pixel size of the obstacle image (smaller than the cell so it appears centered)
    OBSTACLE_SIZE = 70
    # Class-level constant: the delay in milliseconds between each animation frame
    SPEED = 600

    # Constructor method — automatically called when VacuumGUI() is instantiated
    def __init__(self):
        # Call the parent class (CTk) constructor to properly initialize the window
        super().__init__()

        # Set the text shown in the window's title bar
        self.title("Smart Vacuum Cleaner AI")
        # Maximize the window to fill the entire screen on startup
        self.state("zoomed")

        # Create a new 4x4 vacuum environment with randomly placed dirt and obstacles
        self.env = VacuumEnvironment(size=4)
        # Run the AI solver on the environment; returns the path to follow, total cost, and any unreachable dirt cells
        self.path, self.total_cost, self.unreachable = solve_vacuum(self.env)
        
        # --- ADDED THIS LINE TO GENERATE INITIAL REPORT ---
        # Write the initial solution report to solution.txt as soon as the app launches
        write_solution(self.env, self.path, self.total_cost)

        # Initialize the step counter to 0, meaning the vacuum hasn't moved yet
        self.current_step = 0
        # Initialize the running cost display to 0
        self.current_cost = 0
        # Flag to track whether animation is currently playing, preventing duplicate starts
        self.animating = False

        # Load and prepare all image assets from the assets/ folder
        self.load_images()
        # Build all the UI components (frames, buttons, canvas, labels)
        self.create_layout()
        # Draw the initial state of the grid before any animation begins
        self.draw_grid()

    # Method responsible for loading all image files and converting them to tkinter-compatible format
    def load_images(self):
        # Open floor.png, resize it to exactly fill one cell, and convert it for tkinter display
        self.floor_img = ImageTk.PhotoImage(
            Image.open("assets/floor.png").resize((self.CELL_SIZE, self.CELL_SIZE))
        )
        # Open obstacle.png, resize it to OBSTACLE_SIZE (smaller than the cell so it looks inset), and convert it
        self.obstacle_img = ImageTk.PhotoImage(
            Image.open("assets/obstacle.png").resize((self.OBSTACLE_SIZE, self.OBSTACLE_SIZE))
        )
        # Open dirt.png, resize it to fill one full cell, and convert it
        self.dirt_img = ImageTk.PhotoImage(
            Image.open("assets/dirt.png").resize((self.CELL_SIZE, self.CELL_SIZE))
        )
        # Open vacuum.png, resize it to fill one full cell, and convert it
        self.vacuum_img = ImageTk.PhotoImage(
            Image.open("assets/vacuum.png").resize((self.CELL_SIZE, self.CELL_SIZE))
        )

    # Method that creates and arranges all UI widgets inside the main window
    def create_layout(self):

        # Create a horizontal container frame at the top of the window to hold the title label
        self.top_frame = ctk.CTkFrame(self)
        # Place the top frame using pack layout, with 20px vertical padding and stretching across the full window width
        self.top_frame.pack(pady=20, fill="x")

        # Create the main title label inside the top frame
        self.title_label = ctk.CTkLabel(
            # Attach this label to the top frame as its parent container
            self.top_frame,
            # The text content displayed as the app's heading
            text="SMART VACUUM CLEANER",
            # Use a large bold Arial font to make the title prominent
            font=("Arial", 30, "bold")
        )
        # Place the title label inside the top frame using pack (centered by default)
        self.title_label.pack()

        # Create the canvas widget where the grid will be drawn using pixel-based rendering
        self.canvas = tk.Canvas(
            # Attach the canvas directly to the main window
            self,
            # Set canvas width = number of columns × cell size in pixels (e.g., 4 × 120 = 480px)
            width=self.env.size * self.CELL_SIZE,
            # Set canvas height = number of rows × cell size in pixels (square grid)
            height=self.env.size * self.CELL_SIZE,
            # Remove the default blue focus border that tkinter adds around canvas widgets
            highlightthickness=0
        )
        # Place the canvas in the window with 20px vertical padding above and below
        self.canvas.pack(pady=20)

        # Create a container frame at the bottom of the window for the control buttons and cost label
        self.bottom_frame = ctk.CTkFrame(self)
        # Place the bottom frame with 20px vertical padding
        self.bottom_frame.pack(pady=20)

        # Create the "Start Cleaning" button that triggers the animation
        self.start_btn = ctk.CTkButton(
            # Attach to the bottom frame
            self.bottom_frame,
            # Label text shown on the button
            text="Start Cleaning",
            # Bind the button click to the start_animation method
            command=self.start_animation,
            # Set the button's pixel width
            width=200,
            # Set the button's pixel height
            height=50
        )
        # Place the button on the left side of the bottom frame with 20px horizontal padding
        self.start_btn.pack(side="left", padx=20)

        # Create the "Restart" button that resets the environment and generates a new problem
        self.restart_btn = ctk.CTkButton(
            # Attach to the bottom frame
            self.bottom_frame,
            # Label text shown on the button
            text="Restart",
            # Bind the button click to the restart method
            command=self.restart,
            # Set the button's pixel width
            width=200,
            # Set the button's pixel height
            height=50,
            # Override the default blue color with gray to visually distinguish it from the Start button
            fg_color="gray"
        )
        # Place it to the right of the Start button, also on the left side with 20px horizontal padding
        self.restart_btn.pack(side="left", padx=20)

        # Create a label to display the current accumulated movement cost during animation
        self.info_label = ctk.CTkLabel(
            # Attach to the bottom frame
            self.bottom_frame,
            # Initial text before animation starts
            text="Cost: 0",
            # Use a medium-sized font for readability
            font=("Arial", 20)
        )
        # Place it to the right of the buttons with extra 40px padding for visual spacing
        self.info_label.pack(side="left", padx=40)

    # Method that clears and redraws the entire grid canvas on every animation frame
    def draw_grid(self):
        # Delete all existing drawings from the canvas to start fresh each frame
        self.canvas.delete("all")

        # Loop through every row index in the grid
        for r in range(self.env.size):
            # Loop through every column index in the grid
            for c in range(self.env.size):
                # Calculate the pixel X coordinate of this cell's top-left corner
                x = c * self.CELL_SIZE
                # Calculate the pixel Y coordinate of this cell's top-left corner
                y = r * self.CELL_SIZE

                # Draw the floor tile image at this cell's position (anchor="nw" means top-left corner)
                self.canvas.create_image(x, y, anchor="nw", image=self.floor_img)

                # Check if this cell is an obstacle in the environment's grid data
                if self.env.grid[r][c] == "#":
                    # Calculate offset to center the smaller obstacle image within the larger cell
                    offset = (self.CELL_SIZE - self.OBSTACLE_SIZE) // 2
                    # Draw the obstacle image, shifted by the offset to appear centered in the cell
                    self.canvas.create_image(
                        x + offset, y + offset,
                        anchor="nw",
                        image=self.obstacle_img
                    )

        # draw dirt (only if still exists)
        # Iterate over all dirt positions that haven't been cleaned yet
        for (r, c) in self.env.dirt_positions:
            # Calculate the pixel X for this dirt cell
            x = c * self.CELL_SIZE
            # Calculate the pixel Y for this dirt cell
            y = r * self.CELL_SIZE
            # Draw the dirt image on top of the floor tile at this position
            self.canvas.create_image(x, y, anchor="nw", image=self.dirt_img)

        # draw vacuum
        # If the animation hasn't started yet, show the vacuum at the initial starting position
        if self.current_step == 0:
            # Use the environment's defined start cell (row, col)
            r, c = self.env.start
        else:
            # Otherwise show the vacuum at the last position it moved to in the path
            r, c = self.path[self.current_step - 1]

        # Convert the vacuum's current row/col to pixel X coordinate
        x = c * self.CELL_SIZE
        # Convert the vacuum's current row/col to pixel Y coordinate
        y = r * self.CELL_SIZE

        # Draw the vacuum image on top of everything else at its current position
        self.canvas.create_image(x, y, anchor="nw", image=self.vacuum_img)

        # Update the cost label text in the UI to reflect the current accumulated cost
        self.info_label.configure(text=f"Cost: {self.current_cost}")

    # Method called when the "Start Cleaning" button is clicked
    def start_animation(self):
        # Only begin if not already animating — prevents double-triggering
        if not self.animating:
            # Set the flag to indicate animation is now running
            self.animating = True
            # Trigger the first step of the animation loop
            self.animate_step()

    # Recursive method that processes and visualizes one step of the path at a time
    def animate_step(self):

        # Check if all steps in the path have been completed
        if self.current_step >= len(self.path):
            # Mark animation as finished
            self.animating = False
            # Ring the system bell as an audio signal that cleaning is complete
            self.bell()
            # Exit the method — nothing more to animate
            return

        # Only calculate movement cost from the second step onward (need a previous position to compare)
        if self.current_step > 0:
            # Get the cell the vacuum was at before this step
            prev = self.path[self.current_step - 1]
            # Get the cell the vacuum is moving to in this step
            curr = self.path[self.current_step]

            # If the row decreased, the vacuum moved upward on the grid
            if curr[0] < prev[0]:
                # Moving UP has the highest cost of 2
                self.current_cost += 2
            # If the row increased, the vacuum moved downward on the grid
            elif curr[0] > prev[0]:
                # Moving DOWN is free (cost of 0)
                self.current_cost += 0
            # Otherwise the row stayed the same, meaning horizontal movement (LEFT or RIGHT)
            else:
                # Horizontal movement costs 1
                self.current_cost += 1

        # Unpack the row and column of the current destination cell
        r, c = self.path[self.current_step]

        # remove dirt when vacuum reaches it
        # Check if the vacuum has arrived at a cell that still has dirt
        if (r, c) in self.env.dirt_positions:
            # Remove this position from the dirt list — it's now cleaned
            self.env.dirt_positions.remove((r, c))

        # Advance the step counter so the next call processes the following path position
        self.current_step += 1
        # Redraw the entire grid to show the vacuum's updated position and any cleaned dirt
        self.draw_grid()

        # Schedule the next call to animate_step after SPEED milliseconds (non-blocking, event-loop based)
        self.after(self.SPEED, self.animate_step)

    # Method called when the "Restart" button is clicked to reset everything
    def restart(self):
        # Create a brand-new 4x4 environment with freshly randomized dirt and obstacles
        self.env = VacuumEnvironment(size=4)
        # Re-run the AI solver on the new environment to get a new path, cost, and unreachable info
        self.path, self.total_cost, self.unreachable = solve_vacuum(self.env)
        
        # --- ADDED THIS LINE TO UPDATE REPORT ON RESTART ---
        # Append the new solution details to solution.txt for the restarted run
        write_solution(self.env, self.path, self.total_cost)
        
        # Reset the step counter back to 0 (vacuum returns to start)
        self.current_step = 0
        # Reset the cost display back to 0
        self.current_cost = 0
        # Reset the animation flag so a new animation can be started fresh
        self.animating = False
        # Redraw the grid to display the new environment's initial state
        self.draw_grid()


# Standard Python entry point check — only runs if this file is executed directly, not imported as a module
if __name__ == "__main__":
    # Create an instance of the VacuumGUI application, which triggers __init__ and builds the window
    app = VacuumGUI()
    # Start the tkinter event loop — keeps the window open and listens for user interactions
    app.mainloop()