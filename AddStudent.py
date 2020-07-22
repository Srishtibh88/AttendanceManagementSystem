import cv2
import os

def store_capture(datalist):
    (course, branch, year, roll) = datalist
    path = "C:\\Users\\ASUS\\Desktop\\Dataset"
    cap = cv2.VideoCapture(0)
    path = path + "/" + course
    if not os.path.isdir(path):
        os.mkdir(path)
    path = path +  "/" + branch
    if not os.path.isdir(path):
        os.mkdir(path)
    path = path + "/" + year
    if not os.path.isdir(path):
        os.mkdir(path)
    path = path + "/images"
    if not os.path.isdir(path):
        os.mkdir(path)
    path =path + "/" + roll
    if not os.path.isdir(path):
        os.mkdir(path)

    path = path +"/"

    count=0
    while(True):
        ret, image = cap.read()
        if not ret:
            continue
        cv2.imshow(roll,image)
        count += 1
        cv2.imwrite(os.path.join(path, roll + '_%d.jpg' % count), image)
        count += 1
        if count >=40:
            break;

    cap.release()
    cv2.destroyAllWindows()
