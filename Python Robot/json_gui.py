import tkinter as tk
import subprocess

def run_script():
    id = id_entry.get()
    name = name_entry.get()
    url = url_entry.get()
    classification = classification_entry.get()
    
    command = ["python", "generate_json3.py", id, name, url, classification]
    subprocess.run(command)

# Create the main window
window = tk.Tk()

# Set the window size
window.geometry("250x300")  # Set the desired width and height

# Create input fields
id_label = tk.Label(window, text="ID:")
id_label.pack()
id_entry = tk.Entry(window)
id_entry.pack()

name_label = tk.Label(window, text="Name:")
name_label.pack()
name_entry = tk.Entry(window)
name_entry.pack()

url_label = tk.Label(window, text="URL:")
url_label.pack()
url_entry = tk.Entry(window)
url_entry.pack()

classification_label = tk.Label(window, text="Classification:")
classification_label.pack()
classification_entry = tk.Entry(window)
classification_entry.pack()

# Create the "run" button
run_button = tk.Button(window, text="Run", command=run_script)
run_button.pack()

# Start the main loop
window.mainloop()
