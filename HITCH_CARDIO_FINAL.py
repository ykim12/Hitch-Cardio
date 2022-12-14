from statistics import mean

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
mydb = mysql.connector.connect(
    host='localhost', password='hitchcardio12', user='root', database='hitchcardio')
mycursor = mydb.cursor()

dayUSER = 0  # global variable for day for single user

# VARIABLE NAMES OF EACH COLUMN OF DATABSE IN ORDER
# name, id, resting_HR, max_HR, VO2_max, isMale, day
# id is incremented by 1 every time a new user is created
# When isMale = 1, user is male. When isMale = 0, user is female.


def print_database():  # Prints current database. For error testing
    mycursor.execute("SELECT * FROM users")
    print("Database for GUI file:")
    for x in mycursor:
        print(x)

VO2_last30 = []
REST_last30 = []
MAX_last30 = []


def close():
    app.destroy()


class Vo2Max(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(
            family='Helvetica', size=18, weight="bold", slant="italic")
        self.title("Hitch Cardio")
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, weeklyavg, monthavg1, coachadddata):
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


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        logo = PhotoImage(file="hitchcardiologo.png")
        photoimage = logo.subsample(1, 1)

        # Position image on button
        label = tk.Label(self, image=photoimage)
        label.image = photoimage
        label.pack(side=TOP, pady=10)

        def leadpage1():
            controller.show_frame("PageOne")

        # another def to get information about the user
        button1 = tk.Button(self, text="View Health Stats", font=("Arial", 26),
                            command=leadpage1, height=2, width=30)
        # need to add another def of user info into the array

        button1.place(x=300, y=240)
        button1.pack(padx=10)


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Create left and right frames
        left_frame = tk.Frame(self, width=200, height=400, bg='grey')
        left_frame.grid(row=0, column=0, padx=10, pady=5)

        right_frame = tk.Frame(self, width=650, height=400, bg='grey')
        right_frame.grid(row=0, column=1, padx=10, pady=5)

        def clear_text():
            maxhr.delete(0, tk.END)
            resthr.delete(0, tk.END)
        

        # these arrays will be filled with data from data base to be graphed on the "Add More Data" page
        VO2_maxes = []
        MAX_HRs = []
        REST_HRs = []
        
        def fill_graphing_arrays():
            mycursor.execute("SELECT VO2_max from users WHERE name = 'USER1'")
            for x in mycursor:
                VO2_maxes.append(x) # creates list of all VO2 maxes to be graphed
            
            mycursor.execute("SELECT max_HR from users WHERE name = 'USER1'")
            for x in mycursor:
                MAX_HRs.append(x) # creates list of all max heart rates to be graphed
                
            mycursor.execute("SELECT resting_HR from users WHERE name = 'USER1'")
            for x in mycursor:
                REST_HRs.append(x) # creates list of all max heart rates to be graphed
            mydb.commit()
        
        fill_graphing_arrays()
        # initialize graph
        def create_graph():
            if(len(VO2_maxes) > 1 and len(VO2_maxes) < 3):
                def grapher():
                    # Create a figure of specific size
                    figure = Figure(figsize=(5, 5), dpi=100)
    
                    # Define the points for plotting the figure
                    plot = figure.add_subplot(1, 1, 1)
    
                    x = range(len(VO2_maxes))
                    # x doesn't need to be updated because length of all arrays stays the same. will error if different lengths
                    y = VO2_maxes
    
                    plot.plot(x, y, color="red", marker="x", linestyle="solid")
                    plot.set_xlabel('days')
                    figure.tight_layout()
                    # Add a canvas widget to associate the figure with canvas
                    canvas = FigureCanvasTkAgg(figure, right_frame)
                    canvas.get_tk_widget().grid(row=0, column=2, rowspan=10)
                graphlabel = tk.Label(right_frame, text="Would you like to see a graph so show your progress?").grid(
                    row=6, column=2, padx=5, pady=5)
                graphbutton = tk.Button(right_frame, text="Graph", command=grapher).grid(
                    row=7, column=2, padx=5, pady=5)
    
            if(len(VO2_maxes) > 2):
                # Create a figure of specific size
                figure = Figure(figsize=(4.2, 4.2), dpi=100)
                # Define the points for plotting the figure
                plot = figure.add_subplot(1, 1, 1)
    
                x = range(len(VO2_maxes))
                y = VO2_maxes
    
                vo2m = plot.plot(x, y, color="red", marker="x", linestyle="solid")
                plot.set_xlabel('Day')
                
                v = MAX_HRs
                mxhrs = plot.plot(x, v, color="blue", marker="x", linestyle="solid")
                
                z = REST_HRs
                rsthrs = plot.plot(x, z, color="green", marker="x", linestyle="solid")
                
                plot.legend([vo2m[0], mxhrs[0], rsthrs[0]], ["VO2 Max", "Max HR", "Rest HR"], loc="center left")
                figure.tight_layout()
                
                # Add a canvas widget to associate the figure with canvas
                canvas = FigureCanvasTkAgg(figure, right_frame)
                canvas.get_tk_widget().grid(row=0, column=2, rowspan=10)
                
        create_graph() # creates first graph user sees
        VO2_maxes.clear()
        MAX_HRs.clear()
        REST_HRs.clear()
            
        def update_graph():
            create_graph()
            # clears arrays of all variables for graph
            VO2_maxes.clear()
            MAX_HRs.clear()
            REST_HRs.clear()

        def deletelastinput():
            data = []
            mycursor.execute("SELECT * FROM users")
            for x in mycursor:  # creates list of all id's currently in database
                data.append(x[len(x)-6])

            sql = "DELETE FROM users WHERE id = %s"
            # selects last id to be deleted
            to_delete = (str(data[len(data)-1]), )
            # row is deleted where id is found
            mycursor.execute(sql, to_delete)
            mydb.commit()

            fill_graphing_arrays()
            
            # removes last item from each array so that the new graph won't include them
            VO2_maxes.pop(len(VO2_maxes)-1)
            MAX_HRs.pop(len(MAX_HRs)-1)
            REST_HRs.pop(len(REST_HRs)-1)
            update_graph()

        def calc():
            try:
                mycursor.execute("SELECT * FROM users WHERE name = 'USER1'")
                result = mycursor.fetchall()  # result is a list of tuples
                vo2max = -100  # -100 for error checking
                isMale = True  # defaults to male

                mx = int(maxhr.get())
                rest = int(resthr.get())
                vo2max = round(float(mx / rest)*15.3, 2)
                if(enter_gender.get() == 'F'):  # user is female
                    isMale = False

                name = "USER1"
                if(len(result) == 0):  # create new user
                    dayUSER = 0
                    mycursor.execute("INSERT INTO users (name, resting_HR, max_HR, VO2_max, isMale, day) VALUES (%s, %s, %s, %s, %s, %s)", (
                        name, rest, mx, vo2max, isMale, dayUSER))
                    mydb.commit()
                else:  # there is atleast one user named "USER1"
                    # for loop is to find out dayUSER for iteration
                    dayUSERTuple = mycursor.execute(
                        "SELECT day FROM users WHERE name = 'USER1'")
                    dayUSER = -1
                    for x in mycursor:  # grabs highest value of day where name = "USER1"
                        dayUSERMax = x[len(x)-1]
                        if(dayUSERMax > dayUSER):
                            dayUSER = dayUSERMax

                    # when creating a new row of USER1, dayUSERMax is increased by one to indicate new entry
                    dayUSER = dayUSER+1
                    mycursor.execute("INSERT INTO users (name, resting_HR, max_HR, VO2_max, isMale, day) VALUES (%s, %s, %s, %s, %s, %s)", (
                        name, rest, mx, vo2max, isMale, dayUSER))
                mydb.commit()

                fill_graphing_arrays()

                if (vo2max > 60):
                    tk.Label(right_frame, text="Your VO2Max is excellent!!!").grid(row=8, column=1, padx=5, pady=5)
                elif(vo2max >= 52) and (vo2max <= 60):
                    tk.Label(right_frame, text="Your VO2 max is good. Keep up the good work").grid(row=8, column=1, padx=5, pady=5)
                elif(vo2max >= 37) and (vo2max <= 51):
                    tk.Label(right_frame, text="Your VO2 max is average.").grid(row=8, column=1, padx=5, pady=5)
                elif(vo2max >= 30) and (vo2max <= 36):
                    tk.Label(right_frame, text="Your VO2 max is below average. Try hard to get back on track.").grid(row=8, column=1, padx=5, pady=5)
                elif(vo2max < 30):
                    tk.Label(right_frame, text="Your VO2 max isn't the best. Work hard to get better.").grid(row=8, column=1, padx=5, pady=5)

                update_graph()
            except ValueError:
                tk.messagebox.showerror("Error", "Please enter only integers.")

        # Create frames and labels in left_frame
        tk.Label(left_frame, text="Instructions:").grid(
            row=0, column=0, padx=5, pady=5)
        tk.Label(left_frame, text="If you are a new user or looking to put in more data,\n add more data on the right frame").grid(
            row=1, column=0, padx=5, pady=5)

        tk.Label(right_frame, text="Gender: (M/F)").grid(row=0,
                                                         column=1, padx=5, pady=5)
        enter_gender = tk.Entry(right_frame)
        enter_gender.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(right_frame, text="Enter your max heart rate: ").grid(
            row=2, column=1, padx=5, pady=5)
        maxhr = tk.Entry(right_frame)
        maxhr.grid(row=3, column=1)
        tk.Label(right_frame, text="Enter your resting heart rate: ").grid(
            row=4, column=1, padx=5, pady=5)
        resthr = tk.Entry(right_frame)
        resthr.grid(row=5, column=1)
        calculate = tk.Button(right_frame, text="Calculate",
                              command=calc).grid(row=6, column=1, padx=5, pady=5)
        addmore = tk.Button(right_frame, text="Add more", command=clear_text).grid(
            row=10, column=1, padx=5, pady=5)
        deletelast = tk.Button(right_frame, text="Delete last input",
                               command=deletelastinput).grid(row=9, column=1, padx=5, pady=5)

        tool_bar = tk.Frame(left_frame, width=180, height=185)
        tool_bar.grid(row=2, column=0, padx=5, pady=5)

        tk.Label(tool_bar, text="Tools", font=('Arial', 9, 'bold', 'underline'),
                 relief=RAISED).grid(row=0, column=0, padx=5, pady=3, ipadx=10)
        backbutton = tk.Button(tool_bar, text="Back", command=lambda: controller.show_frame(
            "PageOne")).grid(row=2, column=0, padx=5, pady=5)

        # Create tool bar frame
        tool_bar = tk.Frame(left_frame, width=180, height=185)
        tool_bar.grid(row=2, column=0, padx=5, pady=5)

        # Example labels that serve as placeholders for other widgets
        tk.Label(tool_bar, text="Tools", font=('Arial', 9, 'bold', 'underline'), relief=RAISED).grid(
            row=0, column=0, padx=5, pady=3, ipadx=10)  # ipadx is padding inside the Label widget
        weekavg = tk.Button(tool_bar, text="Weekly Average", command=lambda: controller.show_frame(
            "weeklyavg")).grid(row=1, column=0, padx=5, pady=5)
        monthavg = tk.Button(tool_bar, text="Monthly Average", command=lambda: controller.show_frame(
            "monthavg1")).grid(row=2, column=0, padx=5, pady=5)
        #yearavg = tk.Button(tool_bar, text="Yearly Average", command=lambda: controller.show_frame(
        #    "yearavg1")).grid(row=3, column=0, padx=5, pady=5)
        coach = tk.Button(tool_bar, text="Coach Mode", command=lambda: controller.show_frame(
            "coachadddata")).grid(row=4, column=0, padx=5, pady=5)
        exitapp = tk. Button(tool_bar, text="Exit", command=close).grid(
            row=5, column=0, padx=5, pady=5)


