from tkinter import *
from PIL import ImageTk, Image


def window_for_viewing_model_ans():
    root = Tk()
    root.geometry("300x100")
    quesno1 = StringVar()

    def submit():
        ques_no = ques_entry.get()
        print(ques_no)
        path = './MODEL_ANSWER(img)/' + 'img' + str(ques_no) + '.png'
        print(path)
        md = Toplevel()
        canvas = Canvas(md, width=1000, height=600)
        canvas.pack()
        img = ImageTk.PhotoImage(Image.open(path))
        canvas.create_image(500, 300, anchor=CENTER, image=img)
        md.mainloop()

        quesno1.set("")

        def destroy_popups():
            try:
                root.destroy()
            except:
                pass
            try:
                md.destroy()
            except:
                pass

    ques_label = Label(root, text='Question_No',
                       font=('calibre',
                             10, 'bold'))
    ques_entry = Entry(root,
                       textvariable=quesno1, font=('calibre', 10, 'normal'))

    sub_btn = Button(root, text='Ok',
                     bg="green",
                     fg="yellow",
                     command=submit)

    ques_label.grid(row=0, column=0, padx=10, pady=10)
    ques_entry.grid(row=0, column=1)
    sub_btn.grid(row=3, column=1)
    root.mainloop()


def window_for_viewing_student_ans():
    root = Tk()
    root.geometry("300x150")
    quesno1 = StringVar()
    stu_var = StringVar()

    def submit():
        stu = stu_entry.get()
        ques_no = ques_entry.get()
        print(stu+" "+ques_no)
        path = './STUDENTS_ANSWER(img)/' + 'student' + \
            str(stu)+'/'+'img'+str(ques_no) + '.png'
        print(path)
        md = Toplevel()
        canvas = Canvas(md, width=1000, height=600)
        canvas.pack()
        img = ImageTk.PhotoImage(Image.open(path))
        canvas.create_image(500, 300, anchor=CENTER, image=img)
        md.mainloop()

        quesno1.set("")

        def destroy_popups():
            try:
                root.destroy()
            except:
                pass
            try:
                md.destroy()
            except:
                pass

    stu_label = Label(root, text='Student_No',
                      font=('calibre',
                            10, 'bold'))
    stu_entry = Entry(root,
                      textvariable=stu_var, font=('calibre', 10, 'normal'))
    ques_label = Label(root, text='Question_No ',
                       font=('calibre',
                             10, 'bold'))
    ques_entry = Entry(root,
                       textvariable=quesno1, font=('calibre', 10, 'normal'))

    sub_btn = Button(root, text='Ok',
                     bg="green",
                     fg="yellow",
                     command=submit)
    stu_label.grid(row=0, column=0, padx=10, pady=10)
    stu_entry.grid(row=0, column=1)
    ques_label.grid(row=1, column=0, padx=10, pady=10)
    ques_entry.grid(row=1, column=1)
    sub_btn.grid(row=3, column=1)
    root.mainloop()
