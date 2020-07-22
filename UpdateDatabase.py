import openpyxl
from datetime import datetime
import pandas as pd
from openpyxl import load_workbook
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)

def upload_attendance(course, branch, year, subject):
    course = course.lower()
    branch = branch.lower()
    year = str(year)
    currentDate = datetime.now()
    month = currentDate.strftime("%B")
    path = path = "C:/Users/ASUS/Desktop/Resources/" + course + "/" + branch + "/" + year + "/" + subject + ".xlsx"
    df = pd.read_excel(path, sheet_name=month)
    total = df.iloc[:, -1]
    rollno =df.iloc [:, 0]
    subject_code = subject.split()[-1]
    subject_code = subject_code.replace("-","")
    mycursor = mydb.cursor()
    mycursor.execute("Use " + course)

    for i in range(0, len(total)):
        query = "Update "+branch +  year+" set "+ str(subject_code) + "= " + str(total[i]) + " where rollno = " + str(rollno[i])
        mycursor.execute(query)

    mydb.commit()