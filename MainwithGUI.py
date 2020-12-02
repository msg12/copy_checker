import webbrowser
import tkinter.messagebox
from tkinter import *
import img_to_txt_student
import img_to_txt_model
from PIL import Image
import pytesseract as tess
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import OrderedDict
from nltk.stem import WordNetLemmatizer, PorterStemmer, LancasterStemmer, SnowballStemmer
from nltk.corpus import stopwords, wordnet
import nltk
import os
no_of_questions, no_of_students = 10, 2


modelimgpath = './MODEL_ANSWER(img)/'
studentimgpath = './STUDENTS_ANSWER(img)/student'
studenttextpath = './STUDENTS_ANSWER(text)/student'
modeltextpath = './MODEL_ANSWER(text)/'


def model_things():

    i = 2
    img_to_txt_model.func(no_of_questions)


def student_things():

    i = 2
    img_to_txt_student.func(no_of_questions, no_of_students)


def generatekeywords(filepath2):
    f = open(filepath2, "r")
    file_content = f.read()
    f.close()

    word_list = nltk.word_tokenize(file_content)

    tagged_word_list = nltk.pos_tag(word_list)

    stop_words = set(stopwords.words("english"))
    filtered_word_list = []
    for i in tagged_word_list:
        if i[0] not in stop_words:
            filtered_word_list.append(i)

    stemmed_word_list = []
    for i in filtered_word_list:
        if (i[0][len(i[0]) - 2:] == 'ly'):
            k = LancasterStemmer().stem(i[0])
            if (semanticsimilarity(k, i[0]) >= 0.6):
                stemmed_word_list.append(k)
            else:
                stemmed_word_list.append(i)
        elif (i[0][len(i[0]) - 1] != 'e'):
            k = PorterStemmer().stem(i[0])
            if (semanticsimilarity(k, i[0]) >= 0.6):
                stemmed_word_list.append(k)
            else:
                stemmed_word_list.append(i)
        else:
            stemmed_word_list.append(i)

    lemmatizer = WordNetLemmatizer()
    lemmatized_word_list = []
    for i in stemmed_word_list:
        k = lemmatizer.lemmatize(i[0])
        if (semanticsimilarity(k, i[0]) >= 0.6):
            lemmatized_word_list.append(k)
        else:
            lemmatized_word_list.append(i)
    # tagged_word_list = lemmatized_word_list
    # print(lemmatized_word_list)
    # tagged_word_list = stemmed_word_list
    final_processed_word_list = []
    for i in tagged_word_list:
        if (i[1] == 'CD' or i[1] == 'FW' or i[1] == 'NN' or i[1] == 'NNS'
                or i[1] == 'NNP' or i[1] == 'NNPS' or i[1] == 'JJ'):

            final_processed_word_list.append(i[0])
    final_processed_word_list = list(
        OrderedDict.fromkeys(final_processed_word_list))

    return (final_processed_word_list)


def semanticsimilarity(a, b):
    a, b = a.lower(), b.lower()  # converting them into lowercase

    l1 = wordnet.synsets(a)  # printing synsets of a
    l2 = wordnet.synsets(b)  # printing synsets of b

    if (len(l1) == 0 or len(l2) == 0):
        return (0)
    similarity = -1

    synonymsofl1 = []
    antonymsofl2 = []

    for i in l1:
        for l in i.lemmas():
            synonymsofl1.append(l.name())

    for i in l2:
        for l in i.lemmas():
            if (l.antonyms()):
                antonymsofl2.append(l.antonyms()[0].name())

    for i in synonymsofl1:
        for j in antonymsofl2:
            if (i == j):
                return (0)  # If exactly opposite return similarity as zero.

    max1similarity = -1
    for i in l1:
        for j in l2:
            if (i.wup_similarity(j) == None):
                continue
            if (max1similarity < i.wup_similarity(j)):
                max1similarity = i.wup_similarity(j)
    max2similarity = -1
    for i in l2:
        for j in l1:
            if (i.wup_similarity(j) == None):
                continue
            if (max2similarity < i.wup_similarity(j)):
                max2similarity = i.wup_similarity(j)

    return (max(max1similarity, max2similarity))


