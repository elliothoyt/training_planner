import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import threading
import sys
import os
from queue import Queue, Empty
from tkinter import ttk
import sv_ttk
from tools.weekconfig import save_week_schedule, load_week_schedule
from datetime import datetime

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
calendarwrite_script = os.path.join(BASE_DIR, "tools/calendarwrite.py")
writeweek_script = os.path.join(BASE_DIR, "tools/writeweek.py")
weekconfig_script = os.path.join(BASE_DIR, "tools/weekconfig.py")


root = tk.Tk()
root.title("Training Planner GUI")
sv_ttk.set_theme("dark")
#root.geometry("800x800")



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

    def send_input(self, user_input):
        """Send a line to the running script's stdin."""
        if self.process and self.process.poll() is None:
            self.process.stdin.write(user_input + "\n")
            self.process.stdin.flush()
        else:
            self.text_widget.insert(tk.END, "\n[Process not running]\n")
            self.text_widget.see(tk.END)

    def stop_script(self):
        """Terminate the running process."""
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.text_widget.insert(tk.END, "\n--- Script terminated ---\n")
            self.text_widget.see(tk.END)


def start_selected_script(script_path):
    runner.start_script(script_path)


def send_user_input():
    user_input = input_box.get("1.0", tk.END).strip()
    input_box.delete("1.0", tk.END)
    runner.send_input(user_input)


# ---------------- Container for frames ----------------
container = ttk.Frame(root)
container.pack(fill="both", expand=True)

# We’ll build two frames (screens) and stack them
frame_output_input = ttk.Frame(container)
frame_config = ttk.Frame(container)

for frame in (frame_output_input, frame_config):
    frame.grid(row=0, column=0, sticky='nsew')

# ---------------- Frame A: Output + Input ----------------
output_frame = tk.LabelFrame(frame_output_input, text="Output", padx=5, pady=5)
output_frame.pack(fill="both", expand=True, padx=10, pady=5)

output_text = scrolledtext.ScrolledText(output_frame, height=5)
output_text.pack(fill="both", expand=True)

input_frame = tk.LabelFrame(frame_output_input, text="Input", padx=5, pady=5)
input_frame.pack(fill="x", padx=10, pady=5)

input_box = tk.Text(input_frame, height=3)
input_box.pack(fill="x")

# ---------------- Frame B: Weekly config ----------------
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
inter_frame=ttk.Frame(frame_config)
inter_frame.pack(anchor='center')
# Create a frame to hold rows
rows_frame = ttk.Frame(inter_frame)
rows_frame.pack(fill="both", expand=True, padx=10, pady=10)

# column headers
header_day = ttk.Label(rows_frame, text="Day", font=("Arial", 12, "bold"))
header_day.grid(row=0, column=0, padx=5, pady=5)
header_time = ttk.Label(rows_frame, text="Time (HH:MM)", font=("Arial", 12, "bold"))
header_time.grid(row=0, column=1, padx=5, pady=5)

# store references to comboboxes and entries
day_selectors = []
time_entries = []


for i in range(14):  # one row per day or more if needed
    cb = ttk.Combobox(rows_frame, values=days_of_week, width=12)
    cb.grid(row=i+1, column=0, padx=5, pady=3)
    entry = ttk.Entry(rows_frame, width=10)
    entry.grid(row=i+1, column=1, padx=5, pady=3)

    day_selectors.append(cb)
    time_entries.append(entry)

#load existing
existing_schedule = load_week_schedule()

for i, cb in enumerate(day_selectors):
    if i < len(existing_schedule):
        # match by day name
        day = list(existing_schedule.keys())[i]
        time = existing_schedule[day]
        cb.set(day)
        time_entries[i].insert(0, time)
# Button to read all data
def get_schedule():
    schedule = []
    for cb, entry in zip(day_selectors, time_entries):
        day = cb.get().strip()
        time = entry.get().strip()
        if day and time:
            schedule.append({"day": day, "time": time})
    print("Schedule:", schedule)  # or feed to weekconfig/save JSON
    save_week_schedule(schedule)

btn_save = ttk.Button(frame_config, text="Save Schedule", command=get_schedule)
btn_save.pack(pady=10)
# ---------------- Frame Switching ----------------
def show_frame(frame):
    frame.tkraise()

# Start with the output/input frame
show_frame(frame_output_input)

# ---------------- Interactive Runner ----------------
runner = InteractiveRunner(output_text)

def start_selected_script(script_path, frame_to_show):
    """Switch frames then start script."""
    show_frame(frame_to_show)
    runner.start_script(script_path)

# ---------------- Buttons to launch scripts ----------------
button_frame = tk.Frame(root)
button_frame.pack(fill="x", padx=10, pady=10)

btn1 = ttk.Button(button_frame, text="Push Weekly Plan to GCal",
                  command=lambda: start_selected_script(calendarwrite_script, frame_output_input),
                  width=30)
btn1.pack(side="left", padx=5)

btn2 = ttk.Button(button_frame, text="Write Weekly Training Plan",
                  command=lambda: start_selected_script(writeweek_script, frame_config),
                  width=30)
btn2.pack(side="left", padx=5)

btn3 = ttk.Button(button_frame, text="Configure Week Schedule",
    command=lambda: show_frame(frame_config),width=30)  # show frame_config
btn3.pack(side="left", padx=5)

root.mainloop()

