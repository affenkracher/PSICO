from win10toast import ToastNotifier

"""
Creating a new windows 10 popup with a message, title and duration. Automatically
disappears after the duration has run out
"""
class PopUp():
    def __init__(self):
        self.alive = 1

    def createPopUp(self, title, msg, duration,):
        toaster = ToastNotifier()
        toaster.show_toast(title, msg, duration=duration)