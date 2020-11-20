from tkinter import *
from PIL import ImageTk, Image
import os
from MainwithGUI import *

app = Tk()
app.title("Copy-Checker")
image2 = Image.open('front1.jpg')
image2 = image2.resize((1550, 850), Image.ANTIALIAS)
image1 = ImageTk.PhotoImage(image2)
w = image1.width()
h = image1.height()
app.geometry('%dx%d+120+100' % (w, h))


# Creating Menubar
menubar = Menu(app)


def window_for_exits():
    try:
        app.destroy()
    except:
        pass
    window_for_exit()


# Adding ans Menu and commands
ans = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Answer', menu=ans)
ans.add_separator()
ans.add_command(label='Model Answer', command=window_for_no_of_questions)
ans.add_separator()
ans.add_command(label='Student Answer', command=window_for_no_of_students)

# Adding Evaluate Menu and commands
evaluate = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Evaluate', menu=evaluate)
evaluate.add_command(label='Evaluate', command=window_for_evaluate)

# Adding Results Menu and commands
Result = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Result', menu=Result)
Result.add_command(label='Result', command=result)

# Adding Help Menu
help_ = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=help_)
help_.add_command(label='Instruction', command=showInstructions)

# quit
quit_ = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Quit', menu=quit_)
quit_.add_command(label='Quit', command=window_for_exits)

# display Menu
app.config(menu=menubar)
label1 = Label(app, image=image1,
               height=1500, fg="blue")
label1.pack()

app.mainloop()
