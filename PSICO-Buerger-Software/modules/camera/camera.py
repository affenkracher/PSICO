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
        self.fileName = self.queryController.queryId + "_" + str(uuid.uuid1()) + "_onStartUp.png"

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
        self.addToCameraLog(self.queryController.storage, self.fileName)
        self.deleteCamera(cam)

    """
    Add a base64 encoded string of a image to the CameraPictures field, can be decoded to
    view as png
    """
    def addToCameraLog(self, storage, fileName):
        blob = storage.blob("Pictures/" + fileName)
        blob.upload_from_filename(filename=fileName, content_type="image/png")
        blob.make_public()

    """
    Only a bit unnecessary main method, take a picture after 3 seconds to get ready
    """
    def main(self):  
        time.sleep(3)
        self.record()
