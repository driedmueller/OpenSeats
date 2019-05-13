from tkinter import *
from tkinter import ttk

SEMESTERS = [
"201940",
"201970",
"201980"
]

COURSES = [
"CHEM",
"ENGL",
"MATH"
]

def ok():
    print (semester.get())
    print (course.get())

root = Tk()
root.title("Remaining Seats")

mainframe = ttk.Frame(root, padding="20 20")
mainframe.grid(column=0, row=0)

semester = StringVar()
course = StringVar()

#ttk.OptionMenu(mainframe, semester, SEMESTERS[0], *SEMESTERS).grid(row=1, column=2)
semesterCombo = ttk.Combobox(mainframe, state='readonly', textvariable=semester, 
                             values=('201940', '201970', '201980')).grid(row=1, column=2)
#ttk.OptionMenu(mainframe, course, COURSES[0], *COURSES).grid(row=2, column=2)
courseCombo = ttk.Combobox(mainframe, state='readonly', textvariable=course, 
                           values=('CHEM', 'ENGL', 'MATH')).grid(row=2, column=2)
ttk.Button(mainframe, text="Okay", command=ok).grid(row=3, column=2)

#combo['values'] = ('201940', '201970', '201980')
#combo.grid(row=1, column=3)

#for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

"""
set1 = OptionMenu(mainframe, var1, *SEMESTERS)
set1.configure(font=("Arial", 12))
set1.grid(row=0, column=2)
#set1.pack()

set2 = OptionMenu(mainframe, var2, *COURSES)
set2.configure(font=("Arial", 12))
set2.grid(row=1, column=2)
#set2.pack()

button = Button(mainframe, text="ok", command=ok)
button.grid(row=2, column=2)
#button.pack()
"""

#Activate
mainloop()
