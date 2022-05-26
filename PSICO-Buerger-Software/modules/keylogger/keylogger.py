import keyboard

KEY_INPUT = []
KEY_INPUT_STRINGS = []

def record():
    return keyboard.record("backspace", False, False)

def deductStringInputs(keyEventStream):
    KEY_INPUT = []
    KEY_INPUT = keyboard.get_typed_strings(keyEventStream)
    for keyInput in KEY_INPUT:
        if keyInput != "":
            KEY_INPUT_STRINGS.append(keyInput)

def listen():
    deductStringInputs(record())

def getInputStrings():
    return KEY_INPUT_STRINGS

def main():
    listen()
    print(KEY_INPUT_STRINGS)

#test
#main()