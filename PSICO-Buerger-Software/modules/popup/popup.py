#pip install win10toast
from win10toast import ToastNotifier

def createPopUp(title, msg, duration):    
    toaster = ToastNotifier()
    toaster.show_toast(title, msg, duration=duration)