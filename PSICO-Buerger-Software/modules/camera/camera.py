import cv2
import time
import os
import uuid

"""
The CameraLogger is a module designed to take and save a pictures
"""

def getCWD():
    CWD = os.getcwd()
    if CWD.find("\\PSICO-Buerger-Software") >= 0:
        cut = len("\\PSICO-Buerger-Software")
        CWD = CWD[0:-cut]
    return CWD

class CameraLogger():
    def __init__(self, queryController):
        """
        Add a storagePath to store the pictures
        """
        self.queryController = queryController
        self.pictureId = 0
        self.fileName = self.queryController.queryId + "_" + str(self.queryController.lastImgID) + ".png"

    """
    Take one picture with the primary camera / webcam device of the system
    """
    def takePicture(self, camera):
        _, image = camera.read()
        return image

    """
    For presentation and test purposes show the newly taken picture in a image show window
    """
    def showPicture(self, image):
        cv2.imshow('test.png',image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    """
    Delete the camera connection to stop data leaks
    """
    def deleteCamera(self, camera):
        del(camera)

    """
    Record a picture by creating a new camera instance, then taking and showing the picture of the user and 
    storing it in the before-mentioned storage
    """
    def record(self):
        cam = cv2.VideoCapture(0)
        if cam is None or not cam.isOpened():
            print('Warning: no camera found')
            return
        picture = self.takePicture(cam)
        cv2.imwrite(self.fileName, picture)
        self.pictureId = self.pictureId + 1
        self.queryController.addToCameraLog(self.fileName)
        self.deleteCamera(cam)


    """
    Only a bit unnecessary main method, take a picture after 3 seconds to get ready
    """
    def main(self):  
        time.sleep(3)
        self.record()
