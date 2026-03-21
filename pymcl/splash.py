import tkinter as tk
from tkinter import ttk
import random

TIPS = [
    "Tip: You can right-click on a mod to see more options.",
    "Tip: PyMCL is open source!",
    "Tip: Check the settings to customize your experience.",
    "Tip: You can drag and drop mods into the window (soon).",
    "Tip: Press F5 to refresh the mod list (if implemented).",
    "Did you know? PyMCL is written in Python.",
    "Tip: Make sure you have Java installed so that you can load mods.",
    "Tip: PyMCL supports Modrinth for easy mod management.",
    "Tip: Keep an eye on the console for detailed logs.",
    "Tip: Report bugs and suggest features on GitHub!",
    "Tip: Have patience, good things take time to load.",
    "Tip: Customize your game experience with different Minecraft versions.",
    "Tip: Always back up your saves!",
    "Tip: Make sure your internet connection is stable for downloads.",
    "Tip: Explore new mods on Modrinth.com.",
    "Tip: Compilation speed depends on how fast your processor is.",
    "Tip: Subsequent launches will be much faster.",
]

# Color palette matching the main app theme
BG      = "#0d1015"
CARD    = "#131720"
BORDER  = "#1e2530"
ACCENT  = "#3b82f6"
TEXT    = "#e5e7eb"
SUBTEXT = "#6b7280"
WHITE   = "#ffffff"


class Splash(tk.Tk):
    def __init__(self):
        super().__init__()
        self.overrideredirect(True)  # Frameless window

        width, height = 460, 230
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.configure(bg=BG)
        self.resizable(False, False)

        self.canvas = tk.Canvas(
            self, width=width, height=height,
            highlightthickness=0, bg=BG
        )
        self.canvas.pack(fill="both", expand=True)

        # Outer border (simulated rounded card via rectangle)
        self.canvas.create_rectangle(
            1, 1, width - 1, height - 1,
            outline=BORDER, fill=CARD, width=1
        )

        # Accent top stripe
        self.canvas.create_rectangle(
            0, 0, width, 3,
            outline="", fill=ACCENT
        )

        # App name — large, bold
        self.canvas.create_text(
            width // 2, 52,
            text="PyMCL",
            font=("Segoe UI", 26, "bold"),
            fill=WHITE,
            anchor="center"
        )

        # Tagline
        self.canvas.create_text(
            width // 2, 84,
            text="Python Minecraft Launcher",
            font=("Segoe UI", 10),
            fill=SUBTEXT,
            anchor="center"
        )

        # Separator line
        self.canvas.create_line(
            40, 106, width - 40, 106,
            fill=BORDER, width=1
        )

        # Status label (updated dynamically)
        self.status_id = self.canvas.create_text(
            width // 2, 124,
            text="Awaiting PyQt6 compilation…",
            font=("Segoe UI", 9),
            fill=SUBTEXT,
            anchor="center"
        )

        # Progress bar via ttk
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Splash.Horizontal.TProgressbar",
            troughcolor=BORDER,
            background=ACCENT,
            borderwidth=0,
            thickness=4,
        )
        self.progress = ttk.Progressbar(
            self,
            orient="horizontal",
            length=width - 80,
            mode="indeterminate",
            style="Splash.Horizontal.TProgressbar",
        )
        self.canvas.create_window(width // 2, 148, window=self.progress)
        self.progress.start(8)

        # Tip text
        self.tips_sequence = list(TIPS)
        random.shuffle(self.tips_sequence)
        priority = "Tip: Subsequent launches will be much faster."
        if priority in self.tips_sequence:
            self.tips_sequence.remove(priority)
            self.tips_sequence.insert(random.randint(0, min(2, len(self.tips_sequence))), priority)
        self.tip_index = 0

        self.tip_id = self.canvas.create_text(
            width // 2, 196,
            text="",
            font=("Segoe UI", 9, "italic"),
            fill=SUBTEXT,
            width=width - 60,
            justify="center",
            anchor="center"
        )

        self.update()
        self.update_tip()

    def update_tip(self):
        if not self.tips_sequence:
            return
        tip = self.tips_sequence[self.tip_index]
        self.canvas.itemconfigure(self.tip_id, text=tip)
        self.tip_index = (self.tip_index + 1) % len(self.tips_sequence)
        self.after(5000, self.update_tip)


def main():
    app = Splash()
    app.mainloop()


if __name__ == "__main__":
    main()
