import tkinter as tk
from tkinter import ttk
from src.tools import load_week_schedule, save_week_schedule

def create_frame(parent):
    frame = ttk.Frame(parent)
    days_of_week = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

    inter_frame = ttk.Frame(frame)
    inter_frame.pack(anchor='center')

    rows_frame = ttk.Frame(inter_frame)
    rows_frame.pack(fill="both", expand=True, padx=10, pady=10)

    ttk.Label(rows_frame, text="Day", font=("Arial",12,"bold")).grid(row=0,column=0)
    ttk.Label(rows_frame, text="Time (HH:MM)", font=("Arial",12,"bold")).grid(row=0,column=1)

    day_selectors, time_entries = [], []
    for i in range(14):
        cb = ttk.Combobox(rows_frame, values=days_of_week, width=12)
        cb.grid(row=i+1,column=0,padx=5,pady=3)
        entry = ttk.Entry(rows_frame,width=10)
        entry.grid(row=i+1,column=1,padx=5,pady=3)
        day_selectors.append(cb)
        time_entries.append(entry)

    existing_schedule = load_week_schedule()
    for i, cb in enumerate(day_selectors):
        if i < len(existing_schedule):
            day = list(existing_schedule.keys())[i]
            time = existing_schedule[day]
            cb.set(day)
            time_entries[i].insert(0,time)

    def save_schedule():
        schedule = []
        for cb, entry in zip(day_selectors, time_entries):
            day = cb.get().strip()
            time = entry.get().strip()
            if day and time:
                schedule.append({"day": day, "time": time})
        save_week_schedule(schedule)

    btn_save = ttk.Button(frame, text="Save Weekly Schedule", command=save_schedule)
    btn_save.pack(pady=10)

    return frame

