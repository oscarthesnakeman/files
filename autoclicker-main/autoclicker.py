import pyautogui
import time
import tkinter as tk
from tkinter import simpledialog, messagebox
import threading
import win32gui
import win32con
import keyboard

click_positions = []
click_interval = 5
running = False
minimized_mode = False
show_click_positions = False

def set_instance_count():
    global click_positions
    click_positions = []
    instance_count = simpledialog.askinteger("Instances", "Enter number of instances (1-8):", minvalue=1, maxvalue=8)
    if instance_count:
        instances_label.config(text=str(instance_count))
        for i in range(instance_count):
            click_positions.append(None)
        set_positions_button.config(state="normal")

def set_positions():
    global click_positions
    for i in range(len(click_positions)):
        messagebox.showinfo("Set Click Position", f"Move your mouse to instance {i+1} and press OK.")
        x, y = pyautogui.position()
        click_positions[i] = (x, y)
    save_button.config(state="normal")

def show_positions():
    global show_click_positions
    show_click_positions = not show_click_positions
    update_positions_display()

def update_positions_display():
    if show_click_positions:
        for pos in click_positions:
            if pos:
                pyautogui.moveTo(pos[0], pos[1], duration=0.5)

def toggle_minimized_mode():
    global minimized_mode
    minimized_mode = not minimized_mode
    mode_label.config(text="Minimized Mode: ON" if minimized_mode else "Minimized Mode: OFF")

def set_click_interval():
    global click_interval
    interval = simpledialog.askinteger("Interval", "Enter click interval in seconds:", minvalue=1)
    if interval:
        click_interval = interval

def start_clicking():
    global running
    if None in click_positions and not minimized_mode:
        messagebox.showerror("Error", "Please set all click positions first.")
        return
    running = True
    status_label.config(text="Status: Running")
    threading.Thread(target=click_loop, daemon=True).start()

def stop_clicking():
    global running
    running = False
    status_label.config(text="Status: Stopped")

def click_loop():
    global running
    hwnds = get_roblox_windows()
    while running:
        if minimized_mode:
            for hwnd in hwnds:
                win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, 0, 0)
                win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, 0)
        else:
            for pos in click_positions:
                if pos:
                    pyautogui.click(pos)
                    time.sleep(0.5)
        time.sleep(click_interval)

def get_roblox_windows():
    hwnds = []
    def enum_handler(hwnd, _):
        if "roblox" in win32gui.GetWindowText(hwnd).lower():
            hwnds.append(hwnd)
    win32gui.EnumWindows(enum_handler, None)
    return hwnds

def show_help(message):
    messagebox.showinfo("Help", message)

# Create the main window
root = tk.Tk()
root.title("Roblox Autoclicker")
root.geometry("300x400")
root.resizable(False, False)

instances_label = tk.Label(root, text="1", font=("Arial", 14))
instances_label.grid(row=0, column=0, padx=5, pady=5)

instance_button = tk.Button(root, text="Instances", command=set_instance_count)
instance_button.grid(row=0, column=0, padx=5, pady=5)

instance_question_button = tk.Button(root, text="?", command=lambda: show_help("Set the number of instances."))
instance_question_button.grid(row=0, column=1, padx=2, pady=5)

set_positions_button = tk.Button(root, text="Set Click Positions", state="disabled", command=set_positions)
set_positions_button.grid(row=1, column=0, padx=5, pady=5)

set_positions_question_button = tk.Button(root, text="?", command=lambda: show_help("Set the click positions for each instance."))
set_positions_question_button.grid(row=1, column=1, padx=2, pady=5)

show_positions_button = tk.Button(root, text="Show Click Positions", command=show_positions)
show_positions_button.grid(row=2, column=0, padx=5, pady=5)

show_positions_question_button = tk.Button(root, text="?", command=lambda: show_help("Show or hide the click positions on the screen."))
show_positions_question_button.grid(row=2, column=1, padx=2, pady=5)

save_button = tk.Button(root, text="Save", state="disabled")
save_button.grid(row=3, column=0, padx=5, pady=5)

interval_button = tk.Button(root, text="Set Click Interval", command=set_click_interval)
interval_button.grid(row=4, column=0, padx=5, pady=5)

interval_question_button = tk.Button(root, text="?", command=lambda: show_help("Set the interval in seconds between each click."))
interval_question_button.grid(row=4, column=1, padx=2, pady=5)

mode_button = tk.Button(root, text="Toggle Minimized Mode", command=toggle_minimized_mode)
mode_button.grid(row=5, column=0, padx=5, pady=5)

mode_question_button = tk.Button(root, text="?", command=lambda: show_help("Enable or disable minimized mode where the game can be in the background."))
mode_question_button.grid(row=5, column=1, padx=2, pady=5)

mode_label = tk.Label(root, text="Minimized Mode: OFF", font=("Arial", 12))
mode_label.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

status_label = tk.Label(root, text="Status: Stopped", font=("Arial", 12))
status_label.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

start_button = tk.Button(root, text="Start", bg="green", command=start_clicking)
start_button.grid(row=8, column=0, padx=5, pady=10)

stop_button = tk.Button(root, text="Stop", bg="red", command=stop_clicking)
stop_button.grid(row=8, column=1, padx=5, pady=10)

keybind_info = tk.Label(root, text="Keybinds: Start - Ctrl+Alt+S, Stop - Ctrl+Alt+X", font=("Arial", 10))
keybind_info.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

keyboard.add_hotkey("ctrl+alt+s", start_clicking)
keyboard.add_hotkey("ctrl+alt+x", stop_clicking)

root.mainloop()
