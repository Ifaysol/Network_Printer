import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os
import subprocess
from client import send_print_request


def select_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("All Supported Files", "*.pdf *.docx *.xlsx"), 
                  ("PDF Files", "*.pdf"), 
                  ("Word Documents", "*.docx"),
                  ("Excel Files", "*.xlsx")]
    )
    if file_path:
        file_label.config(text=f"Selected: {os.path.basename(file_path)}")
        file_label.file_path = file_path


def process_print():
    if hasattr(file_label, 'file_path'):
        file_path = file_label.file_path
        response = send_print_request(file_path)
        root.after(0, lambda: messagebox.showinfo("Print Status", response.get("message", "Unknown Error")))
    else:
        root.after(0, lambda: messagebox.showwarning("No File Selected", "Please select a file before printing."))


def open_file_in_default_viewer(file_path):
    """Opens the selected file in the default viewer based on the OS."""
    try:
        if os.name == 'nt':  # Windows
            os.startfile(file_path)
        elif os.name == 'posix':  # macOS & Linux
            subprocess.run(['xdg-open', file_path], check=True)
    except Exception as e:
        messagebox.showerror("Error", f"Could not open file: {str(e)}")


def open_and_print_file():
    if hasattr(file_label, 'file_path'):
        open_file_in_default_viewer(file_label.file_path)
        process_print()


# Tkinter GUI
root = tk.Tk()
root.title("R&D")
root.geometry("400x300")
root.configure(bg="#f4f4f4")

header = tk.Label(root, text="📄 Central Maintenance Printer", font=("Arial", 14, "bold"), bg="#f4f4f4", fg="#333")
header.pack(pady=10)

select_btn = ttk.Button(root, text="📂 Select File", command=select_file)
select_btn.pack(pady=10)

file_label = tk.Label(root, text="No file selected", font=("Arial", 10), bg="#f4f4f4", fg="#555")
file_label.pack(pady=5)

print_btn = ttk.Button(root, text="🖨 Print File", command=open_and_print_file)
print_btn.pack(pady=20)

root.mainloop()