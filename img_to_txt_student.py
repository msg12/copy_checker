
import pytesseract as tess
from PIL import Image
import os


modelimgpath = './MODEL_ANSWER(img)/'
studentimgpath = './STUDENTS_ANSWER(img)/student'
studenttextpath = './STUDENTS_ANSWER(text)/student'
modeltextpath = './MODEL_ANSWER(text)/'

def func(no_of_questions,no_of_students):

    print("Student Answer Execution starts")
    for j in range(no_of_students):

        if not os.path.exists('./STUDENTS_ANSWER(text)/student'+str(j+1)+'/'):
            os.makedirs('./STUDENTS_ANSWER(text)/student'+str(j+1)+'/')

        for i in range(no_of_questions):
            ij = i + 1

            pp1=studentimgpath + str(j+1)+'/img'+str(i+1)+'.png'
            pp2=studenttextpath+str(j+1)+'/'+'q'+str(i+1)

            imgm=Image.open(pp1)
            text=tess.image_to_string(imgm)
            print(text)
            ff = open(pp2, "w")
            ff.write(text)
            ff.close()



    print("Student Answer Executed")


