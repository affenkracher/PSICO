import cv2
import os

class CameraLogger():
    def __init__(self, queryController):
        self.queryController = queryController
        self.storagePath = os.getcwd() + "\\PSICO-Buerger-Software\\modules\\camera\\storage\\"

    def takePicture(self, camera):
        _, image = camera.read()
        return image

    def showPicture(self, image):
        cv2.imshow('test.png',image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def deleteCamera(self, camera):
        del(camera)

    def record(self):
        cam = cv2.VideoCapture(0)
        if cam is None or not cam.isOpened():
            print('Warning: no camera found')
            return
        picture = self.takePicture(cam)
        self.queryController.addToCameraLog(picture)
        self.deleteCamera(cam)
