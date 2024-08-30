import tkinter as tk
from tkinter import ttk

# Initialize the main application window
root = tk.Tk()
root.title("Modern GUI Interface")

# Set the window size
root.geometry("600x400")

# Apply a modern theme to the application
style = ttk.Style()
style.theme_use('clam')  # Use the 'clam' theme for a modern look

# Create the main frame that will hold the two sections
main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill=tk.BOTH, expand=True)

# Create the left frame for the keyboard section
left_frame = ttk.Frame(main_frame, borderwidth=2, relief="ridge", padding="10")
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Add a label in the left frame
keyboard_label = ttk.Label(left_frame, text="Keyboard", font=("Helvetica", 16))
keyboard_label.pack(expand=True)

# Create the right frame for the remote section
right_frame = ttk.Frame(main_frame, borderwidth=2, relief="ridge", padding="10")
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Add a label in the right frame
remote_label = ttk.Label(right_frame, text="Remote", font=("Helvetica", 16))
remote_label.pack(expand=True)

# Run the application
root.mainloop()
