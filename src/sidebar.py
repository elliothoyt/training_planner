from tkinter import ttk

def create_sidebar(parent, show_frame, frames_dict, quit_command, start_selected_script,script):
    sidebar = ttk.Frame(parent)
    sidebar.pack(side='left', fill='y')

    button_frame = ttk.Frame(sidebar)
    button_frame.pack(fill="x", padx=10, pady=10, side='top')

    ttk.Button(button_frame, text="Configure Week Schedule",
               command=lambda: show_frame(frames_dict['config']),
               width=30).pack(side="top", padx=5)

    ttk.Button(button_frame, text="Write Weekly Training Plan",
               command=lambda: show_frame(frames_dict['week']),
               width=30).pack(side="top", padx=5)

    ttk.Button(button_frame, text="Push Weekly Plan to GCal",
               command=lambda: start_selected_script(script, frames_dict['output_input']),
               width=30).pack(side="top", padx=5)

    ttk.Button(sidebar, text="Quit",
               command=quit_command,
               width=30).pack(side="bottom", padx=5)

    return sidebar

