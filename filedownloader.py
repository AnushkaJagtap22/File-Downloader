import requests
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def download_file():
    url = url_entry.get().strip()
    filename = file_entry.get().strip()

    if not url.startswith(('http://', 'https://')):
        messagebox.showerror("Invalid URL", "URL must start with http:// or https://")
        return

    if not filename:
        filename = "downloaded_file.html"
    elif '.' not in filename:
        filename += ".html"

    if os.path.exists(filename):
        if not messagebox.askyesno("File Exists", f"'{filename}' already exists. Overwrite?"):
            return

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        progress_bar["maximum"] = total_size
        progress_bar["value"] = 0

        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    progress_bar["value"] += len(chunk)
                    root.update_idletasks()

        messagebox.showinfo("Success", f"Downloaded content from {url} to {filename}")

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Download Failed", f"Error fetching URL:\n{e}")
    except IOError as e:
        messagebox.showerror("File Error", f"Error saving file:\n{e}")

# --- GUI Setup ---
root = tk.Tk()
root.title("URL Fetcher 📥")
root.geometry("400x220")
root.resizable(False, False)

tk.Label(root, text="Enter URL:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack()

tk.Label(root, text="Save As (filename):").pack(pady=5)
file_entry = tk.Entry(root, width=50)
file_entry.pack()

progress_bar = ttk.Progressbar(root, length=360, mode='determinate')
progress_bar.pack(pady=10)

download_button = tk.Button(root, text="Download", command=download_file, bg="#4CAF50", fg="white")
download_button.pack(pady=10)

root.mainloop()
