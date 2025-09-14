import tkinter as tk
from tkinter import scrolledtext, messagebox
import subprocess
import threading
import sys
import os
from queue import Queue, Empty
from tkinter import ttk
import sv_ttk




BASE_DIR = os.path.dirname(os.path.abspath(__file__))

calendarwrite_script = os.path.join(BASE_DIR, "tools/calendarwrite.py")
writeweek_script = os.path.join(BASE_DIR, "tools/writeweek.py")
weekconfig_script = os.path.join(BASE_DIR, "tools/weekconfig.py")

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



# GUI Setup
root = tk.Tk()
root.title("Training Planner")


# This is where the magic happens
sv_ttk.set_theme("dark")


# Frame for buttons
button_frame = ttk.Frame(root)
button_frame.pack(fill="x", padx=10, pady=5)

btn1 = ttk.Button(button_frame, text="Push Weekly Plan to GCal",
                 command=lambda: start_selected_script(calendarwrite_script),
                 width=30)
btn1.pack(side="left", padx=5)

btn2 = ttk.Button(button_frame, text="Write Weekly Training Plan",
                 command=lambda: start_selected_script(writeweek_script),
                 width=30)
btn2.pack(side="left", padx=5)

btn3 = ttk.Button(button_frame, text="Configure Week Schedule",
                 command=lambda: start_selected_script(weekconfig_script),
                 width=30)
btn3.pack(side="left", padx=5)

# Output Text Area
output_frame = tk.LabelFrame(root, text="Output", padx=5, pady=5)
output_frame.pack(fill="both", expand=True, padx=10, pady=5)

output_text = scrolledtext.ScrolledText(output_frame, height=20)
output_text.pack(fill="both", expand=True)

runner = InteractiveRunner(output_text)

# Frame for input
input_frame = tk.LabelFrame(root, text="User Input", padx=5, pady=5)
input_frame.pack(fill="x", padx=10, pady=5)

input_box = tk.Text(input_frame, height=3)
input_box.pack(fill="x")


send_btn = ttk.Button(root, text="Send Input to Script", command=send_user_input, width=25)
send_btn.pack(side="left", padx=5)

stop_btn = ttk.Button(root, text="Stop Script", command=runner.stop_script, width=25)
stop_btn.pack(side="right", padx=5)

# Quit button
quit_btn = ttk.Button(root, text="Quit", command=root.quit, width=20)
quit_btn.pack(pady=10)

root.mainloop()

