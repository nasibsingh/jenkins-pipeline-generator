import tkinter as tk
from tkinter import messagebox
import os

def run_frontend_generator():
    """Runs the frontend pipeline generator script."""
    os.system("python3 /Users/memorres/Desktop/pipeline-generator/frontend-pipeline-generator.py")

def run_backend_generator():
    """Runs the backend pipeline generator script."""
    os.system("python3 /Users/memorres/Desktop/pipeline-generator/backend-pipeline-generator.py")

def generate_pipeline(selection):
    if selection == "1":
        run_frontend_generator()
        messagebox.showinfo("Success", "Frontend Pipeline Generated Successfully!")
    elif selection == "2":
        run_frontend_generator()
        messagebox.showinfo("Success", "Backend Pipeline Generated Successfully!")
    else:
        messagebox.showerror("Error", "Invalid selection. Please choose either 1 (Frontend) or 2 (Backend).")

def submit_choice():
    choice = entry.get()
    generate_pipeline(choice)

# GUI setup

root = tk.Tk()
root.title("Pipeline Generator")

# Instruction Label
label = tk.Label(root, text="Which pipeline do you want to generate?\n1. Frontend Pipeline\n2. Backend Pipeline")
label.pack(pady=10)

# Input Entry
entry = tk.Entry(root)
entry.pack(pady=5)

# Submit Button
submit_button = tk.Button(root, text="Submit", command=submit_choice)
submit_button.pack(pady=10)

# Run the GUI loop
root.mainloop()
