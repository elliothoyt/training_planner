import tkinter as tk
from tkinter import ttk
from src.tools import load_week_schedule, save_week_schedule, save_to_csv
import src.tools as tools

'''
def populate_frame(frame_week):
    #load existing
    existing_schedule = tools.load_week_schedule()
    days= []
    times = []
    summaries = []
    descriptions = []
    #grid for weekly schedule
    for i, entry in enumerate(existing_schedule):
        day_name = entry.get("day","")
        time_val = entry.get("time","")
        summary_val = entry.get("summary","")
        desc_val = entry.get("description","")
        day=ttk.Label(rows_frame,text=day_name)
        day.grid(row=i+1,column=0,padx=5,pady=5)
        time=ttk.Label(rows_frame,text=time_val)
        time.grid(row=i+1,column=1,padx=5,pady=5)
        summary = ttk.Entry(rows_frame, width=10)
        summary.grid(row=i+1, column=2, padx=5, pady=3)
        summary.insert(0, summary_val)
        description = ttk.Entry(rows_frame, width=50)
        description.grid(row=i+1, column=3, padx=5, pady=3)
        description.insert(0, desc_val)
        days.append(day_name)
        times.append(time_val)
        summaries.append(summary)
        descriptions.append(description)

'''


def create_frame(parent):
    frame_week=ttk.Frame(parent)

    interweek_frame=ttk.Frame(frame_week)
    interweek_frame.pack(anchor='nw')

    rows_frame = ttk.Frame(interweek_frame)
    rows_frame.pack(fill="both", expand=True, padx=10, pady=10)

    header_day = ttk.Label(rows_frame, text="Day")
    header_day.grid(row=0, column=0, padx=5, pady=5)
    header_time = ttk.Label(rows_frame, text="Time (HH:MM)")
    header_time.grid(row=0, column=1, padx=5, pady=5)
    header_summary = ttk.Label(rows_frame, text="Title")
    header_summary.grid(row=0, column=2, padx=5, pady=5)
    header_summary = ttk.Label(rows_frame, text="Description")
    header_summary.grid(row=0, column=3, padx=5, pady=5)


    days_labels = []
    times_labels = []
    summaries_entries = []
    descriptions_entries = []
    for i in range(14):  # max rows
        day_label = ttk.Label(rows_frame, text="")
        day_label.grid(row=i+1, column=0, padx=5, pady=5)
        time_label = ttk.Label(rows_frame, text="")
        time_label.grid(row=i+1, column=1, padx=5, pady=5)

        summary_entry = ttk.Entry(rows_frame, width=10)
        summary_entry.grid(row=i+1, column=2, padx=5, pady=3)
        desc_entry = ttk.Entry(rows_frame, width=50)
        desc_entry.grid(row=i+1, column=3, padx=5, pady=3)

        days_labels.append(day_label)
        times_labels.append(time_label)
        summaries_entries.append(summary_entry)
        descriptions_entries.append(desc_entry)

    # attach to frame for later use
    frame_week.days = days_labels
    frame_week.times = times_labels
    frame_week.summaries = summaries_entries
    frame_week.descriptions = descriptions_entries
    # Button to save week
    def save_csv():
        csv = []
        for day, time, summary, description in zip(days,times,summaries,descriptions):
            summary = summary.get().strip()
            description = description.get().strip()
            if day and time and summary and description:
                csv.append({"day": day, "time": time, "summary": summary, "description": description})
        print("Schedule:", csv)  # or feed to save JSON
        save_to_csv(csv)

    btn_save = ttk.Button(frame_week, text="Save Schedule", command=save_csv)
    btn_save.pack(pady=10, side="bottom")
    
    return frame_week


def populate_frame(frame_week):
    """Reload JSON into the widgets on the frame."""
    existing_schedule = load_week_schedule()
    
    # clear old contents
    for day_label, time_label, summary_entry, desc_entry in zip(
        frame_week.days, frame_week.times, frame_week.summaries, frame_week.descriptions):
        day_label.config(text="")
        time_label.config(text="")
        summary_entry.delete(0, tk.END)
        desc_entry.delete(0, tk.END)

    for i, sched_item in enumerate(existing_schedule):
        if i < len(frame_week.days):
            day = sched_item.get("day", "")
            time = sched_item.get("time", "")
            summary = sched_item.get("summary", "")
            description = sched_item.get("description", "")

            frame_week.days[i].config(text=day)
            frame_week.times[i].config(text=time)
            frame_week.summaries[i].insert(0, summary)
            frame_week.descriptions[i].insert(0, description)


