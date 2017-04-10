from tkinter import *

master = Tk()

var = StringVar(master)
var.set("one") # initial value

option = OptionMenu(master, var, "one", "two", "three", "four")
option.grid()

#
# test stuff

def ok():
    print ("value is "+ var.get())
    master.quit()

button = Button(master, text="OK", command=ok)
button.grid()

mainloop()
