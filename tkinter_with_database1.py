from fileinput import close
from tkinter import RAISED
from math import *
from tkinter import *

from tkinter import filedialog
from matplotlib.figure import Figure
import pandas as pd

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import tkinter as tk                # python 3
from tkinter import font as tkfont  # python 3

import mysql.connector
# Connects to database
mydb = mysql.connector.connect(host='localhost', password='hitchcardio12', user='root', database='hitchcardio')
mycursor = mydb.cursor()

# VARIABLE NAMES OF EACH COLUMN IN ORDER
# name, id, resting_HR, max_HR, VO2_max, isMale, day
# When isMale = 1, user is male. When isMale = 0, user is female.

# Prints current database
mycursor.execute("SELECT * FROM users")
for x in mycursor:
    print(x)

def close():
    app.destroy()


class Vo2Max(tk.Tk):

    def __init__(self, *args, **kwargs):

        
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.title("Hitch Cardio")
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, weeklyavg, monthavg1, yearavg1,VO2Calc, Signup, coachadddata):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()



class VO2Calc(tk.Frame):
    

            
        
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        left_frame = tk.Frame(self, width=200, height=400, bg='grey')
        left_frame.grid(row=0, column=0, padx=10, pady=5)
        
        right_frame = tk.Frame(self, width=650, height=400, bg='grey')
        right_frame.grid(row=0, column=1, padx=10, pady=5)
        
        def clear_text():
            maxhr.delete(0, tk.END)
            resthr.delete(0, tk.END)

        def calc():
            mycursor.execute("SELECT * FROM users WHERE name = 'Joe Shmoe'")
            countTry = 0
            for x in mycursor:
                countTry= countTry+1
            print(str(countTry) + "  IS COUNT TRY")
            if(countTry==0): # create new user
                print("this ran")
                name="Joe Shmoe"
                #mx = int(maxhr.get())
                #rest = int(resthr.get())
                #vo2max = round(float (mx / rest)*15.3,2)
                mx = 169
                rest = 69
                vo2max = 17.0
                dayJoe=0
                #mycursor.execute("INSERT INTO users (name, resting_HR, max_HR, VO2_max, day) VALUES (%s, %s, %s, %s, %s)",(name,rest,mx,vo2max,dayJoe))
                mycursor.execute("INSERT INTO users (name, resting_HR, max_HR, VO2_max, day) VALUES (%s, %s, %s, %s, %s)",(name,rest,mx,vo2max,dayJoe))
                """
            else: # there is atleast one user name "Joe Shmoe"
                dayJoeTuple= mycursor.execute("SELECT day FROM users WHERE name = 'Joe Shmoe'")
                dayJoe = -1
                for x in mycursor: # grabs highest value of day where name = "Joe Shmoe"
                    dayJoeMax = x[len(x)-1]
                    if(dayJoeMax > dayJoe):
                        dayJoe = dayJoeMax
                """
            mycursor.execute("INSERT INTO users (name, resting_HR, max_HR, VO2_max) VALUES (%s, %s, %s, %s, %s)",(name,rest,mx,vo2max,dayJoe))
            mydb.commit()
            math = tk.Label(right_frame, text = vo2max).grid(row = 5, column = 1, padx = 5, pady = 5)
            

        tk.Label(left_frame, text="Are you in good shape?").grid(row=0, column=0, padx=5, pady=5)
        
        tk.Label(right_frame,text = "Enter your max heart rate: ").grid(row=0, column = 1, padx = 5, pady = 5)
        maxhr = tk.Entry(right_frame)
        maxhr.grid(row = 1, column = 1)
        
        tk.Label(right_frame,text = "Age: ").grid(row=0, column = 1, padx = 5, pady = 5)
        maxhr = tk.Entry(right_frame)
        maxhr.grid(row = 1, column = 1)

        tk.Label(right_frame,text = "Enter your max heart rate: ").grid(row=0, column = 1, padx = 5, pady = 5)
        maxhr = tk.Entry(right_frame)
        maxhr.grid(row = 1, column = 1)
        tk.Label(right_frame,text = "Enter your resting heart rate: ").grid(row=2, column = 1, padx = 5, pady = 5)
        resthr = tk.Entry(right_frame)
        resthr.grid(row = 3, column = 1)
        calculate = tk.Button(right_frame, text = "Calculate",command = calc).grid(row = 4,column = 1,padx = 5,pady = 5)
        addmore = tk.Button(right_frame, text="Add more", command=clear_text).grid(row = 6, column =1, padx = 5, pady = 5)
        



        tool_bar = tk.Frame(left_frame, width=180, height=185)
        tool_bar.grid(row=2, column=0, padx=5, pady=5)
        
        tk.Label(tool_bar, text="Tools", font=('Arial', 9, 'bold', 'underline'),relief=RAISED).grid(row=0, column=0, padx=5, pady=3, ipadx=10)
        backbutton = tk.Button(tool_bar, text = "Back",command=lambda: controller.show_frame("PageOne")).grid(row = 2,column = 0,padx = 5,pady = 5)

