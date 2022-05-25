import keyboard

KEY_INPUT = []
KEY_INPUT_STRINGS = []

def listen():
    KEYBOARD_EVENTS = keyboard.record("escape", False, False)
    for keyStroke in KEYBOARD_EVENTS:
        KEY_INPUT.append(keyStroke.name)
    return "".join(KEY_INPUT)

def deductStringInputs():
    STRING = keyboard.get_typed_strings(keyboard.record("escape", False, False))
    for stri in STRING:
        if stri != "":
            KEY_INPUT_STRINGS.append(stri)

deductStringInputs()
print(KEY_INPUT_STRINGS)
