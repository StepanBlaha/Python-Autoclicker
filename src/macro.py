from pynput import mouse, keyboard
import time
import threading

# For storing positions for macroing
macro_positions = []
mouse_listener = None
macros_running = False
fake_mouse = mouse.Controller() 


# Handle recording places clicked
def on_click(x, y, button, pressed):
    if pressed:
        action = "pressed"
        macro_positions.append([x, y, int(time.time())])
        print(f"{button} {action} at {x},{y}")

def exit_script():
    print("Script closing...")
    exit()

# Start recording macros
def start_record_macros():
    global macros_running
    macros_running = False
    global mouse_listener
    if not mouse_listener or not mouse_listener.running:
        print("starting macro listener..")
        mouse_listener = mouse.Listener(on_click=on_click)
        mouse_listener.start()

# Stop recording macros
def stop_record_macros():
    global macros_running
    macros_running = False
    global mouse_listener
    if mouse_listener and mouse_listener.running:
        mouse_listener.stop()
        print(f'Set macros: {macro_positions}')
        
# Start the loop for running macros
def start_macro():
    if len(macro_positions) < 1:
        return
    global macros_running
    macros_running = True
    # Runs the macro loop on second thread to be able to take other commands
    threading.Thread(target=macro_loop, daemon=True).start()
    
# Loop for running the macros
def macro_loop():
        global macros_running
        while macros_running:
            
            for i in range(len(macro_positions)):
                if not macros_running: 
                    break

                if i == 0:
                    fake_mouse.position = (macro_positions[i][0], macro_positions[i][1])
                    time.sleep(0.1)
                    fake_mouse.click(mouse.Button.left)
                else:
                    wait_time = macro_positions[i][2] - macro_positions[i-1][2]
                    time.sleep(max(0.1, wait_time))
                    fake_mouse.position = (macro_positions[i][0], macro_positions[i][1])
                    fake_mouse.click(mouse.Button.left)
                    
def end_macro():
    global macros_running
    macros_running = False
    print("Macro stopped")

# Start the hotkey listener
def Macros():
    hotkeys = {
        '<ctrl>+<alt>+h': start_record_macros,  # Start recording
        '<ctrl>+<alt>+q': stop_record_macros,   # Stop recording
        '<ctrl>+<alt>+g': exit_script,         # Stop the script
        '<ctrl>+<alt>+j': start_macro,         # Start macro
        '<ctrl>+<alt>+e': end_macro,           # End macro
    }
    with keyboard.GlobalHotKeys(hotkeys) as listener:
        listener.join()

if __name__ == "__main__":
    Macros()
