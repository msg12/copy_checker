
import pytesseract as tess
from PIL import Image


modelimgpath = './MODEL_ANSWER(img)/'
studentimgpath = './STUDENTS_ANSWER(img)/student'
studenttextpath = './STUDENTS_ANSWER(text)/student'
modeltextpath = './MODEL_ANSWER(text)/'


def func(no_of_questions):
    print("Model Answer Executions starts")
    
    for i in range(no_of_questions):
        ii = i + 1
        model_img_path=modelimgpath+'img'+str(i+1)+'.png'

        imgm=Image.open(model_img_path)
        text=tess.image_to_string(imgm)
        print(text)
        ff = open(modeltextpath+'q'+str(i+1), "w")
        ff.write(text)
        ff.close()



    print("Model Answer Executed")