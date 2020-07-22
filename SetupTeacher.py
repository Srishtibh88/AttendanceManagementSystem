import os
from distutils.file_util import write_file

import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    use_pure=True
)

path = "C:/Users/ASUS/Desktop/Resources"
courses = ["btech", "mca"]

def SetupTeacher(username):
    mycursor = mydb.cursor()

    list= []
    for course in courses:
        mycursor.execute("Use "+course)
        query = "Select * from subjects where teacher = %s "
        mycursor.execute(query, (username, ))
        result = mycursor.fetchall()

        if len(result) > 0:
            if not os.path.isdir(path + "/" + course):
                os.mkdir(path + "/" + course)
        for (code, name, year, branch, teacher) in result:
            branch = branch.lower()
            year = str(year)
            if not os.path.isdir(path + "/" + course+"/"+branch):
                os.mkdir(path + "/" + course+"/"+branch)
            if not os.path.isdir(path + "/" + course+"/"+branch+"/"+year):
                os.mkdir(path + "/" + course+"/"+branch+"/"+year)

            temp_path = path + "/" + course+"/"+branch+"/"+year
            open(temp_path+"/"+name+" "+code+".xlsx",'a').close()
            list.append((course, branch, year))

    mycursor.execute("Use resources")
    query = "Update users Set flag=1 where username = %s"
    mycursor.execute(query, (username,))
    mydb.commit()

    for (course, branch, year) in list:
        branch = branch.lower()
        temp_path = path + "/" + course + "/" + branch + "/" + year
        if not os.path.isfile(temp_path+"/recognizer.pickle"):
            query = "Select classifier, labels from models where course= %s AND branch= %s AND year= %s"
            mycursor.execute(query, (course, branch, year))
            result = mycursor.fetchall()
            file1 = result[0][0]
            file2 = result[0][1]
            newfile = open(temp_path+"/recognizer.pickle", 'wb')
            newfile.write(file1)
            newfile = open(temp_path + "/labels.pickle", 'wb')
            newfile.write(file2)
            #write_file(file1, temp_path+"/recognizer.pickle")
            #write_file(file2, temp_path + "/labels.pickle")






