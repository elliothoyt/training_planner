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

    ttk.Label(rows_frame, text="Day").grid(row=0,column=0)
    ttk.Label(rows_frame, text="Time (HH:MM)").grid(row=0,column=1)
    ttk.Label(rows_frame, text="Default Activity").grid(row=0,column=2)
    ttk.Label(rows_frame, text="Default Description").grid(row=0,column=3)

    day_selectors, time_entries, default_summaries, default_descs = [], [], [], []
    for i in range(14):
        cb = ttk.Combobox(rows_frame, values=days_of_week, width=12)
        cb.grid(row=i+1,column=0,padx=5,pady=3)
        entry = ttk.Entry(rows_frame,width=10)
        entry.grid(row=i+1,column=1,padx=5,pady=3)
        entry2 = ttk.Entry(rows_frame,width=15)
        entry2.grid(row=i+1,column=2,padx=5,pady=3)
        entry3 = ttk.Entry(rows_frame,width=30)
        entry3.grid(row=i+1,column=3,padx=5,pady=3)
        day_selectors.append(cb)
        time_entries.append(entry)
        default_summaries.append(entry2)
        default_descs.append(entry3)

    existing_schedule = load_week_schedule()
    
    for i,item in enumerate(existing_schedule):
        if i < len(existing_schedule):
            day = item.get("day","")
            time = item.get("time","")
            summary = item.get("summary","")
            description = item.get("description","")
            day_selectors[i].set(day)
            time_entries[i].delete(0, tk.END)
            time_entries[i].insert(0,time)
            default_summaries[i].delete(0, tk.END)
            default_summaries[i].insert(0,summary)
            default_descs[i].delete(0, tk.END)
            default_descs[i].insert(0,description)

    def save_schedule():
        schedule = []
        for cb, entry,entry2, entry3 in zip(day_selectors, time_entries,default_summaries, default_descs):
            day = cb.get().strip()
            time = entry.get().strip()
            summary = entry2.get().strip()
            if not summary:
                summary = ""
            desc = entry3.get().strip()
            if not desc:
                desc = ""
            if day and time:
                schedule.append({"day": day, "time": time, "summary": summary, "description": desc})
        save_week_schedule(schedule)

    btn_save = ttk.Button(frame, text="Save Weekly Schedule", command=save_schedule)
    btn_save.pack(pady=10)

    return frame