def mapp_it(s, t1):

    for i in range(len(t1)):
        t1[i] = t1[i].lower()

    s = s.lower()
    sent = sent_tokenize(s)
    word = word_tokenize(s)
    tag_word = nltk.pos_tag(word)

    tag_t1 = nltk.pos_tag(t1)

    noun = []
    extra_noun = []
    adj = []

    new_sent = []
    breaker = []
    for i in sent:
        tokenize_now = word_tokenize(i)
        pos = nltk.pos_tag(tokenize_now)
        prev = 0
        for j in range(len(pos)):
            if pos[j][1] == "UH" or pos[j][1] == "IN" or pos[j][
                    1] == "CC" or tokenize_now[j] == "?" or tokenize_now[
                        j] == "." or tokenize_now[j] == "," or pos[j][
                            1] == "LS":
                new_sent.append(pos[prev:j:])
                breaker.append(pos[j])
                prev = j + 1

    mapp = []
    re = 0
    for j in range(len(new_sent)):
        re = 0
        for i in range(len(new_sent[j])):

            if re == 0:
                if new_sent[j][i][0] in t1:
                    re = 1
                    mapp.append([new_sent[j][i]])
            elif re == 1 and new_sent[j][i][0] in t1:
                mapp[len(mapp) - 1].append(new_sent[j][i])

    rem = []
    las = 0
    for i in range(len(mapp)):
        pres = 0
        if len(mapp[i]) != 1:
            las = i
            for j in mapp[i]:
                if j[1] == "NN" or j[1] == "NNP":
                    pres = 1
        if pres == 0:
            for j in mapp[i]:
                mapp[i - 1].append(j)
            rem.append(i)

    for i in range(len(rem) - 1, -1, -1):
        if len(mapp[rem[i]]) != 1:
            for j in range(1, len(mapp[rem[i]])):
                mapp[rem[i] - 1].append(mapp[rem[i]][j])

    count = 0
    for i in rem:
        z = mapp.pop(i - count)
        count += 1

    app = []
    rem = []
    for i in range(len(mapp)):
        for j in range(len(mapp[i])):
            if mapp[i][j][1] == "JJ":
                nex = 1
                for k in range(len(word)):
                    z = word[k].find(mapp[i][j][0])
                    if z != -1 and k != 0:
                        if nltk.pos_tag(
                                word[k - 1:k:])[0][1] == "VBZ" or nltk.pos_tag(
                                    word[k -
                                         1:k:])[0][1] == "VBD" or nltk.pos_tag(
                                             word[k - 1:k:]
                        )[0][1] == "JJ" or nltk.pos_tag(
                                             word[k -
                                                  1:k:])[0][1][:2:] == "RB":
                            nex = 0
                            break
                if j == len(mapp[i]) - 1:
                    nex = 0
                if nex:
                    app.append([mapp[i][j + 1], mapp[i][j]])
                    rem.append([i, mapp[i][j]])
                    rem.append([i, mapp[i][j + 1]])
                else:
                    app.append([mapp[i][j - 1], mapp[i][j]])
                    rem.append([i, mapp[i][j]])
                    rem.append([i, mapp[i][j - 1]])

    for i in rem:
        if i[1] in mapp[i[0]]:
            mapp[i[0]].remove(i[1])

    mapp += app

    for i in mapp:
        if i == []:
            mapp.remove([])

    rem = []
    for i in range(1, len(mapp)):
        pres = 0
        for j in mapp[i]:
            if j[1][:2:] != "NN":
                pres = 1
                break
        if pres == 0:
            rem.append(i)

    for i in range(len(rem) - 1, -1, -1):
        for j in mapp[rem[i]]:
            mapp[rem[i] - 1].append(j)
        z = mapp.pop(rem[i])

    rem = []
    las = 0
    for i in range(1, len(mapp)):
        pres = 0
        if len(mapp[i]) != 1:
            las = i
            for j in mapp[i]:
                if j[1][:2:] == "NN":
                    pres = 1
        if pres == 0:
            rem.append(i)

    count = 0
    for i in rem:
        z = mapp.pop(i - count)
        count += 1
    las = -1
    for i in range(len(tag_word)):
        if tag_word[i][1] == "JJ" or tag_word[i][1][:2:] == "RB":
            if las == i - 1:
                mapp.append([tag_word[i], tag_word[i - 1]])
            las = i

    for i in range(1, len(mapp)):
        mapp[0].append(mapp[i][0])

    z1 = 0
    if "known as" in s:
        z = "known"
        z1 = 1
    elif "called" in word:
        z = "called"
        z1 = 1
    if z1:
        sent = sent_tokenize(s)
        for i in sent:
            if z in i:
                t = word_tokenize(i)
                tag = nltk.pos_tag(t)
                for x in tag:

                    if x[1][:2:] == "NN":
                        for j in range(len(mapp)):
                            for k in range(len(mapp[j])):
                                if mapp[j][k][0] == x[0]:
                                    z = mapp[j].pop(k)
                                    mapp[0].insert(0, x)

    return mapp


