import DetectFace
from imutils import paths
from PIL import Image
from numpy import asarray, expand_dims
from cv2 import os, imwrite, rectangle, imshow, imread
from numpy import savez
import ExtractEmbeddings

def Store_Embeddings(course, branch, year):
    path = "C:/Users/ASUS/Desktop/Dataset/" + course + "/" + branch + "/" + str(year)
    imagePaths = list(paths.list_images(path+"/images"))
    for imagePath in imagePaths:
        print(imagePath)
        pixels = imread(imagePath)
        bboxes = DetectFace.detectFace(pixels)
        if len(bboxes) == 1:
            # extract
            x1, y1, width, height = bboxes[0]
            x2, y2 = x1 + width, y1 + height
            # draw a rectangle over the pixels
            face = pixels[y1:y2, x1:x2]
            #rectangle(pixels, (x1, y1), (x2, y2), (0, 0, 255), 1)
            imwrite(imagePath, face)
        else:
            os.remove(imagePath)

    faceEmbeddings = []
    requiredSize = (160, 160)
    imagePaths = list(paths.list_images(path+"/images"))
    save_path = path+"/model"
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    id = []
    for imagePath in imagePaths:
        image = Image.open(imagePath)
        id.append(imagePath.split(os.path.sep)[-2])
        # convert to RGB, if needed
        image = image.convert('RGB')
        # resize image
        image = image.resize(requiredSize)
        # convert to array
        pixels = asarray(image)
        # get embeddings
        embeddings = ExtractEmbeddings.getEmbeddings(pixels)
        faceEmbeddings.append(embeddings)

    print(id)
    faceEmbeddings = asarray(faceEmbeddings)
    id = asarray(id)
    savez(os.path.join(save_path, 'trainDataEmbedding.npz'), faceEmbeddings, id)




