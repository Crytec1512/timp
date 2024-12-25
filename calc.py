import tkinter as tk
from tkinter import messagebox

def on_button_click(char):
    if char == "=":
        try:
            result = eval(entry.get())
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result))
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
    elif char == "C":
        entry.delete(0, tk.END)
    else:
        entry.insert(tk.END, char)

# Create main window
root = tk.Tk()
root.title("Simple Calculator")

# Entry widget for input and output
entry = tk.Entry(root, width=30, font=("Arial", 14), bd=5, justify="right")
entry.grid(row=0, column=0, columnspan=4, pady=10)

# Buttons
buttons = [
    "7", "8", "9", "/",
    "4", "5", "6", "*",
    "1", "2", "3", "-",
    "C", "0", "=", "+"
]

row = 1
col = 0
for button in buttons:
    action = lambda x=button: on_button_click(x)
    tk.Button(root, text=button, width=5, height=2, font=("Arial", 14), command=action).grid(row=row, column=col, padx=5, pady=5)
    col += 1
    if col > 3:
        col = 0
        row += 1

# Run the application
root.mainloop()
