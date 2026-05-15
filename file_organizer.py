import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import json

# Define file categories and their extensions
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
    "Documents": [".pdf", ".docx", ".doc", ".xlsx", ".xls", ".pptx", ".txt"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Programs": [".exe", ".msi", ".sh", ".bat", ".py"],
    "Others": []  # For files that don't fit into the above categories
}

UNDO_LOG_FILE = "undo_log.json"

# Function to organize files
def organize_files(directory):
    if not os.path.exists(directory):
        messagebox.showerror("Error", f"Directory '{directory}' does not exist.")
        return

    file_movements = []  # To store file movements for undo

    # Create folders for categories
    for category in FILE_CATEGORIES.keys():
        category_folder = os.path.join(directory, category)
        os.makedirs(category_folder, exist_ok=True)

    # Iterate through files in the directory
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        
        # Skip directories
        if os.path.isdir(file_path):
            continue

        # Determine file category
        file_extension = os.path.splitext(file)[1].lower()
        category_found = False
        
        for category, extensions in FILE_CATEGORIES.items():
            if file_extension in extensions:
                target_folder = os.path.join(directory, category)
                new_path = shutil.move(file_path, target_folder)
                file_movements.append({"from": new_path, "to": file_path})
                category_found = True
                break

        # If no category matches, move to 'Others'
        if not category_found:
            target_folder = os.path.join(directory, "Others")
            new_path = shutil.move(file_path, target_folder)
            file_movements.append({"from": new_path, "to": file_path})

    # Save movements to the undo log
    with open(UNDO_LOG_FILE, "w") as log_file:
        json.dump(file_movements, log_file)

    messagebox.showinfo("Success", f"Files in '{directory}' have been organized. You can undo this operation.")

# Function to undo the last organization
def undo_last_operation():
    if not os.path.exists(UNDO_LOG_FILE):
        messagebox.showwarning("Warning", "No undo log found. No operations to undo.")
        return

    with open(UNDO_LOG_FILE, "r") as log_file:
        file_movements = json.load(log_file)

    for movement in file_movements:
        if os.path.exists(movement["from"]):
            shutil.move(movement["from"], movement["to"])

    os.remove(UNDO_LOG_FILE)
    messagebox.showinfo("Success", "Last operation has been undone.")

# Function to browse directory
def browse_directory():
    directory = filedialog.askdirectory(title="Select Directory")
    if directory:
        entry_directory.delete(0, tk.END)
        entry_directory.insert(0, directory)

# Function to handle organize button
def handle_organize():
    directory = entry_directory.get()
    if not directory:
        messagebox.showwarning("Warning", "Please select a directory.")
    else:
        organize_files(directory)

# Create the GUI
root = tk.Tk()
root.title("File Organizer with Undo")

# Directory input
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(pady=10)

label_directory = tk.Label(frame, text="Directory:")
label_directory.grid(row=0, column=0, padx=5, pady=5)

entry_directory = tk.Entry(frame, width=50)
entry_directory.grid(row=0, column=1, padx=5, pady=5)

button_browse = tk.Button(frame, text="Browse", command=browse_directory)
button_browse.grid(row=0, column=2, padx=5, pady=5)

# Organize and Undo buttons
button_organize = tk.Button(root, text="Organize Files", command=handle_organize, bg="green", fg="white")
button_organize.pack(pady=5)

button_undo = tk.Button(root, text="Undo Last Operation", command=undo_last_operation, bg="red", fg="white")
button_undo.pack(pady=5)

# Run the GUI event loop
root.mainloop()
