import tkinter as tk
from tkinter import ttk
import random

TIPS = [
    "Tip: You can right-click on a mod to see more options.",
    "Tip: PyMCL is open source!",
    "Tip: Check the settings to customize your experience.",
    "Tip: You can drag and drop mods into the window (soon).",
    "Tip: Press F5 to refresh the mod list (if implemented).",
    "Tip: Launching Minecraft...",
    "Tip: Loading assets...",
    "Tip: Checking for updates...",
    "Did you know? PyMCL is written in Python.",
    "Tip: Make sure you have Java installed.",
    "Tip: PyMCL supports Modrinth for easy mod management.",
    "Tip: Keep an eye on the console for detailed logs.",
    "Tip: Report bugs and suggest features on GitHub!",
    "Tip: Have patience, good things take time to load.",
    "Tip: Customize your game experience with different Minecraft versions.",
    "Tip: Always back up your saves!",
    "Tip: Make sure your internet connection is stable for downloads.",
    "Tip: Explore new mods on Modrinth.com.",
    "Tip: Compilation speeds depends on how fast your processor is.",
    "Tip: Subsequent launches will be much faster.",
]

class Splash(tk.Tk):
    def __init__(self):
        super().__init__()
        self.overrideredirect(True)  # Frameless window
        
        # Set size and center
        width = 400
        height = 200
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        
        self.configure(bg='#2b2b2b')
        
        # Create Canvas for gradient background
        self.canvas = tk.Canvas(self, width=width, height=height, highlightthickness=0, bg='#2b2b2b')
        self.canvas.pack(fill="both", expand=True)

        # "Awaiting PyQt6 Compilation" text
        self.canvas.create_text(
            width // 2, 30,
            text="Awaiting PyQt6 Compilation, Please Wait",
            font=("Segoe UI", 10),
            fill='#ffffff'
        )

        # "PyMCL" text
        self.canvas.create_text(
            width // 2, 70,
            text="PyMCL",
            font=("Segoe UI", 24, "bold"),
            fill='white'
        )
        
        # "Loading..." text
        self.canvas.create_text(
            width // 2, 110,
            text="Loading...",
            font=("Segoe UI", 12),
            fill='#cccccc'
        )

        # Progress bar
        self.progress = ttk.Progressbar(self, orient="horizontal", length=300, mode="indeterminate")
        self.canvas.create_window(width // 2, 140, window=self.progress)
        self.progress.start(5)

        # Prepare tips sequence with priority logic
        self.tips_sequence = list(TIPS)
        random.shuffle(self.tips_sequence)
        
        target_tip = "Tip: Subsequent launches will be much faster."
        if target_tip in self.tips_sequence:
            self.tips_sequence.remove(target_tip)
            # Insert at random position 0, 1, or 2
            insert_pos = random.randint(0, min(2, len(self.tips_sequence)))
            self.tips_sequence.insert(insert_pos, target_tip)
            
        self.tip_index = 0

        # Tip text (stored in attribute to update later)
        self.tip_text_id = self.canvas.create_text(
            width // 2, 175,
            text="", # Will be set by update_tip
            font=("Segoe UI", 10, "italic"),
            fill='#aaaaaa',
            width=350,
            justify="center"
        )

        # Force update to show immediately
        self.update()

        # Start tip cycling
        self.update_tip()

    def update_tip(self):
        if not self.tips_sequence:
            return
        new_tip = self.tips_sequence[self.tip_index]
        self.canvas.itemconfigure(self.tip_text_id, text=new_tip)
        self.tip_index = (self.tip_index + 1) % len(self.tips_sequence)
        self.after(5000, self.update_tip)

def main():
    app = Splash()
    app.mainloop()

if __name__ == "__main__":
    main()
