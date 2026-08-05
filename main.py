from pynput import keyboard

def on_press(key):
    print(repr(key))
    try:
        if key.char == 'a':
            print("Naciśnięto A")
    except AttributeError:
        pass

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()