import tkinter as tk
from tkinter import ttk
import random
import sys
import time
import threading

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
    "Tip: PyMCL aims for a smooth and intuitive user experience.",
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
        
        # Main label
        self.label = tk.Label(
            self, 
            text="PyMCL", 
            font=("Segoe UI", 24, "bold"), 
            bg='#2b2b2b', 
            fg='white'
        )
        self.label.pack(pady=(40, 10))
        
        # Loading text
        self.loading_label = tk.Label(
            self, 
            text="Loading...", 
            font=("Segoe UI", 12), 
            bg='#2b2b2b', 
            fg='#cccccc'
        )
        self.loading_label.pack(pady=(0, 20))

        # Tip label
        self.tip_label = tk.Label(
            self,
            text=random.choice(TIPS),
            font=("Segoe UI", 10, "italic"),
            bg='#2b2b2b',
            fg='#aaaaaa',
            wraplength=350
        )
        self.tip_label.pack(side="bottom", pady=20)

        # Progress bar (indeterminate)
        self.progress = ttk.Progressbar(self, orient="horizontal", length=300, mode="indeterminate")
        self.progress.pack(pady=10)
        self.progress.start(10)

        # Force update to show immediately
        self.update()

        # Start tip cycling
        self.update_tip()

    def update_tip(self):
        new_tip = random.choice(TIPS)
        self.tip_label.config(text=new_tip)
        self.after(5000, self.update_tip)

def main():
    app = Splash()
    app.mainloop()

if __name__ == "__main__":
    main()
