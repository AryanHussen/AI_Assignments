import tkinter as tk
import customtkinter as ctk
from logic import VacuumEnvironment, solve_vacuum
from PIL import Image, ImageTk
from report_writer import write_solution

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class VacuumGUI(ctk.CTk):

    CELL_SIZE = 120
    OBSTACLE_SIZE = 70
    SPEED = 600

    def __init__(self):
        super().__init__()

        self.title("Smart Vacuum Cleaner AI")
        self.state("zoomed")

        self.env = VacuumEnvironment(size=4)
        self.path, self.total_cost, self.unreachable = solve_vacuum(self.env)
        
        # --- ADDED THIS LINE TO GENERATE INITIAL REPORT ---
        write_solution(self.env, self.path, self.total_cost)

        self.current_step = 0
        self.current_cost = 0
        self.animating = False

        self.load_images()
        self.create_layout()
        self.draw_grid()

    def load_images(self):
        self.floor_img = ImageTk.PhotoImage(
            Image.open("assets/floor.png").resize((self.CELL_SIZE, self.CELL_SIZE))
        )
        self.obstacle_img = ImageTk.PhotoImage(
            Image.open("assets/obstacle.png").resize((self.OBSTACLE_SIZE, self.OBSTACLE_SIZE))
        )
        self.dirt_img = ImageTk.PhotoImage(
            Image.open("assets/dirt.png").resize((self.CELL_SIZE, self.CELL_SIZE))
        )
        self.vacuum_img = ImageTk.PhotoImage(
            Image.open("assets/vacuum.png").resize((self.CELL_SIZE, self.CELL_SIZE))
        )

    def create_layout(self):

        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.pack(pady=20, fill="x")

        self.title_label = ctk.CTkLabel(
            self.top_frame,
            text="SMART VACUUM CLEANER",
            font=("Arial", 30, "bold")
        )
        self.title_label.pack()

        self.canvas = tk.Canvas(
            self,
            width=self.env.size * self.CELL_SIZE,
            height=self.env.size * self.CELL_SIZE,
            highlightthickness=0
        )
        self.canvas.pack(pady=20)

        self.bottom_frame = ctk.CTkFrame(self)
        self.bottom_frame.pack(pady=20)

        self.start_btn = ctk.CTkButton(
            self.bottom_frame,
            text="Start Cleaning",
            command=self.start_animation,
            width=200,
            height=50
        )
        self.start_btn.pack(side="left", padx=20)

        self.restart_btn = ctk.CTkButton(
            self.bottom_frame,
            text="Restart",
            command=self.restart,
            width=200,
            height=50,
            fg_color="gray"
        )
        self.restart_btn.pack(side="left", padx=20)

        self.info_label = ctk.CTkLabel(
            self.bottom_frame,
            text="Cost: 0",
            font=("Arial", 20)
        )
        self.info_label.pack(side="left", padx=40)

    def draw_grid(self):
        self.canvas.delete("all")

        for r in range(self.env.size):
            for c in range(self.env.size):
                x = c * self.CELL_SIZE
                y = r * self.CELL_SIZE

                self.canvas.create_image(x, y, anchor="nw", image=self.floor_img)

                if self.env.grid[r][c] == "#":
                    offset = (self.CELL_SIZE - self.OBSTACLE_SIZE) // 2
                    self.canvas.create_image(
                        x + offset, y + offset,
                        anchor="nw",
                        image=self.obstacle_img
                    )

        # draw dirt (only if still exists)
        for (r, c) in self.env.dirt_positions:
            x = c * self.CELL_SIZE
            y = r * self.CELL_SIZE
            self.canvas.create_image(x, y, anchor="nw", image=self.dirt_img)

        # draw vacuum
        if self.current_step == 0:
            r, c = self.env.start
        else:
            r, c = self.path[self.current_step - 1]

        x = c * self.CELL_SIZE
        y = r * self.CELL_SIZE

        self.canvas.create_image(x, y, anchor="nw", image=self.vacuum_img)

        self.info_label.configure(text=f"Cost: {self.current_cost}")

    def start_animation(self):
        if not self.animating:
            self.animating = True
            self.animate_step()

    def animate_step(self):

        if self.current_step >= len(self.path):
            self.animating = False
            self.bell()
            return

        if self.current_step > 0:
            prev = self.path[self.current_step - 1]
            curr = self.path[self.current_step]

            if curr[0] < prev[0]:
                self.current_cost += 2
            elif curr[0] > prev[0]:
                self.current_cost += 0
            else:
                self.current_cost += 1

        r, c = self.path[self.current_step]

        # remove dirt when vacuum reaches it
        if (r, c) in self.env.dirt_positions:
            self.env.dirt_positions.remove((r, c))

        self.current_step += 1
        self.draw_grid()

        self.after(self.SPEED, self.animate_step)

    def restart(self):
        self.env = VacuumEnvironment(size=4)
        self.path, self.total_cost, self.unreachable = solve_vacuum(self.env)
        
        # --- ADDED THIS LINE TO UPDATE REPORT ON RESTART ---
        write_solution(self.env, self.path, self.total_cost)
        
        self.current_step = 0
        self.current_cost = 0
        self.animating = False
        self.draw_grid()


if __name__ == "__main__":
    app = VacuumGUI()
    app.mainloop()