def match(mapp1, mapp2):
    count = 0
    neg = 0
    for i in mapp1:
        main = i[0][0]
        flg = 0
        pres = -5
        for j in mapp2:
            sim = semanticsimilarity(main, j[0][0])
            if sim > 0.9:
                flg = 1
                pres = -1
                for k in range(1, len(i)):
                    c = count
                    pres = 0
                    for l in j:
                        sim_word = semanticsimilarity(l[0], i[k][0])
                        if sim_word > 0.75 and l != j[0]:
                            pres = 1
                            count += 1
                            # print(count,i[k][0],l[0])
                            x = 0
                            for z in range(len(mapp2)):
                                if mapp2[z][0][0] == l[0]:
                                    if mapp2[z][1][0] == "not" or mapp2[z][1][
                                            0] == "nor" or mapp2[z][1][
                                                0] == "neither" or mapp2[z][1][
                                                    0] == "never":
                                        x = 1
                                        # count-=1
                                        # neg+=1
                                        break
                            if x == 1:
                                pres = 2
                            break
                        elif sim_word == 0:
                            for z in range(len(mapp2)):
                                if mapp2[z][0][0] == l[0]:
                                    if mapp2[z][1][0] == "not" or mapp2[z][1][
                                            0] == "nor" or mapp2[z][1][
                                                0] == "neither" or mapp2[z][1][
                                                    0] == "never":
                                        ant = ""
                                        for s in wordnet.synsets(
                                                mapp2[z][0][0]):
                                            p = 1
                                            for le in s.lemmas():
                                                if le.antonyms():
                                                    ant += le.antonyms(
                                                    )[0].name()
                                                    p = 0
                                                    break
                                            if p == 0:
                                                break

                                        sim_word = semanticsimilarity(
                                            ant, i[k][0])
                                        if sim_word > 0.8:
                                            pres = 1
                                            count += 1
                                            break
                    # sprint(c,count)
                    if c == count:
                        if pres != 2:
                            pres = 0
                            for y in j:
                                for z in mapp2:
                                    if y == z[0]:
                                        for x in z:
                                            if semanticsimilarity(
                                                    i[k][0], x[0]) > 0.8:
                                                pres = 1
                                                # print(1)
                                                break
                                        if pres == 1:
                                            # print(2)
                                            break
                                if pres == 1:
                                    # print(3)
                                    break
                            if pres == 1:
                                count += 1
                            else:
                                neg += 1
        if flg == 0:
            for y in mapp2:
                for x in y:
                    if semanticsimilarity(x[0], i[0][0]) > 0.9:
                        for k in range(1, len(i)):
                            pres = 0
                            for l in y:
                                sim_word = semanticsimilarity(l[0], i[k][0])
                                if sim_word > 0.8 and l != j[0]:
                                    x = 0
                                    for z in range(len(mapp2)):
                                        if mapp2[z][1][0] == "not" or mapp2[z][
                                                1][0] == "nor" or mapp2[z][1][
                                                    0] == "neither" or mapp2[
                                                        z][1][0] == "never":
                                            ant = ""
                                            x = 1
                                            break
                                        elif sim_word == 0:
                                            for z in range(len(mapp2)):
                                                if mapp2[z][0] == l[0]:
                                                    if mapp2[z][1][0] == "not" or mapp2[
                                                            z][1][0] == "nor" or mapp2[
                                                                z][1][0] == "neither" or mapp2[
                                                                    z][1][
                                                                        0] == "never":
                                                        ant = ""
                                                        for s in wordnet.synsets(
                                                            mapp2[z][0]
                                                                [0]):
                                                            p = 1
                                                            for le in s.lemmas(
                                                            ):
                                                                if le.antonyms(
                                                                ):
                                                                    ant = le.lantonyms(
                                                                    )[0].name(
                                                                    )
                                                                    p = 0
                                                                    break
                                                            if p == 0:
                                                                break
                                                        sim_word = semanticsimilarity(
                                                            ant, i[k][0])
                                                        if sim_word > 0.8:
                                                            pres = 1
                                                            break

                            if pres == 1:
                                count += 1
                            else:
                                for y in j:
                                    for z in mapp2:
                                        if y == z[0]:
                                            for x in z:
                                                if semanticsimilarity(
                                                        i[k][0], x[0]) > 0.8:
                                                    pres = 1
                                                    break
                                            if pres == 1:
                                                break
                                    if pres == 1:
                                        break
                                if pres == 1:
                                    count += 1
                                else:
                                    neg += 1
    if neg == 0 and count == 0:
        return 0.0
    return count / (count + neg)


