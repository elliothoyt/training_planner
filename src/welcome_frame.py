import tkinter as tk
from tkinter import ttk
from src.tools import WELCOMETEXT

def create_frame(parent):
    frame = ttk.Frame(parent)
    label = ttk.Label(frame, text=WELCOMETEXT, padding=5)
    label.pack(fill="both", expand=True)
    return frame
