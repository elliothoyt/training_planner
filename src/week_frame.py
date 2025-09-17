import tkinter as tk
from tkinter import ttk
from src.tools import load_week_schedule, save_week_schedule, save_to_csv
import src.tools as tools

def create_frame(parent):
    frame_week=ttk.Frame(parent)

    interweek_frame=ttk.Frame(frame_week)
    interweek_frame.pack(anchor='nw')
    # Create a frame to hold rows
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


    #load existing
    existing_schedule = tools.load_week_schedule()
    days_list=list(existing_schedule.keys())
    days= []
    times = []
    summaries = []
    descriptions = []
    #grid for weekly schedule
    for i in range(len(existing_schedule)):
        day=ttk.Label(rows_frame,text=days_list[i])
        day.grid(row=i+1,column=0,padx=5,pady=5)
        time=ttk.Label(rows_frame,text=existing_schedule[days_list[i]])
        time.grid(row=i+1,column=1,padx=5,pady=5)
        summary = ttk.Entry(rows_frame, width=10)
        summary.grid(row=i+1, column=2, padx=5, pady=3)
        description = ttk.Entry(rows_frame, width=50)
        description.grid(row=i+1, column=3, padx=5, pady=3)
        days.append(days_list[i])
        times.append(existing_schedule[days_list[i]])
        summaries.append(summary)
        descriptions.append(description)

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


