import tkinter as tk
from tkinter import ttk, scrolledtext

def create_frame(parent):
    frame = ttk.Frame(parent)

    output_frame = tk.LabelFrame(frame, text="Output", padx=5, pady=5)
    output_frame.pack(fill="both", expand=True, padx=10, pady=5)

    output_text = scrolledtext.ScrolledText(output_frame, height=5)
    output_text.pack(fill="both", expand=True)

    return frame, output_text  # you’ll want the text widget for InteractiveRunner

