import keyboard
from keyboard._keyboard_event import KeyboardEvent, KEY_UP, KEY_DOWN
import time

SHIFT_PUNCTUATION = ['!', '"', '§', '$', '%', '&', '/', '(', ')', '=', '?', ';', ':', '_', '`', '*', '\'']

KEY_INPUT_STRINGS = []

def record():
    return keyboard.record("backspace", False, False)

def deductStringInputs(keyEventStream):
    print(keyEventStream)
    keyInputs = []
    keyInputs = keyboard.get_typed_strings(keyEventStream)
    for keyInput in keyInputs:
        if keyInput != "":
            KEY_INPUT_STRINGS.append(keyInput)

def listen():
    deductStringInputs(record())

def getInputStrings():
    return KEY_INPUT_STRINGS

def write(str):
    events = stringToKeyboardEvents(str)
    keyboard.play(events)

def stringToKeyboardEvents(str = ""):
    events = []
    for s in str:
        if(s.isupper() or s in SHIFT_PUNCTUATION):
            events.append(KeyboardEvent(KEY_DOWN, "shift", "shift"))
            events.append(KeyboardEvent(KEY_DOWN, s, s))
            events.append(KeyboardEvent(KEY_UP, s, s))
            events.append(KeyboardEvent(KEY_UP, "shift", "shift"))
        else:
            events.append(KeyboardEvent(KEY_DOWN, s, s))
            events.append(KeyboardEvent(KEY_UP, s, s))
    print(events)
    return events

def main():
    """ listen()
    print(KEY_INPUT_STRINGS) """
    time.sleep(3)
    write("Hello World!")

#test
main()