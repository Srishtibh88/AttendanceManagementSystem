import os
import subprocess
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import mysql.connector
import AddStudent as adds
import SetupTeacher as st
from StoreEmbeddings import Store_Embeddings
from TrainModel import Train_Model, Upload_Model
import Recognize
import UpdateDatabase

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=""
)

class App:

    def __init__(self, root):
        self.root = root
        self.initialize()

    def initialize(self):
        self.root.title("Attendance Management System")
        width, height = root.winfo_screenwidth(), root.winfo_screenheight()
        self.root.geometry('%dx%d+0+0' % (width, height))
        self.image = Image.open("C:/Users\ASUS\Desktop\miniProject/back3.jpg")
        self.image = self.image.resize((2000, 2000), Image.ANTIALIAS)
        self.background_image = ImageTk.PhotoImage(self.image)
        self.background_label = Label(self.root, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.background_label.image = self.background_image
        self.login_page()

    def authenticate(self, user, passw, mem_type):
        mem_type = mem_type.lower()
        mycursor = mydb.cursor()
        mycursor.execute("Use Resources")
        query = "Select * from users Where username= %s AND password= %s AND member= %s "
        mycursor.execute(query,(user, passw, mem_type))
        myresult = mycursor.fetchall()
        if len(myresult) > 0:
            self.login_frame.destroy()
            if mem_type == "admin":
                admin = Admin(root, user)
            else:
                if myresult[0][3] == 0:
                    st.SetupTeacher(user)
                teacher = Teacher(root, user)
        else:
            self.login_error["fg"]="Red"



    def login_page(self):
        self.login_frame = Frame(self.root, bg="Black")
        self.login_frame.pack(expand=1, ipadx=30, ipady=30, padx=50, pady=50)
        self.login_msg = Label(self.login_frame, text = "Member Login", bg="Black", fg = "White").pack(pady = 50)
        self.username_msg = Label(self.login_frame, text="Username", bg="Black", fg = "White").pack(anchor="w", padx = (30,0))
        self.username = Entry(self.login_frame, width = 70, bg = "White")
        self.username.pack(ipady=20)
        self.password_msg = Label(self.login_frame, text="Password", bg="Black", fg = "White").pack(anchor="w", padx = (30,0), pady=(40,0))
        self.password = Entry(self.login_frame, width = 70, bg = "White", show="*")
        self.password.pack(ipady = 20)
        self.clicked = StringVar()
        self.clicked.set("Teacher")
        self.drop = OptionMenu(self.login_frame, self.clicked, "Admin", "Teacher")
        self.drop.config(bg="White", width=15)
        self.drop.pack(anchor="w", padx = (30,0), pady=(50,0), ipadx = 10, ipady = 10)
        self.login_error = Label(self.login_frame, text="Incorrect Username or Password!", bg="Black", fg="Black")
        self.login_error.pack(pady=(20,0))
        self.button = Button(self.login_frame, borderwidth=0, text="Log In", width=60, bg="#006080", fg="White",
                             command = lambda:self.authenticate(self.username.get(), self.password.get(), self.clicked.get()))
        self.button.pack(pady = (50,0), ipady = 20)

class Admin:

    def __init__(self, root, username):
        self.root = root
        self.Admin_Page()
        self.Welcome(username)

    def Welcome(self, val):
        self.welcome_frame = Frame(self.root, bg="#DCDCDC")
        self.welcome_frame.pack(side="left", fill=BOTH, expand=1)
        self.welcome_msg = Label(self.welcome_frame, text="Welcome " + val + " !", font=("Times New Roman", 20), width=100, bg="#DCDCDC")
        self.welcome_msg.pack(pady=100, ipadx=20, ipady=20)

    def Admin_Page(self):
        sc_width = root.winfo_screenwidth() // 30
        self.frame0 = Frame(self.root, bg="black", borderwidth=2, relief="sunken")
        self.frame0.pack(ipadx=30, ipady=30, side=TOP, fill=BOTH)
        self.title = Label(self.frame0, text="Attendance Management System", bg="black", fg="white",
                           font=("Times New Roman", 25))
        self.title.pack(pady=(50, 0))
        self.frame1 = Frame(self.root, bg="Black")
        self.frame1.pack(side="left", fill=BOTH, ipadx=sc_width)
        self.add_student = Button(self.frame1, bg="#006080", fg="white", relief="solid", text="Add Student",
                                  width=sc_width // 2, command=self.Add_Student, font=("Times New Roman", 18))
        self.add_student.pack(pady=(60, 5), ipady=10)
        self.add_teacher = Button(self.frame1, bg="#006080", fg="white", relief="solid", text="Add Teacher",
                                  width=sc_width // 2, command=self.Add_Teacher, font=("Times New Roman", 18))
        self.add_teacher.pack(pady=(5), ipady=10)
        self.train_data = Button(self.frame1, bg="#006080", fg="white", relief="solid", text="Train Data",
                                 width=sc_width // 2, command=self.Train_Data, font=("Times New Roman", 18))
        self.train_data.pack(pady=(5), ipady=10)
        self.logout = Button(self.frame1, text="Logout", bg="black", fg="white", font=("Times New Roman", 15),
                             command=self.Logout).pack(pady=(160, 20), ipady=5)

    def Logout(self):
        list1 = self.root.winfo_children()
        for i in range(0, len(list1)):
            list1[i].destroy()

        app.initialize()

    def Switch_Option_Admin(self):
        for child in self.root.winfo_children():
            if child != self.frame0 and child != self.frame1:
                child.destroy()
        self.add_teacher["state"] = "normal"
        self.add_student["state"] = "normal"
        self.train_data["state"] = "normal"


    def Add_Student(self):

        self.Switch_Option_Admin()
        self.add_student["state"] = "disabled"

        self.student_frame = Frame(self.root, bg="#DCDCDC")
        self.student_frame.pack(side="left", fill=BOTH, expand=1)
        self.options = ["BTech", "MCA"]
        Label(self.student_frame, text="Add Student", bg="#DCDCDC", font=("Times New Roman", 20)).pack(ipady=20,pady=(10))
        Label(self.student_frame, text="Course", bg="#DCDCDC", width=50, font=("Times New Roman", 15)).pack(pady=(20, 5), anchor="w", padx=(140, 0))
        self.course_selected = StringVar()
        self.course_selected.set("Select Course")
        self.course = ttk.Combobox(self.student_frame, state="readonly", textvariable=self.course_selected,value=self.options, width=50)
        self.course.bind("<<ComboboxSelected>>", self.Load_Combo)
        self.course.pack(ipady=10)
        self.branch_selected = StringVar()
        Label(self.student_frame, text="Branch", bg="#DCDCDC", width=50, font=("Times New Roman", 15)).pack( pady=(30, 5), anchor="w", padx=(140, 0))
        self.branch_selected.set("Select Branch")
        self.branch = ttk.Combobox(self.student_frame, state="disabled", textvariable=self.branch_selected, value=[], width=50)
        self.branch.pack(ipady=10)
        self.year_selected = StringVar()
        Label(self.student_frame, text="Year", bg="#DCDCDC", width=50, font=("Times New Roman", 15)).pack(pady=(30, 5), anchor="w", padx=(130, 0))
        self.year_selected.set("Select Year")
        self.year = ttk.Combobox(self.student_frame, state="disabled", textvariable=self.year_selected, value=[],
                                 width=50)
        self.year.pack(ipady=10)
        self.next = Button(self.student_frame, text="Next", command=self.Capture_Student,
                           font=("Times New Roman", 15)).pack(pady=(60, 5), ipadx=5)

    def Load_Combo(self, event):
        self.options1 = [["Civil", "Computer Science"],["1","2","3","4"]]
        self.options2 = [["MCA"],["1","2","3"]]
        self.branch_selected.set("Select Branch")
        self.year_selected.set("Select Year")
        if self.course_selected.get() == "BTech":
            self.branch["value"]=self.options1[0]
            self.year["value"]=self.options1[1]
        else:
            self.branch["value"] = self.options2[0]
            self.year["value"] = self.options2[1]
        self.branch["state"] = "readonly"
        self.year["state"] = "readonly"


    def Capture_Student(self):
        if self.course_selected.get() == "Select Course" or self.branch_selected.get() == "Select Branch" or self.year_selected.get() == "Select Year":
            messagebox.showerror("Error", "Select all entries")
        else:
            self.student_frame.pack_forget()
            self.capture_frame = Frame(self.root, bg="#DCDCDC")
            self.capture_frame.pack(side="left", fill=BOTH, expand=1)
            self.back = Button(self.capture_frame, text="Back", command=self.Go_Back, font=("Times New Roman", 15)).pack(
                anchor="nw", ipadx=5)
            self.disp_course = Label(self.capture_frame, bg="#DCDCDC", font=("Times New Roman", 15), width=50,
                                     text="Course: " + self.course_selected.get()
                                          + ",  Branch: " + self.branch_selected.get() + ",  Year: " + self.year_selected.get()).pack(pady=(30))
            self.name_msg = Label(self.capture_frame, bg="#DCDCDC", font=("Times New Roman", 15), width=50,text="Name").pack(anchor="w", pady=(30, 5), padx=(45,0))
            self.tname = StringVar()
            self.name = Entry(self.capture_frame, font=("Times New Roman", 15), width=50, textvariable = self.tname).pack()
            self.roll_msg = Label(self.capture_frame, bg="#DCDCDC", font=("Times New Roman", 15), width=50,text="Roll No").pack(anchor="w", pady=(50, 5) ,padx=(55,0))
            self.troll = StringVar()
            self.rollno = Entry(self.capture_frame, font=("Times New Roman", 15), width=50, textvariable = self.troll).pack()
            self.capture = Button(self.capture_frame, font=("Times New Roman", 15), text="Capture & Save",
                  command=lambda:self.Save_Student_Data(self.course_selected.get(),self.branch_selected.get(),self.year_selected.get(),self.tname.get(),self.troll.get()))
            self.capture.pack(pady=(100, 0))

    def Go_Back(self):
        self.capture_frame.destroy()
        self.student_frame.pack(side="left", fill=BOTH, expand=1)

    def Save_Student_Data(self, course, branch, year, name, roll):
        if name == "" or roll == "":
            messagebox.showerror("Error", "Provide input for all entries")
        else:
            mycursor = mydb.cursor()
            course = course.lower()
            branch = branch.lower()
            branch = branch.replace(" ","")
            roll = str(roll)
            year = str(year)
            query = "Use "+course
            mycursor.execute(query)
            self.table = branch + year
            self.table = self.table.replace(" ","")
            query = "Insert into "+ self.table + " (rollno, name) values (%s, %s)"
            mycursor.execute(query, (roll, name))
            mydb.commit()
            self.troll.set("")
            self.tname.set("")
            self.datalist = (course, branch, year, roll)
            adds.store_capture(self.datalist)
            messagebox.showinfo("Confirmation", "Student data recorded successfully")

    def Add_Teacher(self):

        self.Switch_Option_Admin()
        self.add_teacher["state"] = "disabled"

        self.teacher_frame = Frame(self.root,  bg="#DCDCDC")
        self.teacher_frame.pack(side="left", fill=BOTH, expand=1)
        Label(self.teacher_frame, text="Add Teacher", bg="#DCDCDC", font=("Times New Roman", 20)).pack(ipady=20, pady=(10))
        Label(self.teacher_frame, text="Username", bg="#DCDCDC", font=("Times New Roman", 15), width=50).pack(pady=(30, 5), anchor="w", padx=(60,0))
        self.tname = StringVar()
        self.teacher_name = Entry(self.teacher_frame, textvariable=self.tname, font=("Times New Roman", 15), width=50)
        self.teacher_name.pack()
        Label(self.teacher_frame, text="Password", bg="#DCDCDC", font=("Times New Roman", 15), width=50).pack(pady=(30,5), anchor="w", padx=(60,0))
        self.tpass = StringVar()
        self.teacher_password = Entry(self.teacher_frame, textvariable=self.tpass, show="*", font=("Times New Roman", 15), width=50)
        self.teacher_password.pack()
        Label(self.teacher_frame, text="Confirm Password", bg="#DCDCDC", font=("Times New Roman", 15), width=50).pack(pady=(30, 5), anchor="w", padx=(95, 0))
        self.tcpass = StringVar()
        self.confirm_password = Entry(self.teacher_frame, show="*", textvariable=self.tcpass, font=("Times New Roman", 15), width=50)
        self.confirm_password.pack()
        self.error_msg = Label(self.teacher_frame, text="Password Mismatched!", fg="#DCDCDC", bg="#DCDCDC")
        self.error_msg.pack()
        self.register_btn = Button(self.teacher_frame, text="Register", font=("Times New Roman", 15),
                                   command=lambda:self.Register_Teacher(self.tname.get(),self.tpass.get(), self.tcpass.get()))
        self.register_btn.pack(pady=(80,5), ipadx=5)

    def Register_Teacher(self, name, passw, cpassw):
        if name == "" or passw == "" or cpassw == "":
            messagebox.showerror("Error","Provide input for all entries")
        elif passw == cpassw:
            mycursor = mydb.cursor()
            mycursor.execute("Use Resources")
            query = "Insert into users (username, password, member, flag) values (%s, %s, %s, 0)"
            mycursor.execute(query, (name, passw, "teacher"))
            mydb.commit()
            self.error_msg["fg"] = "#DCDCDC"
            messagebox.showinfo("Confirmation", "Registration Successful")
            self.tname.set("")
            self.tpass.set("")
            self.tcpass.set("")
        else:
            self.error_msg["fg"] = "Red"

    def Train_Data(self):

        self.Switch_Option_Admin()
        self.train_data["state"] = "disabled"

        self.student_frame = Frame(self.root, bg="#DCDCDC")
        self.student_frame.pack(side="left", fill=BOTH, expand=1)
        self.options = ["BTech", "MCA"]
        Label(self.student_frame, text="Train Data", bg="#DCDCDC", font=("Times New Roman", 20)).pack(ipady=20, pady=(10))
        Label(self.student_frame, text="Course", bg="#DCDCDC", width=50, font=("Times New Roman", 15)).pack(pady=(15, 5), anchor="w", padx=(140, 0))
        self.course_selected = StringVar()
        self.course_selected.set("Select Course")
        self.course = ttk.Combobox(self.student_frame, state="readonly", textvariable=self.course_selected, value=self.options, width=50)
        self.course.bind("<<ComboboxSelected>>", self.Load_Combo)
        self.course.pack(ipady=10)
        self.branch_selected = StringVar()
        Label(self.student_frame, text="Branch", bg="#DCDCDC", width=50, font=("Times New Roman", 15)).pack(pady=(30, 5), anchor="w", padx=(140, 0))
        self.branch_selected.set("Select Branch")
        self.branch = ttk.Combobox(self.student_frame, state="disabled", textvariable=self.branch_selected, value=[], width=50)
        self.branch.pack(ipady=10)
        self.year_selected = StringVar()
        Label(self.student_frame, text="Year", bg="#DCDCDC", width=50, font=("Times New Roman", 15)).pack(pady=(30, 5), anchor="w", padx=(130, 0))
        self.year_selected.set("Select Year")
        self.year = ttk.Combobox(self.student_frame, state="disabled", textvariable=self.year_selected, value=[],width=50)
        self.year.pack(ipady=10)
        self.next = Button(self.student_frame, text="Train Classifier", font=("Times New Roman", 15),
                           command = lambda:self.verify(self.course_selected.get(), self.branch_selected.get(), self.year_selected.get()))
        self.next.pack(pady=(80, 5),ipadx=5)

    def verify(self, course, branch, year):
        if course == "Select Course" or branch == "Select Branch" or year == "Select Year":
            messagebox.showerror("Error", "Select all entries")
        else:
            course = course.lower()
            branch = branch.lower()
            year = str(year)
            self.next["state"] = "disabled"
            Store_Embeddings(course, branch, year)
            Train_Model(course, branch, year)
            Upload_Model(course, branch, year)
            messagebox.showinfo("Confirmation", "Model trained & uploaded succesfully")
            self.next["state"] = "normal"

class Teacher:

    def __init__(self, root, username):
        self.root = root
        self.Teacher_Page()
        self.Welcome(username)

    def Welcome(self, val):
        self.welcome_frame = Frame(self.root, bg="#DCDCDC")
        self.welcome_frame.pack(side="left", fill=BOTH, expand=1)
        self.welcome_msg = Label(self.welcome_frame, text="Welcome " + val + " !", font=("Times New Roman", 20), width=100, bg="#DCDCDC")
        self.welcome_msg.pack(pady=100, ipadx=20, ipady=20)

    def Teacher_Page(self):
        sc_width = root.winfo_screenwidth() // 30
        self.frame0 = Frame(self.root, bg="black", borderwidth=2, relief="sunken")
        self.frame0.pack(ipadx=30, ipady=30, side=TOP, fill=BOTH)
        self.title = Label(self.frame0, text="Attendance Management System", bg="black", fg="white", font=("Times New Roman", 25))
        self.title.pack(pady=(50, 0))
        self.frame1 = Frame(self.root, bg="Black")
        self.frame1.pack(side="left", fill=BOTH, ipadx=sc_width)
        self.mark_attendance = Button(self.frame1, bg="#006080", fg="white", relief="solid", width=sc_width // 2, text="Mark Attendance", font=("Times New Roman", 18), command=self.Mark_Attendance)
        self.mark_attendance.pack(pady=(60, 5), ipady=10)
        self.view_attendance = Button(self.frame1, bg="#006080", fg="white", relief="solid", width=sc_width // 2, text="View/Edit Attendance", font=("Times New Roman", 18), command=self.View_Attendance)
        self.view_attendance.pack(pady=(5), ipady=10)
        self.upload_attendance = Button(self.frame1, bg="#006080", fg="white", relief="solid", width=sc_width // 2, text="Upload Attendance", font=("Times New Roman", 18), command=self.Upload_Attendance)
        self.upload_attendance.pack(pady=(5), ipady=10)
        self.logout = Button(self.frame1, text="Logout", bg="black", fg="white", font=("Times New Roman", 15), command=self.Logout).pack(pady=(160, 20), ipady=5)

    def Logout(self):
        list1 = self.root.winfo_children()
        for i in range(0, len(list1)):
            list1[i].destroy()

        app.initialize()

    def Switch_Option_Teacher(self):
        for child in self.root.winfo_children():
            if child != self.frame0 and child != self.frame1:
                child.destroy()
        self.mark_attendance["state"] = "normal"
        self.view_attendance["state"] = "normal"
        self.upload_attendance["state"] = "normal"

    def Mark_Attendance(self):
        self.Switch_Option_Teacher()
        self.mark_attendance["state"] = "disabled"

        self.student_frame = Frame(self.root, bg="#DCDCDC")
        self.student_frame.pack(side="left", fill=BOTH, expand=1)
        self.options = ["BTech", "MCA"]
        Label(self.student_frame, text="Mark Attendance", bg="#DCDCDC", font=("Times New Roman", 20)).pack(ipady=20,pady=(10))
        Label(self.student_frame, text="Course", bg="#DCDCDC", width=50, font=("Times New Roman", 15)).pack(pady=(20, 5), anchor="w", padx=(140, 0))
        self.course_selected = StringVar()
        self.course_selected.set("Select Course")
        self.course = ttk.Combobox(self.student_frame, state="readonly", textvariable=self.course_selected,value=self.options, width=50)
        self.course.bind("<<ComboboxSelected>>", self.Load_Combo)
        self.course.pack(ipady=10)
        self.branch_selected = StringVar()
        Label(self.student_frame, text="Branch", bg="#DCDCDC", width=50, font=("Times New Roman", 15)).pack( pady=(30, 5), anchor="w", padx=(140, 0))
        self.branch_selected.set("Select Branch")
        self.branch = ttk.Combobox(self.student_frame, state="disabled", textvariable=self.branch_selected, value=[], width=50)
        self.branch.pack(ipady=10)
        self.year_selected = StringVar()
        Label(self.student_frame, text="Year", bg="#DCDCDC", width=50, font=("Times New Roman", 15)).pack(pady=(30, 5), anchor="w", padx=(130, 0))
        self.year_selected.set("Select Year")
        self.year = ttk.Combobox(self.student_frame, state="disabled", textvariable=self.year_selected, value=[], width=50)
        self.year.pack(ipady=10)
        self.next = Button(self.student_frame, text="Next",
                           command = lambda:self.Mark_Sheet(self.course_selected.get(), self.branch_selected.get(),self.year_selected.get()),font=("Times New Roman", 15))
        self.next.pack(pady=(60, 5), ipadx=5)

    def Load_Combo(self, event):
        self.options1 = [["Civil", "Computer Science"], ["1", "2", "3", "4"]]
        self.options2 = [["MCA"], ["1", "2", "3"]]
        self.branch_selected.set("Select Branch")
        self.year_selected.set("Select Year")
        if self.course_selected.get() == "BTech":
            self.branch["value"] = self.options1[0]
            self.year["value"] = self.options1[1]
        else:
            self.branch["value"] = self.options2[0]
            self.year["value"] = self.options2[1]
        self.branch["state"] = "readonly"
        self.year["state"] = "readonly"

    def Mark_Sheet(self, course, branch, year):
        if course == "Select Course" or branch == "Select Branch" or year == "Select Year":
            messagebox.showerror("Error", "Select all entries")
        else:
            self.options = []
            self.options = self.find_subject(course, branch, year)
            self.student_frame.pack_forget()
            self.mark_frame = Frame(self.root,  bg="#DCDCDC")
            self.mark_frame.pack(side="left", fill=BOTH, expand=1)
            self.back = Button(self.mark_frame, text="Back", command=lambda:self.Go_Back(1), font=("Times New Roman", 15)).pack(anchor="nw", ipadx=5)
            self.subject_selected = StringVar()
            self.disp_course = Label(self.mark_frame, bg="#DCDCDC", font=("Times New Roman", 15), width=50, text="Course: " + self.course_selected.get()
                                          + ",  Branch: " + self.branch_selected.get() + ",  Year: " + self.year_selected.get()).pack(pady=(30))
            Label(self.mark_frame, text="Subject", bg="#DCDCDC", width=50, font=("Times New Roman", 15)).pack( pady=(30, 5), anchor="w", padx=(140, 0))
            self.subject_selected.set("Select Subject")
            self.subject = ttk.Combobox(self.mark_frame, state="readonly", textvariable=self.subject_selected, value=self.options, width=50)
            self.subject.pack(ipady=10)
            self.select_image = Button(self.mark_frame, text="Select Images", width=28, command=self.Image_Picker, font=("Times New Roman", 15)).pack(pady=(50,0))
            self.image_count = Label(self.mark_frame, bg="#DCDCDC", pady=20)
            self.image_count.pack()
            self.test_images = []
            self.recognize = Button(self.mark_frame, text="Recognize & Mark Attendance", font=("Times New Roman", 15),
                command=lambda:self.call_recognize(course, branch, year, self.subject_selected.get(), self.test_images))
            self.recognize.pack(pady=(60, 5), ipadx=5)

    def call_recognize(self, course, branch, year, subject, test_images):
        if subject == "Select Subject" or len(test_images) == 0:
            messagebox.showerror("Error", "Select all entries")
        else:
            course = course.lower()
            branch = branch.lower()
            year = str(year)
            self.path = self.path = "C:/Users/ASUS/Desktop/Resources/" + course +"/" + branch + "/" + year +"/" + subject + ".xlsx"
            if not os.path.exists(self.path):
                messagebox.showerror("File not found", "Please verify your entries")
            else:
                self.recognize["state"] = "disabled"
                self.count = Recognize.recognize(course, branch, year, subject, test_images)
                messagebox.showinfo("Confirmation", "Attendance marked successfully \n"+str(self.count) +" student(s) present")
                self.recognize["state"] = "normal"


    def find_subject(self, course, branch, year):
        mycursor = mydb.cursor()
        course = course.lower()
        branch = branch.lower()
        query = "Use "+course
        mycursor.execute(query)
        query = "Select subject_code, name from subjects Where branch = %s AND year = %s "
        mycursor.execute(query, (branch, str(year)))
        myresult = mycursor.fetchall()
        subject_list = []
        for row in myresult:
            subject_list.append(row[1]+" "+row[0])
        return subject_list


    def Go_Back(self, val):
        if val==1:
            self.mark_frame.destroy()
        elif val==2:
                self.view_frame.destroy()
        elif val==3:
            self.upload_frame.destroy()
        self.student_frame.pack(side="left", fill=BOTH, expand=1)

    def Image_Picker(self):
        self.test_images = filedialog.askopenfilenames(initialdir="C:/Users/ASUS/Desktop/", title="Select file", filetypes=(("jpg files", "*.jpg*"), ("jpeg files", "*.jpeg")))
        if len(self.test_images) > 0:
            self.image_count["text"] = str(len(self.test_images))+" file(s) selected"

    def View_Attendance(self):
        self.Switch_Option_Teacher()
        self.view_attendance["state"] = "disabled"

        self.student_frame = Frame(self.root, bg="#DCDCDC")
        self.student_frame.pack(side="left", fill=BOTH, expand=1)
        self.options = ["BTech", "MCA"]
        Label(self.student_frame, text="View/Edit Attendance", bg="#DCDCDC", font=("Times New Roman", 20)).pack(ipady=20, pady=(10))
        Label(self.student_frame, text="Course", bg="#DCDCDC", width=50, font=("Times New Roman", 15)).pack(pady=(20, 5), anchor="w", padx=(140, 0))
        self.course_selected = StringVar()
        self.course_selected.set("Select Course")
        self.course = ttk.Combobox(self.student_frame, state="readonly", textvariable=self.course_selected,value=self.options, width=50)
        self.course.bind("<<ComboboxSelected>>", self.Load_Combo)
        self.course.pack(ipady=10)
        self.branch_selected = StringVar()
        Label(self.student_frame, text="Branch", bg="#DCDCDC", width=50, font=("Times New Roman", 15)).pack(pady=(30, 5), anchor="w", padx=(140, 0))
        self.branch_selected.set("Select Branch")
        self.branch = ttk.Combobox(self.student_frame, state="disabled", textvariable=self.branch_selected, value=[],width=50)
        self.branch.pack(ipady=10)
        self.year_selected = StringVar()
        Label(self.student_frame, text="Year", bg="#DCDCDC", width=50, font=("Times New Roman", 15)).pack(pady=(30, 5),anchor="w",padx=(130, 0))
        self.year_selected.set("Select Year")
        self.year = ttk.Combobox(self.student_frame, state="disabled", textvariable=self.year_selected, value=[], width=50)
        self.year.pack(ipady=10)
        self.next = Button(self.student_frame, text="Next",
                           command=lambda: self.View_Sheet(self.course_selected.get(), self.branch_selected.get(),self.year_selected.get()), font=("Times New Roman", 15))
        self.next.pack(pady=(60, 5), ipadx=5)

    def View_Sheet(self, course, branch, year):
        if course == "Select Course" or branch == "Select Branch" or year == "Select Year":
            messagebox.showerror("Error", "Select all entries")
        else:
            self.options = []
            self.options = self.find_subject(course, branch, year)
            self.student_frame.pack_forget()
            self.view_frame = Frame(self.root, bg="#DCDCDC")
            self.view_frame.pack(side="left", fill=BOTH, expand=1)
            self.back = Button(self.view_frame, text="Back", command=lambda:self.Go_Back(2), font=("Times New Roman", 15)).pack(anchor="nw", ipadx=5)
            self.disp_course = Label(self.view_frame, bg="#DCDCDC", font=("Times New Roman", 15), width=50,text="Course: " + self.course_selected.get()
                                          + ",  Branch: " + self.branch_selected.get() + ",  Year: " + self.year_selected.get()).pack(pady=(30))
            self.subject_selected = StringVar()
            Label(self.view_frame, text="Subject", bg="#DCDCDC", width=50, font=("Times New Roman", 15)).pack(pady=(30, 5),anchor="w", padx=(140, 0))
            self.subject_selected.set("Select Subject")
            self.subject = ttk.Combobox(self.view_frame, state="readonly", textvariable=self.subject_selected,
                                        value=self.options, width=50)
            self.subject.pack(ipady=10)
            self.view = Button(self.view_frame, text="View Attendance Sheet",
                               command=lambda:self.Show_Sheet(course, branch, year, self.subject_selected.get()), font=("Times New Roman", 15))
            self.view.pack(pady=(60, 5), ipadx=5)

    def Show_Sheet(self, course, branch, year, subject):
        if subject == "Select Subject":
            messagebox.showerror("Error", "Select all entries")
        else:
            course = course.lower()
            branch = branch.lower()
            year = str(year)
            self.path = self.path = "C:/Users/ASUS/Desktop/Resources/" + course + "/" + branch + "/" + year + "/" + subject + ".xlsx"
            if not os.path.exists(self.path):
                messagebox.showerror("File not found", "Please verify your entries")
            else:
                self.path = "C:/Users/ASUS/Desktop/Resources/" + course +"/" + branch + "/" + year +"/" + subject + ".xlsx"
                subprocess.Popen([self.path], shell=True)

    def Upload_Attendance(self):

        self.Switch_Option_Teacher()
        self.upload_attendance["state"] = "disabled"

        self.student_frame = Frame(self.root, bg="#DCDCDC")
        self.student_frame.pack(side="left", fill=BOTH, expand=1)
        self.options = ["BTech", "MCA"]
        Label(self.student_frame, text="Upload Attendance", bg="#DCDCDC", font=("Times New Roman", 20)).pack(ipady=20, pady=(10))
        Label(self.student_frame, text="Course", bg="#DCDCDC", width=50, font=("Times New Roman", 15)).pack(pady=(20, 5), anchor="w", padx=(140, 0))
        self.course_selected = StringVar()
        self.course_selected.set("Select Course")
        self.course = ttk.Combobox(self.student_frame, state="readonly", textvariable=self.course_selected, value=self.options, width=50)
        self.course.bind("<<ComboboxSelected>>", self.Load_Combo)
        self.course.pack(ipady=10)
        self.branch_selected = StringVar()
        Label(self.student_frame, text="Branch", bg="#DCDCDC", width=50, font=("Times New Roman", 15)).pack(
            pady=(30, 5), anchor="w", padx=(140, 0))
        self.branch_selected.set("Select Branch")
        self.branch = ttk.Combobox(self.student_frame, state="disabled", textvariable=self.branch_selected, value=[],
                                   width=50)
        self.branch.pack(ipady=10)
        self.year_selected = StringVar()
        Label(self.student_frame, text="Year", bg="#DCDCDC", width=50, font=("Times New Roman", 15)).pack(pady=(30, 5),anchor="w", padx=(130, 0))
        self.year_selected.set("Select Year")
        self.year = ttk.Combobox(self.student_frame, state="disabled", textvariable=self.year_selected, value=[],width=50)
        self.year.pack(ipady=10)
        self.next = Button(self.student_frame, text="Next",
                           command=lambda: self.Upload_Sheet(self.course_selected.get(), self.branch_selected.get(),self.year_selected.get()), font=("Times New Roman", 15))
        self.next.pack(pady=(60, 5), ipadx=5)

    def Upload_Sheet(self, course, branch, year):
        if course == "Select Course" or branch == "Select Branch" or year == "Select Year":
            messagebox.showerror("Error", "Select all entries")
        else:
            self.options = []
            self.options = self.find_subject(course, branch, year)
            self.student_frame.pack_forget()
            self.upload_frame = Frame(self.root, bg="#DCDCDC")
            self.upload_frame.pack(side="left", fill=BOTH, expand=1)
            self.back = Button(self.upload_frame, text="Back", command=lambda:self.Go_Back(3), font=("Times New Roman", 15)).pack(anchor="nw", ipadx=5)
            self.disp_course = Label(self.upload_frame, bg="#DCDCDC", font=("Times New Roman", 15), width=50,text="Course: " + self.course_selected.get()
                                          + ",  Branch: " + self.branch_selected.get() + ",  Year: " + self.year_selected.get()).pack(pady=(30))
            self.subject_selected = StringVar()
            Label(self.upload_frame, text="Subject", bg="#DCDCDC", width=50, font=("Times New Roman", 15)).pack(pady=(30, 5),anchor="w", padx=(140, 0))
            self.subject_selected.set("Select Subject")
            self.subject = ttk.Combobox(self.upload_frame, state="readonly", textvariable=self.subject_selected,
                                        value=self.options, width=50)
            self.subject.pack(ipady=10)
            self.upload = Button(self.upload_frame, text="Upload Attendance", font=("Times New Roman", 15),
                                 command=lambda:self.Update_Database(course, branch, year, self.subject_selected.get()))
            self.upload.pack(pady=(60, 5), ipadx=5)

    def Update_Database(self, course, branch, year, subject):
        if subject == "Select Subject":
            messagebox.showerror("Error", "Select all entries")
        else:
            course = course.lower()
            branch = branch.lower()
            year = str(year)
            self.path = self.path = "C:/Users/ASUS/Desktop/Resources/" + course + "/" + branch + "/" + year + "/" + subject + ".xlsx"
            if not os.path.exists(self.path):
                messagebox.showerror("File not found", "Please verify your entries")
            else:
                self.upload["state"] = "disabled"
                UpdateDatabase.upload_attendance(course, branch, year, subject)
                messagebox.showinfo("Confirmation", "Attendance uploaded successfully")
                self.upload["state"] = "normal"


root = Tk()
app = App(root)
root.mainloop()