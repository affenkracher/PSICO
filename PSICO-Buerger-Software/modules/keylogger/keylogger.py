from typing import List
import keyboard
from keyboard._keyboard_event import KeyboardEvent, KEY_UP, KEY_DOWN
import time
from difflib import SequenceMatcher

SHIFT_PUNCTUATION = ['!', '"', '§', '$', '%', '&', '/', '(', ')', '=', '?', ';', ':', '_', '`', '*', '\'']

def record():
    executionTimeStart = time.time()
    return (keyboard.record("backspace", False, False), executionTimeStart)

def deductStringInputs(keyEventStream):
    keyInputStream, executionTimeStart = keyEventStream
    keyInputs = keyboard.get_typed_strings(keyInputStream, True)
    executionTimeEnd = time.time()
    keyInputStrings = []
    for keyInput in keyInputs:
        if keyInput != "":
            keyInputStrings.append(keyInput)
    evaluation = evaluateUsage(keyInputStrings)
    words = {word for string in keyInputStrings for word in string.split(" ")}
    wordsPerMinute = (len(words) * 60 / (executionTimeEnd - executionTimeStart))
    if wordsPerMinute < 100:
        print(f'Produktivität niedrig: WPM = {wordsPerMinute}')
    return keyInputStrings

def evaluateUsage(stringList: List[str]):
    keyEvaluation = {}
    for str in stringList:
        for c in str:
            if not c in keyEvaluation:
                keyEvaluation[c] = str.count(c)
    return keyEvaluation

def listen():
    return deductStringInputs(record())

def write(string: str):
    for c in string:
        if c.isupper() or c in SHIFT_PUNCTUATION:
            keyboard.press("shift")
            keyboard.press_and_release(f'{c.lower()}')
            keyboard.release("shift")
        else:
            keyboard.press_and_release(f'{c}')

def similar(a: str, b: str):
    return SequenceMatcher(None, a, b).ratio() > 0.75

def deleteWordInLine(sentence: str, word: str):
    try:
        leftIndex = sentence.index(word)
        rightIndex = leftIndex + len(word)
        moveLeft(len(sentence)-rightIndex)
        deleteWord(word)
        newSenctence = sentence[:leftIndex] + sentence[rightIndex+1:]
        moveRight(len(sentence)-rightIndex)
        return newSenctence
    except:
        return ""

def deleteAllInLine(line: str, word: str):
    newLine = line
    while contains(newLine, word):
        newLine = deleteWordInLine(newLine, word)
    return newLine

def deleteWord(word: str):
    length = len(word)
    for _ in range(0, length):
        keyboard.press_and_release("backspace")
    keyboard.press_and_release("delete")
    return True

def deleteLine(sentence: str):
    length = len(sentence)
    for _ in range(0, length):
        keyboard.press_and_release("backspace")

def correctWord(wrongWord: str, correctWord: str):
    deleteWord(wrongWord)
    write(correctWord+" ")
    return True

def contains(input: str, substring: str):
    for word in input.split(" "):
        if similar(word, substring):
            return True
    return False

def getSimilar(input: str, substing: str):
    for word in input.split(" "):
        if similar(word, substing):
            return word

def censorLine(line: str, badWords: List[str]):
    for badWord in badWords:
        nl = line
        while contains(nl, badWord):
            nl = deleteAllInLine(line, getSimilar(line, badWord))

def censor(keyInputString: List[str], badWords: List[str]):
    copied = keyInputString.copy()
    copied.reverse()
    correctedSentences = []
    for index, input in enumerate(copied):
        correctedSentence = censorLine(input, badWords)
        correctedSentences.append(correctedSentence)
        moveToUpperRightLineEnd()
    return correctedSentences

def moveRight(len: int):
    for i in range(0, len):
        keyboard.press_and_release("right")

def moveLeft(len: int):
    for i in range(0, len):
        keyboard.press_and_release("left")

def moveUp(len: int):
    for i in range(0, len):
        keyboard.press_and_release("up")

def moveDown(len: int):
    for i in range(0, len):
        keyboard.press_and_release("down")

def moveToUpperRightLineEnd():
    moveUp(1)
    keyboard.press_and_release("end")

def main():
    """ time.sleep(3)
    write("Dear World, Hello World!") """
    """ time.sleep(2)
    deleteWordInLine("Dear World, Hello World!", "Dear") """
    """ time.sleep(1)
    deleteWordInLine(deleteWordInLine(deleteWordInLine("Dear World, Hello World!", "Hello"), "Dear"), "World!") """
    lines = listen()
    censor(lines, ["awd", "jwt"])
    """ time.sleep(3)
    moveToUpperRightLineEnd()
 """
main()