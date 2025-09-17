import tkinter as tk
import subprocess
import threading
import sys
import os
import sv_ttk
import src
from tkinter import scrolledtext, messagebox
from queue import Queue, Empty
from tkinter import ttk
from datetime import datetime
from src import welcome_frame, output_input_frame, config_frame, week_frame, sidebar

def valid_time(t):
    try:
        datetime.strptime(t, "%H:%M")
        return True
    except ValueError:
        return False


def load_config(config_path="data/config.json"):
    with open(config_path, 'r') as f:
        return json.load(f)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
calendarwrite_script = os.path.join(BASE_DIR, "src/calendarwrite.py")


root = tk.Tk()
root.title("Training Planner GUI")
sv_ttk.set_theme("dark")



class InteractiveRunner:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.process = None
        self.queue = Queue()

    def start_script(self, script_path):
        """Start the Python script interactively."""
        # Clear old text
        self.text_widget.delete("1.0", tk.END)

        # -u runs Python in unbuffered mode for instant output
        cmd = [sys.executable, "-u", script_path]

        # Start subprocess with pipes
        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # merge stdout and stderr
            stdin=subprocess.PIPE,
            text=True,
            bufsize=0
        )

        # Start thread to read output (character by character)
        threading.Thread(target=self._enqueue_output, daemon=True).start()

        # Start updating GUI
        self.text_widget.after(50, self._update_text)

    def _enqueue_output(self):
        """Read stdout char by char so we see prompts immediately."""
        while True:
            char = self.process.stdout.read(1)
            if not char:
                break
            self.queue.put(char)
        self.process.stdout.close()

    def _update_text(self):
        """Pull output chars from queue into text widget."""
        try:
            while True:
                char = self.queue.get_nowait()
                self.text_widget.insert(tk.END, char)
                self.text_widget.see(tk.END)
        except Empty:
            pass

        if self.process and self.process.poll() is None:
            self.text_widget.after(50, self._update_text)
        else:
            self.text_widget.insert(tk.END, "\n--- Script finished ---\n")
            self.text_widget.see(tk.END)

    def stop_script(self):
        """Terminate the running process."""
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.text_widget.insert(tk.END, "\n--- Script terminated ---\n")
            self.text_widget.see(tk.END)


def start_selected_script(script_path):
    runner.start_script(script_path)

def close_window(root):
    root.destroy()


# ---------------- keyboard shortcuts -----------------
root.bind_all('<Control-q>', lambda event: root.quit())
root.bind_all('<Command-q>', lambda event: root.quit())

# ---------------- Container for frames ----------------
container = ttk.Frame(root)
container.pack(fill="both", expand=True, side='right')

frame_welcome = welcome_frame.create_frame(container)
frame_output_input, output_text = output_input_frame.create_frame(container)
frame_config = config_frame.create_frame(container)
frame_week = week_frame.create_frame(container)

for frame in (frame_welcome, frame_config,frame_week,frame_output_input):
    frame.grid(row=0, column=0, sticky='nsew')

def show_frame(frame):
    frame.tkraise()

frames_dict = {
    'welcome': frame_welcome,
    'output_input': frame_output_input,
    'config': frame_config,
    'week': frame_week,
}

# ---------------- sidebar nav ----------------
sidebar.create_sidebar(root, show_frame, frames_dict,
                       quit_command=root.quit,
                       start_script=calendarwrite_script)

# ---------------- Frame Switching ----------------
def show_frame(frame):
    frame.tkraise()

# Start with the output/input frame
show_frame(frame_welcome)

# ---------------- Interactive Runner ----------------
runner = InteractiveRunner(output_text)

def start_selected_script(script_path, frame_to_show):
    """Switch frames then start script."""
    show_frame(frame_to_show)
    runner.start_script(script_path)



root.mainloop()

