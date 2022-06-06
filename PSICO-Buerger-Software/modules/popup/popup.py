from win10toast import ToastNotifier

class PopUp():
    def init(self):
        self.alive = 1

    def createPopUp(self, title, msg, duration,):
        toaster = ToastNotifier()
        toaster.show_toast(title, msg, duration=duration)