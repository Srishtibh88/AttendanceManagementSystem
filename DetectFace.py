# https://machinelearningmastery.com/how-to-perform-face-detection-with-classical-and-deep-learning-methods-in-python-with-keras/
from cv2 import CascadeClassifier, imread

# load the pre-trained model
classifier = CascadeClassifier("C:/Users\ASUS\PycharmProjects\AttendanceSystem\Models\haarcascade_frontalface_alt.xml")

def detectFace(pixels):
    #pixels = cv2.cvtColor(pixels, cv2.COLOR_BGR2GRAY)
    bboxes = classifier.detectMultiScale(pixels)  # can tune scaleFactor and minNeighbours for improved results
    return bboxes

