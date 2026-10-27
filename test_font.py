import tkinter as tk
from tkinter import font


root = tk.Tk()
root.title("Zen Dots test")
root.geometry("700x300")

available_fonts = font.families()

print("Zen Dots" in available_fonts)

if "Zen Dots" in available_fonts:
    print("Zen Dots найден!")
else:
    print("Zen Dots НЕ найден.")

label = tk.Label(
    root,
    text="Backup Manager",
    font=("Zen Dots", 40),
)

label.pack(pady=40)

button = tk.Button(
    root,
    text="Exit",
    font=("Zen Dots", 24),
)

button.pack()

root.mainloop()