class StartPage(tk.Frame):


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Hitch Cardio", font=controller.title_font)
        label.pack(side="top", fill="x", pady=50)


        id = tk.Label(self, text = "Enter ID", font = ('bold', 15))
        id.place(x=380, y= 100)

        enterid = tk.Entry(self, width=20)
        enterid.place(x=350, y= 220)
        enterid.pack(pady= 5)
        
        signup = tk.Button(self, text = "Signup", command = lambda: controller.show_frame("Signup"))
        signup.place(rely=1.0, relx=1.0, x=0, y=0, anchor="se")

        def leadpage1():
            controller.show_frame("PageOne")

        #another def to get information about the user

        button1 = tk.Button(self, text="Click to see your Vo2 max",
                            command=lambda: [leadpage1(), ], height=5, width = 30)
                            ## need to add another def of user info into the array

        button1.place(x=300, y=240)
        button1.pack(padx=10)

class Signup(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        # Create left and right frames
        frame1 = tk.Frame(self, width=850, height=400, bg='grey')
        frame1.grid(row = 0, column=0, padx=10, pady=5)


        
        # Create tool bar frame
        info = tk.Frame(frame1, width=850, height=400)
        info.grid(row=0, column=0, padx=5, pady=5)

        # Example labels that serve as placeholders for other widgets
        tk.Label(info, text="Information", font=('Arial', 9, 'bold', 'underline'),relief=RAISED).grid(row = 0, columnspan=2, padx=5, pady=3, ipadx=10)  # ipadx is padding inside the Label widget
        ID =tk.Label(info, text="ID").grid(row=1, column=0, padx=5, pady=5)
        EnterID = tk.Entry(info).grid(row = 1, column = 1, padx= 5, pady=5)

        Age = tk.Label(info, text="Age").grid(row=2, column=0, padx=5, pady=5)
        EnterAge = tk.Entry(info).grid(row = 2, column = 1, padx= 5, pady=5)

        Gender = tk.Label(info, text="Gender").grid(row=3, column=0, padx=5, pady=5)
        EnterGender = tk.Entry(info).grid(row = 3, column = 1, padx= 5, pady=5)

        #need to store data in MySQL
        tk.Button(info, text="Click to finish and log in", command= lambda: controller.show_frame("StartPage")).grid(row = 4, columnspan =2, padx = 5, pady=5)

class PageOne(tk.Frame):
    
        
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Create left and right frames
        left_frame = tk.Frame(self, width=200, height=400, bg='grey')
        left_frame.grid(row=0, column=0, padx=10, pady=5)

        right_frame = tk.Frame(self, width=650, height=400, bg='grey')
        right_frame.grid(row=0, column=1, padx=10, pady=5)

        


        # Create frames and labels in left_frame
        tk.Label(left_frame, text="Are you in good shape?").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(left_frame).grid(row=1, column=0, padx=50, pady=50)



        # Create tool bar frame
        tool_bar = tk.Frame(left_frame, width=180, height=185)
        tool_bar.grid(row=2, column=0, padx=5, pady=5)

        # Example labels that serve as placeholders for other widgets
        tk.Label(tool_bar, text="Tools", font=('Arial', 9, 'bold', 'underline'),relief=RAISED).grid(row=0, column=0, padx=5, pady=3, ipadx=10)  # ipadx is padding inside the Label widget
        weekavg =tk.Button(tool_bar, text="Weekly Average", command=lambda: controller.show_frame("weeklyavg")).grid(row=1, column=0, padx=5, pady=5)
        monthavg = tk.Button(tool_bar, text="Monthly Average", command=lambda: controller.show_frame("monthavg1")).grid(row=2, column=0, padx=5, pady=5)
        yearavg = tk.Button(tool_bar, text="Yearly Average", command=lambda: controller.show_frame("yearavg1")).grid(row=3, column=0, padx=5, pady=5)
        addmore=tk.Button(tool_bar, text="Add More Data", command=lambda: controller.show_frame("VO2Calc")).grid(row=4, column=0, padx=5, pady=5)
        coach = tk.Button(tool_bar, text = "Coach Mode", command = lambda: controller.show_frame("coachadddata")).grid(row = 5, column = 0, padx = 5, pady =5)        
        exitapp =tk. Button(tool_bar, text="Exit", command = close).grid(row=6, column=0, padx=5, pady=5)

class weeklyavg(tk.Frame):
    
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

                # Create left and right frames
        left_frame = tk.Frame(self, width=200, height=400, bg='grey')
        left_frame.grid(row=0, column=0, padx=10, pady=5)

        right_frame = tk.Frame(self, width=650, height=400, bg='grey')
        right_frame.grid(row=0, column=1, padx=10, pady=5)

        ##need to get gender and age from database
        # gender =
        # age = 

        # Create a figure of specific size
        figure = Figure(figsize=(5, 5), dpi=100)

        # Define the points for plotting the figure
        plot = figure.add_subplot(1, 1, 1)

        # Define Data points for x and y axis
        x = [1, 2, 3, 4, 5, 6, 7]
        y = [0, 1, 2, 3, 4, 5 ,6 ] #Vo2Max
        plot.plot(x, y, color="red", marker="x", linestyle="solid")
        plot.set_xlabel('Day')
        plot.set_ylabel('Vo2Max')
        figure.tight_layout()

        # Add a canvas widget to associate the figure with canvas
        canvas = FigureCanvasTkAgg(figure, right_frame)
        canvas.get_tk_widget().grid(row=0, column=0)


        # Create frames and labels in left_frame
        tk.Label(left_frame, text="Are you in good shape?").grid(row=0, column=0, padx=5, pady=5)
        

        tk.Label(left_frame).grid(row=1, column=0, padx=50, pady=50)



        # Create tool bar frame
        tool_bar = tk.Frame(left_frame, width=180, height=185)
        tool_bar.grid(row=2, column=0, padx=5, pady=5)

        # Example labels that serve as placeholders for other widgets
        tk.Label(tool_bar, text="Tools", font=('Arial', 9, 'bold', 'underline'),relief=RAISED).grid(row=0, column=0, padx=5, pady=3, ipadx=10)  # ipadx is padding inside the Label widget
        monthavg = tk.Button(tool_bar, text="Monthly Average", command=lambda: controller.show_frame("monthavg1")).grid(row=2, column=0, padx=5, pady=5)
        yearavg = tk.Button(tool_bar, text="Yearly Average", command=lambda: controller.show_frame("yearavg1")).grid(row=3, column=0, padx=5, pady=5)
        addmore=tk.Button(tool_bar, text="Add More Data", command=lambda: controller.show_frame("VO2Calc")).grid(row=4, column=0, padx=5, pady=5)
        coach = tk.Button(tool_bar, text = "Coach Mode", command = lambda: controller.show_frame("coachadddata")).grid(row = 6, column = 0, padx = 5, pady =5)        
        exitapp =tk. Button(tool_bar, text="Exit", command=close).grid(row=5, column=0, padx=5, pady=5)

class monthavg1(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

                # Create left and right frames
        left_frame = tk.Frame(self, width=200, height=400, bg='grey')
        left_frame.grid(row=0, column=0, padx=10, pady=5)

        right_frame = tk.Frame(self, width=650, height=400, bg='grey')
        right_frame.grid(row=0, column=1, padx=10, pady=5)

        # Create a figure of specific size
        figure = Figure(figsize=(5, 5), dpi=100)

        # Define the points for plotting the figure
        plot = figure.add_subplot(1, 1, 1)

        # Define Data points for x and y axis
        x =  [0, 1, 2, 3, 4, 5 ,6,7,8,9,10,11]
        y = [0, 1, 2, 3, 4, 5 ,6,7,8,9,10,11] #Vo2Max
        plot.plot(x, y, color="red", marker="x", linestyle="solid")
        plot.set_xlabel('Month')
        plot.set_ylabel('Vo2Max')
        figure.tight_layout()
        # Add a canvas widget to associate the figure with canvas
        canvas = FigureCanvasTkAgg(figure, right_frame)
        canvas.get_tk_widget().grid(row=0, column=0)

        # Create frames and labels in left_frame
        tk.Label(left_frame, text="Are you in good shape?").grid(row=0, column=0, padx=5, pady=5)
        

        tk.Label(left_frame).grid(row=1, column=0, padx=50, pady=50)


        # Create tool bar frame
        tool_bar = tk.Frame(left_frame, width=180, height=185)
        tool_bar.grid(row=2, column=0, padx=5, pady=5)

        # Example labels that serve as placeholders for other widgets
        tk.Label(tool_bar, text="Tools", font=('Arial', 9, 'bold', 'underline'),relief=RAISED).grid(row=0, column=0, padx=5, pady=3, ipadx=10)  # ipadx is padding inside the Label widget
        weekavg =tk.Button(tool_bar, text="Weekly Average", command=lambda: controller.show_frame("weeklyavg")).grid(row=1, column=0, padx=5, pady=5)
        yearavg = tk.Button(tool_bar, text="Yearly Average", command=lambda: controller.show_frame("yearavg1")).grid(row=3, column=0, padx=5, pady=5)
        addmore=tk.Button(tool_bar, text="Add More Data", command=lambda: controller.show_frame("VO2Calc")).grid(row=4, column=0, padx=5, pady=5)
        coach = tk.Button(tool_bar, text = "Coach Mode", command = lambda: controller.show_frame("coachadddata")).grid(row = 6, column = 0, padx = 5, pady =5)        
        exitapp =tk. Button(tool_bar, text="Exit", command=close).grid(row=5, column=0, padx=5, pady=5)

class yearavg1(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

                # Create left and right frames
        left_frame = tk.Frame(self, width=200, height=400, bg='grey')
        left_frame.grid(row=0, column=0, padx=10, pady=5)

        right_frame = tk.Frame(self, width=650, height=400, bg='grey')
        right_frame.grid(row=0, column=1, padx=10, pady=5)

        # Create a figure of specific size
        figure = Figure(figsize=(5, 5), dpi=100)

        # Define the points for plotting the figure
        plot = figure.add_subplot(1, 1, 1)

        # Define Data points for x and y axis
        x = [1, 2, 3, 4, 5]
        y = [0, 1, 2, 3, 4 ] #Vo2Max
        plot.plot(x, y, color="red", marker="x", linestyle="solid")
        plot.set_xlabel('Year')
        plot.set_ylabel('Vo2Max')
        figure.tight_layout()
        
        # Add a canvas widget to associate the figure with canvas
        canvas = FigureCanvasTkAgg(figure, right_frame)
        canvas.get_tk_widget().grid(row=0, column=0)

        
        # Create frames and labels in left_frame
        tk.Label(left_frame, text="Are you in good shape?").grid(row=0, column=0, padx=5, pady=5)
        

        tk.Label(left_frame).grid(row=1, column=0, padx=50, pady=50)


        # Create tool bar frame
        tool_bar = tk.Frame(left_frame, width=180, height=185)
        tool_bar.grid(row=2, column=0, padx=5, pady=5)

        # Example labels that serve as placeholders for other widgets
        tk.Label(tool_bar, text="Tools", font=('Arial', 9, 'bold', 'underline'),relief=RAISED).grid(row=0, column=0, padx=5, pady=3, ipadx=10)  # ipadx is padding inside the Label widget
        weekavg =tk.Button(tool_bar, text="Weekly Average", command=lambda: controller.show_frame("weeklyavg")).grid(row=1, column=0, padx=5, pady=5)
        monthavg = tk.Button(tool_bar, text="Monthly Average", command=lambda: controller.show_frame("monthavg1")).grid(row=2, column=0, padx=5, pady=5)
        addmore=tk.Button(tool_bar, text="Add More Data", command=lambda: controller.show_frame("VO2Calc")).grid(row=4, column=0, padx=5, pady=5)
        coach = tk.Button(tool_bar, text = "Coach Mode", command = lambda: controller.show_frame("coachadddata")).grid(row = 6, column = 0, padx = 5, pady =5)        
        exitapp =tk. Button(tool_bar, text="Exit", command=close).grid(row=5, column=0, padx=5, pady=5)

class coachadddata(tk.Frame):
        
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Create left and right frames
        left_frame = tk.Frame(self, width=200, height=400, bg='grey')
        left_frame.grid(row=0, column=0, padx=10, pady=5)

        right_frame = tk.Frame(self, width=650, height=400, bg='grey')
        right_frame.grid(row=0, column=1, padx=10, pady=5)

        
        tk.Label(right_frame, text="Add your athlete's data", font=('Arial',20)).grid(row=0, column=0, padx=5, pady=5)
        
        def new_win():
            new = Toplevel(app)
            new.geometry("750x750")
            new.title("Coach's mode")

            tk.Label(new, text='Upload Here').pack(pady=10)

            
            def getExcel ():
                global df
            
                import_file_path = filedialog.askopenfilename()
                df = pd.read_excel (import_file_path)
                global bar1
                x = df['Day']
                y = df['Vo2Max']
                z = df['Vo2Max2']
                a = df['Vo2Max3']
                figure1 = Figure(figsize=(8,4), dpi=100)
                subplot1 = figure1.add_subplot(111)
                bar1 = FigureCanvasTkAgg(figure1, new)
                bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=0)
                vm1 =subplot1.plot(x, y, color='green',linestyle='dashed', linewidth = 3, marker='x', markerfacecolor='blue', markersize=12)
                vm2 =subplot1.plot(x, z, color='blue',linestyle='dashed', linewidth = 3, marker='x', markerfacecolor='blue', markersize=12)
                vm3 =subplot1.plot(x, a, color='red',linestyle='dashed', linewidth = 3, marker='x', markerfacecolor='blue', markersize=12)

                subplot1.legend([vm1[0],vm2[0],vm3[0]],["Chris", "Trevor", "Yujin"], loc = "upper right")
                subplot1.set_xlabel("Day")
                subplot1.set_ylabel("Vo2Max")
                subplot1.set_title("Vo2Max for your athletes")

                figure1.tight_layout()
            tk.Button(new,text='Load File', command=getExcel, bg='grey', fg='white', font=('helvetica', 12, 'bold')).pack(pady=5)
            

            tk.Button (new, text='Go Back', command=new.destroy, bg='grey',fg='white',  font=('helvetica', 11, 'bold')).pack(pady=5)

        
        tk.Button(right_frame, text = "Open", command = new_win).grid(row=1, column = 0, padx = 5, pady = 5)


        # Create frames and labels in left_frame
        tk.Label(left_frame, text="Are you in good shape?").grid(row=0, column=0, padx=5, pady=5)
        

        tk.Label(left_frame).grid(row=1, column=0, padx=50, pady=50)


        # Create tool bar frame
        tool_bar = tk.Frame(left_frame, width=180, height=185)
        tool_bar.grid(row=2, column=0, padx=5, pady=5)

        # Example labels that serve as placeholders for other widgets
        tk.Label(tool_bar, text="Tools", font=('Arial', 9, 'bold', 'underline'),relief=RAISED).grid(row=0, column=0, padx=5, pady=3, ipadx=10)  # ipadx is padding inside the Label widget
        weekavg =tk.Button(tool_bar, text="Weekly Average", command=lambda: controller.show_frame("weeklyavg")).grid(row=1, column=0, padx=5, pady=5)
        monthavg = tk.Button(tool_bar, text="Monthly Average", command=lambda: controller.show_frame("monthavg1")).grid(row=2, column=0, padx=5, pady=5)
        yearavg = tk.Button(tool_bar, text="Yearly Average", command=lambda: controller.show_frame("yearavg1")).grid(row=3, column=0, padx=5, pady=5)
        addmore=tk.Button(tool_bar, text="Add More Data", command=lambda: controller.show_frame("VO2Calc")).grid(row=4, column=0, padx=5, pady=5)
        exitapp =tk. Button(tool_bar, text="Exit", command = close).grid(row=5, column=0, padx=5, pady=5)

if __name__ == "__main__":
    app = Vo2Max()
    app.mainloop()