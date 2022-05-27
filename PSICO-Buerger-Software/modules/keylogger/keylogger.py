from typing import List
import keyboard
from keyboard._keyboard_event import KeyboardEvent, KEY_UP, KEY_DOWN
import time
from difflib import SequenceMatcher

SHIFT_PUNCTUATION = ['!', '"', '§', '$', '%', '&', '/', '(', ')', '=', '?', ';', ':', '_', '`', '*', '\'']

KEY_INPUT_STRINGS = []

def record():
    executionTimeStart = time.time()
    return (keyboard.record("backspace", False, False), executionTimeStart)

def deductStringInputs(keyEventStream):
    keyInputStream, executionTimeStart = keyEventStream
    keyInputs = keyboard.get_typed_strings(keyInputStream)
    executionTimeEnd = time.time()
    keyInputStrings = []
    for keyInput in keyInputs:
        if keyInput != "":
            keyInputStrings.append(keyInput)
    evaluateUsage(keyInputStrings)
    words = {word for string in keyInputStrings for word in string.split(" ")}
    wordsPerMinute = (len(words) * 60 / (executionTimeEnd - executionTimeStart))
    if wordsPerMinute < 200:
        print(f'Produktivität niedrig: WPM = {wordsPerMinute}')
    return keyInputStrings

def evaluateUsage(stringList: List[str]):
    keyEvaluation = {}
    for str in stringList:
        for c in str:
            if not c in keyEvaluation:
                keyEvaluation[c] = str.count(c)
    return keyEvaluation

def checkForBadWords(listOfBadWords: List[str], listOfWordsToCheck):
    counter = 0
    for word in listOfWordsToCheck:
        if word in listOfBadWords:
            counter += 1
    return counter

def checkForBadSentences(listOfBadSentences: List[str], listOfSentencesToCheck):
    counter = 0
    for sentence in listOfSentencesToCheck:
        for badSentence in listOfBadSentences:
            if SequenceMatcher(None, sentence, badSentence) > 0.75:
                counter += 1
    return counter

def listen():
    return deductStringInputs(record())

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
    return events

def main():
    words = deductStringInputs(record())
    print(words)
    print(evaluateUsage(words))
    """ time.sleep(3)
    write("Hello World!") """

#test
main()