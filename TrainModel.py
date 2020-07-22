import os
from numpy import load
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import Normalizer
from sklearn.svm import SVC
import mysql.connector

def Train_Model(course, branch, year):
    path ="C:/Users/ASUS/Desktop/Dataset/" + course + "/" + branch + "/" + str(year)
    path = path + "/model"
    data = load(path + "/trainDataEmbedding.npz")
    trainX, trainY = data['arr_0'], data['arr_1']
    # normalize input vectors
    in_encoder = Normalizer(norm='l2')
    trainX = in_encoder.transform(trainX)
    # label encode targets
    out_encoder = LabelEncoder()
    out_encoder.fit(trainY)
    trainY = out_encoder.transform(trainY)
    # fit model
    model = SVC(kernel='linear', probability=True)
    model.fit(trainX, trainY)
    # write the actual face recognition model to disk
    f = open(path + '/recognizer.pickle', "wb")
    f.write(pickle.dumps(model))
    f.close()
    # write the label encoder to disk
    f = open(path + '/label.pickle', "wb")
    f.write(pickle.dumps(out_encoder))
    f.close()

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def Upload_Model(course, branch, year):
    path = "C:/Users/ASUS/Desktop/Dataset/" + course + "/" + branch + "/" + str(year)
    model_path = path + "/model/recognizer.pickle"
    label_path = path + "/model/label.pickle"
    file1 = convertToBinaryData(model_path)
    file2 = convertToBinaryData(label_path)
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    mycursor = mydb.cursor()
    mycursor.execute("Use resources")
    query = "Insert into models (course, branch, year, classifier, labels) values (%s, %s, %s ,%s ,%s)"
    mycursor.execute(query, (course, branch, year, file1, file2))
    mydb.commit()
