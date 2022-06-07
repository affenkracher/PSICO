import cv2
import os
import base64
import time

"""
The CameraLogger is a module designed to take and save a pictures
"""

class CameraLogger():
    def __init__(self, queryController):
        self.queryController = queryController
        """
        Add a storagePath to store the pictures
        """
        self.storagePath = os.getcwd() + "\\PSICO-Buerger-Software\\modules\\camera\\storage\\"


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
        self.showPicture(picture)
        self.deleteCamera(cam)

    """
    Only a bit unnecessary main method, take a picture after 3 seconds to get ready
    """
    def main(self):
        time.sleep(3)
        self.record()
