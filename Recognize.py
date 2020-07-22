from PIL import Image
from numpy import asarray, expand_dims
import DetectFace as df
import pickle
import cv2
from imutils import paths
from ExtractEmbeddings import getEmbeddings
import UpdateAttendanceSheet


def recognize(course, branch, year, subject, test_images):
    course = course.lower()
    branch = branch.lower()
    year = str(year)
    path = "C:/Users/ASUS/Desktop/Resources/" + course + "/" + branch + "/" + year
    recognizer =pickle.loads(open(path + '/recognizer.pickle', "rb").read())
    le = pickle.loads(open( path + '/labels.pickle', "rb").read())
    requiredSize = (160,160)
    rollset = {"-1"}

    for imagePath in test_images:
        pixels = cv2.imread(imagePath)
        bboxes = df.detectFace(pixels)
        image = Image.open(imagePath)
        for box in bboxes:
            x1, y1, width, height = box
            x2, y2 = x1 + width, y1 + height
            # draw a rectangle over the pixels
            face = image.crop((x1,y1,x2,y2))
            # convert to RGB, if needed
            face = face.convert('RGB')
            # resize image
            face = face.resize(requiredSize)
            # convert to array
            face = asarray(face)
            # get embeddings
            embeddings = getEmbeddings(face)
            # prediction for the face
            samples = expand_dims(embeddings, axis=0)
            id = recognizer.predict(samples)
            probability = recognizer.predict_proba(samples)
            # get name
            label = id[0]
            predictedProb = probability[0, label] * 100
            predictedLabel = le.inverse_transform(id)
            if(predictedProb>50):
                rollset.add(str(predictedLabel[0]))
                text = "Roll= " +predictedLabel[0] + " (" +  str(round(predictedProb,2)) + ")"
                print('Predicted: %s (%.2f)' % (predictedLabel[0], predictedProb))
            else:
                text= "Unknown"

            #y = x1 - 10 if y1 - 10 > 10 else y1 + 10
            cv2.rectangle(pixels, (x1, y1), (x2, y2),(0, 0, 255), 2)
            cv2.putText(pixels, text, (x1, y1-5),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

        cv2.imshow("Press any key for next", pixels)
        cv2.waitKey(0)

    rollset.remove("-1")
    #print(rollset)
    UpdateAttendanceSheet.markAttendance(rollset, course, branch, year, subject)
    return len(rollset)
