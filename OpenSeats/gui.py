import tkinter as tkr

master = tkr.Tk()
master.geometry("200x100")
master.title("Dropdown List")

tkr.Label(master, text="Basic Dropdown List").grid(row=0)

var = tkr.StringVar()

set1 = tkr.OptionMenu(master, var, "1", "2", "3")
set1.configure(font=("Arial", 20))
set1.grid(row=1, column=0)

#Activate
tkr.mainloop()