def generatescore():

    global no_of_questions
    global no_of_students
    print(no_of_questions)
    print(no_of_students)
    for i in range(no_of_questions):
        filepath = modeltextpath + 'q' + str(i + 1)
        model_keywords = generatekeywords(filepath)
        f = open(filepath, "r")
        model_content = f.read()
        f.close()
        index = 0
        for k in range(len(model_content)):
            if (model_content[k].isalpha()):
                index = k
                break
        model_content = model_content[index:]

        for j in range(no_of_students):
            filepath = studenttextpath + str(j + 1) + '/' + 'q' + str(i + 1)
            student_keywords = generatekeywords(filepath)
            f = open(filepath, "r")
            student_content = f.read()
            f.close()

            index = 0
            for l in range(len(student_content)):
                index2 = 0
                if (student_content[l].isalpha()):
                    index2 = l
                    break
            student_content = student_content[index2:]

            score = match(mapp_it(model_content, model_keywords),
                          mapp_it(student_content, student_keywords))

            score = round(score * 100, 2)
            if (j == 0 and i == 0):
                with open("score.txt", 'w') as f:

                    f.write(str(score) + " ")
            else:
                with open("score.txt", 'a') as f:
                    f.write(str(score) + " ")
            print(score)

        with open("score.txt", 'a') as f:
            f.write("\n")


# myApp = Tk()
# myApp.title("AutoCheckMyAnswer")


def result():

    import tkinter
    from prettytable import PrettyTable
    root = Tk()
    root.title("Results")

    f = open("score.txt", "r")
    line = []
    line.append(f.readline())
    while line[len(line) - 1]:
        line[len(line) - 1] = line[len(line) - 1].split(" ")
        line.append(f.readline())

    f.close()
    line.remove(line[len(line) - 1])

    for i in range(len(line)):
        line[i] = line[i][:len(line[i]) - 1]
    print(line)
    head = [" "]
    for i in range(len(line)):
        head.append("Que " + str(i + 1))

    t = PrettyTable(head)

    line_new = []
    for i in range(len(line[0])):
        line_new.append(["Student " + str(i + 1)])

    for i in range(len(line)):
        for j in range(len(line[i])):
            line_new[j].append(line[i][j])
    print(line_new)

    for i in line_new:
        t.add_row(i)

    label = Label(root, text=t)
    label.config(font=("Courier", 44))
    label.pack()

    root.mainloop()


