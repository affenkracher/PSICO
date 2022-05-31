from typing import List
import keyboard
import time
from difflib import SequenceMatcher

SHIFT_PUNCTUATION = ['!', '"', '§', '$', '%', '&', '/', '(', ')', '=', '?', ';', ':', '_', '`', '*', '\'']

def readKeyInput(antiGovernmentWords: List[str], antiGovernmentSentences: List[str]):
    for badWord in antiGovernmentWords:
        keyboard.add_abbreviation(badWord, "")
    for badSentence in antiGovernmentSentences:
        keyboard.add_abbreviation(badSentence, "")
    keyboard.remap_key("tab", "space+space+space+space")
    while 1:
        lines = []
        recordingStart = time.time()
        keyboard.start_recording()
        keyboard.wait("enter")
        keyEvents = keyboard.stop_recording()
        recordingEnd = time.time()
        typedStrings = keyboard.get_typed_strings(keyEvents)
        for line in typedStrings:
            lines.append(line)
            if containes(line, "konami"):
                return
        censor(lines, antiGovernmentSentences)
        keyEvaluation = evaluateKeyUsage(lines)
        print(keyEvaluation)
        print(wpm(lines, recordingEnd, recordingStart))
        yield lines

def containes(line: str, sub: str):
    try:
        index = line.index(sub)
        return True
    except:
        return False

def censorSentences(sentences: List[str], antiGovernmentSentences: List[str]):
    reversed = sentences.copy()
    reversed.reverse()
    for sentence in reversed:
        for badSentence in antiGovernmentSentences:
            if similar(sentence, badSentence):
                deleteLine(sentence)
        moveToUpperRightLineEnd()
    moveDown(len(sentences))
    keyboard.press_and_release("end")

def censor(line: str, antiGovernmentStrings: List[str]):
    for badString in antiGovernmentStrings:
        index = line.find(badString)
        if index > 0:
            deleteLine(line)
        
def wpm(lines: List[str], recordingEnd, recordingStart):
    words = []
    for line in lines:
        words.append(line.split(" "))
    wordsPerMinute = (len(words) * 60) / (recordingEnd - recordingStart)
    return wordsPerMinute

def evaluateKeyUsage(stringList: List[str]):
    keyEvaluation = {}
    for str in stringList:
        for c in str:
            count = str.count(c)
            if c not in keyEvaluation:
                keyEvaluation[c] = count
            else:
                oldCount = keyEvaluation[c]
                keyEvaluation[c] = oldCount + count
    return keyEvaluation

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

def deleteWord(word: str):
    length = len(word)
    for _ in range(0, length):
        keyboard.press_and_release("backspace")
    keyboard.press_and_release("delete")
    return True

def deleteLine(line: str):
    length = len(line)
    for _ in range(0, length):
        keyboard.press_and_release("backspace")

def correctWord(wrongWord: str, correctWord: str):
    deleteWord(wrongWord)
    write(correctWord+" ")
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

def moveToUpperRightLineEnd():
    moveUp(1)
    keyboard.press_and_release("end")

def checkWordInSentence(sentence: str, antiGovernmentWords: List[str]):
    words = sentence.split(" ")
    foundWords = []
    for word in words:
        for anitWord in antiGovernmentWords:
            if similar(word, anitWord):
                foundWords.append(word)
    return foundWords

def checkSentences(sentences: List[str], antiGovernmentSentences: List[str]):
    foundSentences = []
    for sentence in sentences:
        for antiSentence in antiGovernmentSentences:
            if similar(sentence, antiSentence):
                foundSentences.append(sentence)
    return foundSentences

def main():
    input = readKeyInput([], ["jwt jwt"])
    for a in input:
        print(a)
    
main()