class weeklyavg(tk.Frame):

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
        x = [1, 2, 3, 4, 5, 6, 7]
        VO2_last7 = []
        REST_last7 = []
        MAX_last7 = []
        
        # fills each array with last 7 entries for user
        mycursor.execute("SELECT * FROM users WHERE name = 'USER1' ORDER BY day DESC LIMIT 7")
        data = mycursor.fetchall()
        for row in data:
            VO2_last7.append(row[4])
            REST_last7.append(row[2])
            MAX_last7.append(row[3])
        
        vo2m = plot.plot(x, VO2_last7, color="red", marker="x", linestyle="solid")
        maxhrs = plot.plot(x, REST_last7, color="green", marker="x", linestyle="solid")
        rsthrs = plot.plot(x, MAX_last7, color="blue", marker="x", linestyle="solid")
        
        plot.legend([vo2m[0], maxhrs[0], rsthrs[0]], ["VO2 Max", "Max HR", "Rest HR"], loc="center left")
        
        plot.set_xlabel('Day')
        
        figure.tight_layout()

        # Add a canvas widget to associate the figure with canvas
        canvas = FigureCanvasTkAgg(figure, right_frame)
        canvas.get_tk_widget().grid(row=0, column=0)

        # Create frames and labels in left_frame
        tk.Label(left_frame, text="Averages over last 7 days:").grid(
            row=0, column=0, padx=5, pady=5)

        tk.Label(left_frame, text="Resting heart rate: "+str(int(mean(REST_last7)))).grid(
            row=1, column=0, padx=5, pady=5)
        tk.Label(left_frame, text="Maximum heart rate: "+str(int(mean(MAX_last7)))).grid(
            row=2, column=0, padx=5, pady=5)
        tk.Label(left_frame, text="VO2 max: "+str(int(mean(VO2_last7)))).grid(
            row=3, column=0, padx=5, pady=5)

        # Create tool bar frame
        tool_bar = tk.Frame(left_frame, width=180, height=185)
        tool_bar.grid(row=4, column=0, padx=5, pady=5)

        # Example labels that serve as placeholders for other widgets
        tk.Label(tool_bar, text="Tools", font=('Arial', 9, 'bold', 'underline'),
                 relief=RAISED).grid(row=0, column=0, padx=5, pady=3, ipadx=10)

        backbutton = tk.Button(tool_bar, text="Back", command=lambda: controller.show_frame(
            "PageOne")).grid(row=2, column=0, padx=5, pady=5)


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
        x = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29]
        
        # fills each array with last 30 entries for user
        mycursor.execute("SELECT * FROM users WHERE name = 'USER1' ORDER BY day DESC LIMIT 30")
        data = mycursor.fetchall()
        count = 0
        for row in data:
            count= count+1
            VO2_last30.append(row[4])
            REST_last30.append(row[2])
            MAX_last30.append(row[3])
        VO2_last30.reverse()
        REST_last30.reverse()
        MAX_last30.reverse()
        
        print(count)
        if(count>=30): # there is enough data to create this graph
            vo2m = plot.plot(x, VO2_last30, color="red", marker="x", linestyle="solid")
            maxhrs = plot.plot(x, REST_last30, color="green", marker="x", linestyle="solid")
            rsthrs = plot.plot(x, MAX_last30, color="blue", marker="x", linestyle="solid")
            
            plot.legend([vo2m[0], maxhrs[0], rsthrs[0]], ["VO2 Max", "Max HR", "Rest HR"], loc="center left")
            
            plot.set_xlabel('Month')
            figure.tight_layout()
    
            # Add a canvas widget to associate the figure with canvas
            canvas = FigureCanvasTkAgg(figure, right_frame)
            canvas.get_tk_widget().grid(row=0, column=0)
    
            # Create frames and labels in left_frame
            tk.Label(left_frame, text="Averages over last 30 days:").grid(
                row=0, column=0, padx=5, pady=5)
    
            tk.Label(left_frame, text="Resting heart rate: "+str(int(mean(REST_last30)))).grid(
                row=1, column=0, padx=5, pady=5)
            tk.Label(left_frame, text="Maximum heart rate: "+str(int(mean(MAX_last30)))).grid(
                row=2, column=0, padx=5, pady=5)
            tk.Label(left_frame, text="VO2 max: "+str(int(mean(VO2_last30)))).grid(
                row=3, column=0, padx=5, pady=5)
    
            # Create tool bar frame
            tool_bar = tk.Frame(left_frame, width=180, height=185)
            tool_bar.grid(row=4, column=0, padx=5, pady=5)
    
            # Example labels that serve as placeholders for other widgets
            tk.Label(tool_bar, text="Tools", font=('Arial', 9, 'bold', 'underline'),
                     relief=RAISED).grid(row=0, column=0, padx=5, pady=3, ipadx=10)
    
            backbutton = tk.Button(tool_bar, text="Back", command=lambda: controller.show_frame(
                "PageOne")).grid(row=2, column=0, padx=5, pady=5)
        else:
            tool_bar = tk.Frame(left_frame, width=180, height=185)
            tool_bar.grid(row=4, column=0, padx=5, pady=5)
            tk.Label(left_frame, text="Not enough data in the database").grid(
                row=1, column=0, padx=5, pady=5)
            backbutton = tk.Button(tool_bar, text="Back", command=lambda: controller.show_frame(
                "PageOne")).grid(row=2, column=0, padx=5, pady=5)

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
            tk.Label(new, text = "Make sure you have your athlete's resting and max heart rates").pack(pady=0)
            # tk.Label(new, text = "Enter athlete's name in order separated by comma").pack(pady=10)

            # def command1():
            #     name = ((names_list.get().split(",")))

            # names_list = StringVar()
            
            # names = tk.Entry(new, textvariable = names_list).pack(pady=10)
            # button = Button(new, text="Ok", command=command1).pack(pady = 10)


            def getExcel ():
                try:

                    global df
                    import_file_path = filedialog.askopenfilename()
                    df = pd.read_excel (import_file_path)

                    global bar1
                    x = df['Day']

                    #athlete 1 rest and max hr
                    resthr1 = df["resthr1"]
                    maxhr1 = df["maxhr1"]
                    a = []
                    for b in range(len(resthr1)):
                            vo21 = round((maxhr1[b]/resthr1[b])*15.3,3)
                            a.append(vo21)
                    a_mean = round(mean(a),3)

                    #athlete 1 rest and max hr
                    resthr2 = df["resthr2"]
                    maxhr2 = df["maxhr2"]
                    c = []
                    for b in range(len(resthr2)):
                            vo21 = round((maxhr2[b]/resthr2[b])*15.3,3)
                            c.append(vo21)
                    c_mean = round(mean(c),3)

                    #athlete 1 rest and max hr
                    resthr3 = df["resthr3"]
                    maxhr3 = df["maxhr3"]
                    d = []
                    for b in range(len(resthr3)):
                            vo21 = round((maxhr3[b]/resthr3[b])*15.3,3)
                            d.append(vo21)
                    d_mean = round(mean(d),3)
        

                    figure1 = Figure(figsize=(4,4), dpi=100)
                    subplot1 = figure1.add_subplot(111)
                    bar1 = FigureCanvasTkAgg(figure1, new)
                    bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=0)
                    vm1 =subplot1.plot(x, a, color='green',linestyle='dashed', linewidth = 3, marker='x', markerfacecolor='blue', markersize=12)
                    vm2 =subplot1.plot(x, c, color='blue',linestyle='dashed', linewidth = 3, marker='x', markerfacecolor='blue', markersize=12)
                    vm3 =subplot1.plot(x, d, color='red',linestyle='dashed', linewidth = 3, marker='x', markerfacecolor='blue', markersize=12)

                    subplot1.legend([vm1[0],vm2[0],vm3[0]],["Yujin", "Chris", "Trevor"], loc = "upper right")
                    subplot1.set_xlabel("Day")
                    subplot1.set_title("VO2Max for your athletes")

                    figure1.tight_layout()
                    means = [a_mean,c_mean,d_mean]
                    
                    text = ["","",""]
                    
                    for x in range(len(means)):
                        if (means[x] > 60):
                            text[x] = " VO2Max is excellent!!!"
                        elif(means[x] >=52) and (means[x] <=60):
                            text[x] = " VO2 max is good."
                        elif(means[x]>=37) and (means[x]<=51):
                            text[x] = " VO2 max is average."
                        elif(means[x]>=30) and (means[x] <=36):
                            text[x] = " VO2 max is not good. Need to try hard to get back on track."
                        elif(means[x]<30):
                            text[x] = " VO2max is very bad. Need to work hard to get better."



                    canvas = Canvas(new, width = 300, height = 150, bg = "grey")
                    canvas.create_text(150,50,text = f"Yujin's weekly Vo2Max: {a_mean}{text[0]}", fill = "black")
                    canvas.create_text(150,75,text = f"Chris's weekly Vo2Max: {c_mean}{text[1]}", fill = "black")
                    canvas.create_text(150,100,text = f"Trevor's weekly Vo2Max: {d_mean}{text[2]}", fill = "black")
                    canvas.pack()

                except Exception as e:
                    tk.messagebox.showerror("Error", "Incorrect file type")
                
            tk.Button(new,text='Load File', command=getExcel, bg='grey', fg='white', font=('helvetica', 12, 'bold')).pack(pady=5)
            tk.Button (new, text='Go Back', command=new.destroy, bg='grey',fg='white',  font=('helvetica', 11, 'bold')).pack(pady=5)
        
        tk.Button(right_frame, text = "Open", command = new_win).grid(row=1, column = 0, padx = 5, pady = 5)



                # Create frames and labels in left_frame
        tk.Label(left_frame, text="Instructions:").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(left_frame, text="Click open to proceed").grid(row = 1, column=0, padx=5, pady=5)


        # Create tool bar frame
        tool_bar = tk.Frame(left_frame, width=180, height=185)
        tool_bar.grid(row=2, column=0, padx=5, pady=5)

        # Example labels that serve as placeholders for other widgets
        tk.Label(tool_bar, text="Tools", font=('Arial', 9, 'bold', 'underline'),relief=RAISED).grid(row=0, column=0, padx=5, pady=3, ipadx=10)  # ipadx is padding inside the Label widget
        backbutton = tk.Button(tool_bar, text = "Back",command=lambda: controller.show_frame("PageOne")).grid(row = 2,column = 0,padx = 5,pady = 5)

if __name__ == "__main__":
    app = Vo2Max()
    app.mainloop()