def window_for_exit():
    def yes_delete_everything():
        # myApp.destroy()
        try:
            master.destroy()
        except:
            pass

    def no_exit():
        # myApp.destroy()
        try:
            master.destroy()
        except:
            pass

    master = Tk()
    master.title(" ")
    option_label = Label(master,
                         text="Do You Want To exit deleting all the data ?",
                         bg="green",
                         fg="yellow")
    option_label.config(font=("Helvetica", 17))
    option_label.grid(row=0, column=0, columnspan=2, sticky=N + E + S + W)

    yes_button = Button(master, text="Yes", command=yes_delete_everything)
    yes_button.config(font=("Helvetica", 14))
    yes_button.grid(row=2, column=0, sticky=N + E + S + W)

    no_button = Button(master, text="NO", command=no_exit)
    no_button.config(font=("Helvetica", 14))
    no_button.grid(row=2, column=1, sticky=N + E + S + W)

    master.mainloop()


def window_for_no_of_questions():
    global no_of_questions

    def confirm():
        global no_of_questions

        question = entry_field.get()
        no_of_questions = int(question)
        model_things()
        print(no_of_questions)

        def destroy_popups():
            try:
                popup.destroy()
            except:
                pass
            try:
                master.destroy()
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

    master = Tk()
    master.title(" ")
    label = Label(master, text="Enter No.of Questions", fg="purple")
    label.config(font=("Helvetica", 17))
    label.grid(row=0, column=0, sticky=N + E + S + W)

    entry_field = Entry(master)
    entry_field.config(font=("Helvetica", 17))
    entry_field.grid(row=0, column=1, sticky=N + E + S + W)

    entry_field.focus_set()

    entry_button = Button(master,
                          text="Confirm",
                          bg="green",
                          fg="yellow",
                          command=confirm)
    entry_button.config(font=("Helvetica", 17))
    entry_button.grid(row=1, column=1, sticky=N + E + S + W)

    wait_label = Label(
        master,
        text="Please wait for some minutes a popup will appear after processing is finished",
        fg="blue")
    wait_label.config(font=("Helvetica", 14))
    wait_label.grid(row=2, column=0, columnspan=2, sticky=N + E + S + W)

    master.mainloop()


def window_for_evaluate():

    global no_of_questions
    global no_of_students

    def confirm():
        global no_of_questions
        global no_of_students
        generatescore()

        def destroy_popups():
            try:
                popup.destroy()
            except:
                pass
            try:
                master.destroy()
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

    master = Tk()
    master.title(" ")
    entry_button = Button(master,
                          text="Generate Students Score",
                          bg="green",
                          fg="yellow",
                          command=confirm)
    entry_button.config(font=("Helvetica", 17))
    entry_button.grid(row=0, column=0, columnspan=2, sticky=N + E + S + W)

    wait_label = Label(
        master,
        text="Please wait for some minutes a popup will appear after Evaluation is finished"
    )
    wait_label.config(font=("Helvetica", 17))
    wait_label.grid(row=1, column=0, columnspan=2, sticky=N + E + S + W)

    master.mainloop()


