# Needed Modules
import cv2

path = "file"

"""
def connectCamera():
    cam = cv2.VideoCapture(0)
    if cam is None or not cam.isOpened():
        print('Warning: no camera found')
    else:
        print('camera connected')
        return cam
"""

def takePicture(camera):
    _, image = camera.read()
    return image

def showPicture(image):
    cv2.imshow('test.png',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def deleteCamera(camera):
    del(camera)

def savePicture(path, picture):
    cv2.imwrite(path, picture)


def record():
    cam = cv2.VideoCapture(0)
    if cam is None or not cam.isOpened():
        print('Warning: no camera found')
    else:
        print('camera connected')
        showPicture(takePicture(cam))
        #savePicture(path, takePicture(cam))
        deleteCamera(cam)

#test
#record()