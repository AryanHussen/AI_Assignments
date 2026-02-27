import tkinter as tk
import customtkinter as ctk
from logic import VacuumEnvironment, solve_vacuum
from PIL import Image, ImageTk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class VacuumGUI(ctk.CTk):
    CELL_SIZE = 130
    OBSTACLE_SIZE = 75  # smaller than cell
    ANIMATION_SPEED = 400  # delay in ms, slower

    def __init__(self):
        super().__init__()
        self.title("🤖 Smart Vacuum Cleaner AI")
        self.state('zoomed')
        self.resizable(True, True)

        self.create_gradient_background()
        self.reset_environment()
        self.load_images()
        self.create_frames()
        self.create_widgets()
        self.draw_grid()

    def create_gradient_background(self):
        self.bg_canvas = tk.Canvas(self, width=self.winfo_screenwidth(), height=self.winfo_screenheight(), highlightthickness=0)
        self.bg_canvas.place(x=0, y=0)
        for i in range(0, self.winfo_screenheight()):
            color = f'#{20+i//8:02x}{30+i//10:02x}{60+i//12:02x}'
            self.bg_canvas.create_line(0, i, self.winfo_screenwidth(), i, fill=color)

    def reset_environment(self):
        self.env = VacuumEnvironment(size=4, dirt_count=5)
        self.path, self.total_cost, self.unreachable = solve_vacuum(self.env)
        self.current_step = 0
        self.current_cost = 0
        self.animating = False

    def load_images(self):
        self.floor_img = ImageTk.PhotoImage(Image.open("assets/floor.png").resize((self.CELL_SIZE, self.CELL_SIZE)))
        self.obstacle_img = ImageTk.PhotoImage(Image.open("assets/obstacle.png").resize((self.OBSTACLE_SIZE, self.OBSTACLE_SIZE)))
        self.dirt_img = ImageTk.PhotoImage(Image.open("assets/dirt.png").resize((self.CELL_SIZE, self.CELL_SIZE)))
        self.vacuum_img = ImageTk.PhotoImage(Image.open("assets/vacuum.png").resize((self.CELL_SIZE, self.CELL_SIZE)))

    def create_frames(self):
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.pack(pady=20, fill='x')

        self.canvas_frame = ctk.CTkFrame(self)
        self.canvas_frame.pack(pady=10, expand=True)

        self.bottom_frame = ctk.CTkFrame(self)
        self.bottom_frame.pack(pady=10, fill='x')

    def create_widgets(self):
        self.title_label = ctk.CTkLabel(self.top_frame, text="SMART VACUUM CLEANER AI", font=("Arial", 32, "bold"))
        self.title_label.pack()

        self.canvas = tk.Canvas(self.canvas_frame, width=self.env.size*self.CELL_SIZE,
                                height=self.env.size*self.CELL_SIZE, highlightthickness=0)
        self.canvas.pack(expand=True)

        self.start_button = ctk.CTkButton(self.bottom_frame, text="▶ Start Cleaning",
                                          command=self.start_animation, width=220, height=50)
        self.start_button.pack(side='left', padx=30)
        self.restart_button = ctk.CTkButton(self.bottom_frame, text="🔄 Restart",
                                            command=self.restart, width=220, height=50, fg_color="gray")
        self.restart_button.pack(side='left', padx=30)

        self.info_label = ctk.CTkLabel(self.bottom_frame, text="", font=("Arial", 20))
        self.info_label.pack(side='left', padx=40)

    def draw_grid(self):
        self.canvas.delete("all")
        for r in range(self.env.size):
            for c in range(self.env.size):
                x = c*self.CELL_SIZE
                y = r*self.CELL_SIZE
                self.canvas.create_image(x, y, anchor="nw", image=self.floor_img)
                if self.env.grid[r][c] == "#":
                    offset = (self.CELL_SIZE - self.OBSTACLE_SIZE)//2
                    self.canvas.create_image(x+offset, y+offset, anchor="nw", image=self.obstacle_img)
                elif (r, c) in self.env.dirt_positions:
                    self.canvas.create_image(x, y, anchor="nw", image=self.dirt_img)
                elif (r, c) in getattr(self.env, 'unreachable', []):
                    self.canvas.create_oval(x+25, y+25, x+self.CELL_SIZE-25, y+self.CELL_SIZE-25, fill="red")

        if self.current_step == 0:
            r, c = self.env.start
        else:
            r, c = self.path[self.current_step-1]
        x = c*self.CELL_SIZE
        y = r*self.CELL_SIZE
        self.canvas.create_oval(x+30, y+90, x+self.CELL_SIZE-30, y+self.CELL_SIZE-20, fill="black", stipple="gray50")
        self.canvas.create_image(x, y, anchor="nw", image=self.vacuum_img)

        remaining = len(self.env.dirt_positions)
        self.info_label.configure(text=f"Step: {self.current_step} / Cost: {self.current_cost} / Remaining dirt: {remaining}")

    def start_animation(self):
        if not self.path or self.animating:
            return
        self.animating = True
        self.animate_step()

    def animate_step(self):
        if self.current_step >= len(self.path):
            msg = f"✅ Finished! Total Cost = {self.current_cost}"
            if getattr(self.env, 'unreachable', []):
                msg += f" | ⚠ Unreachable dirt: {len(self.env.unreachable)}"
            self.info_label.configure(text=msg)
            self.bell()
            self.after(150, self.bell)
            self.animating = False
            return

        if self.current_step > 0:
            prev_r, prev_c = self.path[self.current_step-1]
            curr_r, curr_c = self.path[self.current_step]
            dr = curr_r - prev_r
            dc = curr_c - prev_c
            if dr == -1:
                self.current_cost += 2
            elif dr == 1:
                self.current_cost += 0
            elif dc == -1:
                self.current_cost += 1
            elif dc == 1:
                self.current_cost += 1

        r, c = self.path[self.current_step]
        if (r, c) in self.env.dirt_positions:
            self.env.dirt_positions.remove((r, c))

        self.current_step += 1
        self.draw_grid()
        self.after(self.ANIMATION_SPEED, self.animate_step)

    def restart(self):
        self.current_step = 0
        self.current_cost = 0
        self.reset_environment()
        self.draw_grid()
        self.animating = False


if __name__ == "__main__":
    app = VacuumGUI()
    app.mainloop()