def window_for_no_of_students():
    global no_of_questions
    global no_of_students

    def confirm():
        student = entry1_field.get()
        global no_of_questions
        global no_of_students
        no_of_students = int(student)

        student_things()

        def destroy_popups():
            try:
                popup1.destroy()
            except:
                pass
            try:
                master1.destroy()
            except:
                pass

        popup1 = Tk()
        popup1.wm_title(" ")

        B2 = Button(popup1,
                    text="Done !!",
                    bg="green",
                    fg="yellow",
                    command=destroy_popups)
        B2.config(font=("Helvetica", 14))
        B2.pack(padx=50, pady=50)
        popup1.mainloop()

    master1 = Tk()
    label1 = Label(master1, text="Enter No.of Students", fg="purple")
    label1.config(font=("Helvetica", 17))
    label1.grid(row=0, column=0, sticky=N + E + S + W)

    entry1_field = Entry(master1)
    entry1_field.config(font=("Helvetica", 17))
    entry1_field.grid(row=0, column=1, sticky=N + E + S + W)

    entry1_field.focus_set()

    entry1_button = Button(master1,
                           text="Confirm",
                           bg="green",
                           fg="yellow",
                           command=confirm)
    entry1_button.config(font=("Helvetica", 17))
    entry1_button.grid(row=1, column=1, sticky=N + E + S + W)

    wait_label1 = Label(
        master1,
        text="Please wait for some minutes a popup will appear after processing is finished"
    )
    wait_label1.config(font=("Helvetica", 14))
    wait_label1.grid(row=2, column=0, columnspan=2, sticky=N + E + S + W)

    master1.mainloop()


# instruction_frame = Frame(myApp)
# instruction_frame.pack(fill=BOTH, expand=1)


def showInstructions():
    webbrowser.open("instructions.txt")


# firstFrame = Frame(myApp)
# firstFrame.pack(fill=BOTH, expand=1)

# secondFrame = Frame(myApp)
# secondFrame.pack(fill=BOTH, expand=1)

# for x in range(3):
#     Grid.columnconfigure(firstFrame, x, weight=1)

# for y in range(3):
#     Grid.rowconfigure(firstFrame, y, weight=1)

# for x in range(3):
#     Grid.columnconfigure(secondFrame, x, weight=1)

# for y in range(3):
#     Grid.rowconfigure(secondFrame, y, weight=1)

# for x in range(3):
#     Grid.columnconfigure(instruction_frame, x, weight=1)

# for y in range(3):
#     Grid.rowconfigure(instruction_frame, y, weight=1)

# instr_button = Button(instruction_frame,
#                       text="Instructions",
#                       width=15,
#                       height=10,
#                       fg="purple",
#                       bg="yellow",
#                       command=showInstructions)
# instr_button.config(font=("Helvetica", 17))
# instr_button.grid(row=0, column=0, sticky=N + E + S + W)

# quit_button = Button(instruction_frame,
#                      text="Quit",
#                      width=15,
#                      height=10,
#                      fg="purple",
#                      bg="yellow",
#                      command=window_for_exit)
# quit_button.config(font=("Helvetica", 17))
# quit_button.grid(row=0, column=1, sticky=N + E + S + W)

# button1 = Button(firstFrame,
#                  text="Model Answers",
#                  width=15,
#                  height=10,
#                  fg="purple",
#                  bg="yellow",
#                  command=window_for_no_of_questions)
# button1.config(font=("Helvetica", 17))
# button1.grid(row=1, column=0, sticky=N + E + S + W)

# button2 = Button(firstFrame,
#                  text="Students' Answers",
#                  width=15,
#                  height=10,
#                  fg="purple",
#                  bg="yellow",
#                  command=window_for_no_of_students)
# button2.config(font=("Helvetica", 17))
# button2.grid(row=1, column=1, sticky=N + E + S + W)

# button3 = Button(secondFrame,
#                  text="Evaluate",
#                  width=15,
#                  height=10,
#                  fg="purple",
#                  bg="yellow",
#                  command=window_for_evaluate)
# button3.config(font=("Helvetica", 17))
# button3.grid(row=2, column=0, sticky=N + E + S + W)

# button4 = Button(secondFrame,
#                  text="Results",
#                  width=15,
#                  height=10,
#                  fg="purple",
#                  bg="yellow",
#                  command=result)
# button4.config(font=("Helvetica", 17))
# button4.grid(row=2, column=1, sticky=N + E + S + W)
# myApp.mainloop()
