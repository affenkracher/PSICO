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

def checkForBadWords(listOfBadWords: List[str], sentence: str):
    for word in sentence.split(" "):
        if word == "" or word == " ":
            continue
        for badWord in listOfBadWords:
            if SequenceMatcher(None, word, badWord).ratio() > 0.75:
                index = sentence.index(word)
                return (True, word, index)
    return (False, "", 0)

def deleteWordInKeyInput(keyInputStrings: List[str], listOfBadWords: List[str]):
    reversedInputStrings = keyInputStrings.reverse()
    moveRight(len(reversedInputStrings))
    for index, line in enumerate(reversedInputStrings):
        for word in line:
            bad, wordToDelete, indexOfWordToDelete = checkForBadWords(listOfBadWords, line)
            if bad:
                correctedSentence = deleteWordInSentence(line, wordToDelete)
                reversedInputStrings[index] = correctedSentence
                moveRight(len(reversedInputStrings[index]))

def deleteWordInSentence(sentence: str, word: str):
    try:
        leftIndex = sentence.index(word)
        rightIndex = leftIndex + len(word)
        moveLeft(len(sentence)-rightIndex)
        deleteWord(word)
        newSenctence = sentence[:leftIndex] + sentence[rightIndex+1:]
        moveRight(len(sentence)-rightIndex)
        return newSenctence
    except:
        return

def deleteWord(word: str):
    length = len(word)
    for _ in range(0, length):
        keyboard.press_and_release("backspace")
    keyboard.press_and_release("delete")

def correctWord(wrongWord: str, correctWord: str):
    deleteWord(wrongWord)
    write(correctWord)
    return True

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

def moveToUpperLineEnd(currentLine: str, upperLine = ""):
    if len(upperLine) == 0:
        return
    moveUp(1)
    underLength = len(currentLine)
    upperLength = len(upperLine)
    diff = upperLength - underLength
    if diff < 0:
        moveLeft(diff)
    else:
        moveRight(diff)

def containsBadWord(input: str, badWord: str):
    try:
        index = input.index(badWord)
        if index:
            return True
        return False
    except:
        return False

def censor(keyInputString: List[str], badWords: List[str]):
    copied = keyInputString.copy()
    copied.reverse()
    correctedSentences = []
    for index, inputString in enumerate(copied):
        words = inputString.split(" ")
        correctedSentence = inputString
        for word in words:
            for badWord in badWords:
                while containsBadWord(correctedSentence, badWord):
                    correctedSentence = deleteWordInSentence(correctedSentence, word)
                    correctedSentences.append(correctedSentence)
        if index < len(copied) - 1:
            moveToUpperLineEnd(correctedSentence, copied[index+1])
    return correctedSentences

def main():
    """ time.sleep(3)
    write("Dear Hello World!")
    time.sleep(1)
    deleteWordInSentence(deleteWordInSentence("Dear Hello World!", "Hello"), "Dear") """
    words = listen()
    censor(words, ["awd"])

main()