from tkinter import *
from PIL import ImageTk, Image
import os
from upload_file import window_for_upload_model_ans, window_for_upload_student_ans
from MainwithGUI import *


app = Tk()
app.title("Copy-Checker")
image2 = Image.open('front.jpg')
image2 = image2.resize((1550, 850), Image.ANTIALIAS)
image1 = ImageTk.PhotoImage(image2)
w = image1.width()
h = image1.height()
app.geometry('%dx%d+200+100' % (w, h))


# Creating Menubar
menubar = Menu(app)
menubar.configure(bg='yellow')


def window_for_exits():
    try:
        app.destroy()
    except:
        pass
    window_for_exit()


# Adding ans Menu and commands
ans = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Answer', menu=ans)
# ans.add_separator()
ans.add_command(label='Model Answer', command=window_for_no_of_questions)
# ans.add_separator()
ans.add_command(label='Student Answer', command=window_for_no_of_students)
# ans.add_separator()

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

# Upload files

upload_ = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Upload', menu=upload_)
upload_.add_command(label='Model Answer', command=window_for_upload_model_ans)
upload_.add_command(label='Student Answer',
                    command=window_for_upload_student_ans)


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
