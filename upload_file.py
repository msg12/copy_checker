from tkinter import *
import cv2
import os


def window_for_upload_student_ans():
    root = Tk()
    root.geometry("320x80")
    dest = './STUDENTS_ANSWER(img)/'

    def submit():
        newpath = create_student(dest)
        print(newpath)
        root1 = Tk()
        root1.geometry("300x120")
        src1_var = StringVar()

        dest1 = newpath

        def subsubmit1():
            src1 = src1_entry.get()
            print(src1)
            move_file(src1, dest1)
            src1_var.set("")

            def destroy_popups():
                try:
                    popup.destroy()
                except:
                    pass
                try:
                    root1.destroy()
                except:
                    pass
                try:
                    root.destroy()
                except:
                    pass

            popup = Tk()
            popup.wm_title(" ")

            B1 = Button(popup,
                        text="Done !!",
                        bg="green",
                        fg="yellow",
                        command=destroy_popups)
            B1.config(font=("Helvetica", 14))
            B1.pack(padx=50, pady=50)
            popup.mainloop()

        src1_label = Label(root1, text='import_path ',
                           font=('calibre',
                                 10, 'bold'))
        src1_entry = Entry(root1,
                           textvariable=src1_var, font=('calibre', 10, 'normal'))

        sub_btn1 = Button(root1, text='Ok',
                          bg="green",
                          fg="yellow",
                          command=subsubmit1)

        src1_label.grid(row=0, column=0, padx=10, pady=10)
        src1_entry.grid(row=0, column=1)
        sub_btn1.grid(row=3, column=1)
        root1.mainloop()

    def submit2():
        root2 = Tk()
        root2.geometry("300x120")
        src2_var = StringVar()
        stu2_var = StringVar()

        def subsubmit2():
            stu2 = stu2_entry.get()
            src2 = src2_entry.get()
            dest2 = dest+'student'+stu2
            print(src2)
            move_file(src2, dest2)
            src2_var.set("")

            def destroy_popups():
                try:
                    popup.destroy()
                except:
                    pass
                try:
                    root2.destroy()
                except:
                    pass
                try:
                    root.destroy()
                except:
                    pass

            popup = Tk()
            popup.wm_title(" ")

            B1 = Button(popup,
                        text="Done !!",
                        bg="green",
                        fg="yellow",
                        command=destroy_popups)
            B1.config(font=("Helvetica", 14))
            B1.pack(padx=50, pady=50)
            popup.mainloop()

        stu2_label = Label(root2, text='Student_No',
                           font=('calibre',
                                 10, 'bold'))
        stu2_entry = Entry(root2,
                           textvariable=stu2_var, font=('calibre', 10, 'normal'))
        src2_label = Label(root2, text='import_path ',
                           font=('calibre',
                                 10, 'bold'))
        src2_entry = Entry(root2,
                           textvariable=src2_var, font=('calibre', 10, 'normal'))

        sub_btn2 = Button(root2, text='Ok',
                          bg="green",
                          fg="yellow",
                          command=subsubmit2)
        stu2_label.grid(row=0, column=0, padx=10, pady=10)
        stu2_entry.grid(row=0, column=1)
        src2_label.grid(row=1, column=0, padx=10, pady=10)
        src2_entry.grid(row=1, column=1)
        sub_btn2.grid(row=3, column=1)
        root2.mainloop()

    sub_btn = Button(root, text='New Student',
                     bg="green",
                     fg="yellow", width=10,
                     height=2,
                     command=submit)
    sub_btn1 = Button(root, text='Existing Student',
                      bg="green",
                      fg="yellow", width=10,
                      height=2,
                      command=submit2)

    sub_btn.grid(row=3, column=1, padx=20, pady=15)
    sub_btn1.grid(row=3, column=2, padx=20, pady=15)

    root.mainloop()


def window_for_upload_model_ans():
    root = Tk()
    root.geometry("300x100")
    src_var = StringVar()
    dest = './MODEL_ANSWER(img)'

    def submit():
        src = src_entry.get()
        print(src)
        move_file(src, dest)
        src_var.set("")

        def destroy_popups():
            try:
                popup.destroy()
            except:
                pass
            try:
                root.destroy()
            except:
                pass

        popup = Tk()
        popup.wm_title(" ")

        B1 = Button(popup,
                    text="Done !!",
                    bg="green",
                    fg="yellow",
                    command=destroy_popups)
        B1.config(font=("Helvetica", 14))
        B1.pack(padx=50, pady=50)
        popup.mainloop()

    src_label = Label(root, text='import_path ',
                      font=('calibre',
                            10, 'bold'))
    src_entry = Entry(root,
                      textvariable=src_var, font=('calibre', 10, 'normal'))

    sub_btn = Button(root, text='Ok',
                     bg="green",
                     fg="yellow",
                     command=submit)

    src_label.grid(row=0, column=0, padx=10, pady=10)
    src_entry.grid(row=0, column=1)
    sub_btn.grid(row=3, column=1)
    root.mainloop()


def move_file(src, dest):
    img = cv2.imread(src, 1)
    files_dest = os.listdir(dest)
    img_name = 'img'+str(len(files_dest)+1)+'.png'
    cv2.imwrite(os.path.join(dest, img_name), img)
    cv2.waitKey(0)


def create_student(dest):
    files_dest = os.listdir(dest)
    # print(files_dest)
    abkistudent = len(files_dest)+1
    path = dest+'student'+str(abkistudent)
    try:
        os.mkdir(path)
        print("folder student created!!")
    except OSError as error:
        print(error)
    return path
