import time
import math
import csv

import pandas
from selenium import webdriver
from tkinter import *


top = Tk()
top.geometry("450x400")
top.title("Aham Brahmasmi")

C = Canvas(top, bg="blue", height=250, width=300)
filename = PhotoImage(file="C:\\Users\\jtg\\Desktop\\bg.png")
background_label = Label(top, image=filename)
background_label.place(x=120, y=120, relwidth=1, relheight=1)

driver_var = StringVar()
kiwiid_var = StringVar()
kiwipassword_var = StringVar()
path_var = StringVar()
planURL_var = StringVar()

messagelabel = Label(top, text="")


def cleanData(f):
    if type(f) == float and math.isnan(f):
        return "Empty data"
    f = str(f)
    t = ""
    for i in range(len(f)):
        if ord(f[i]) == 34:
            t += chr(92) + chr(34)
        elif ord(f[i]) == 10:
            t += "\\n"
        elif ord(f[i]) == 47:
            t += "\\"
        else:
            t += f[i]
    return t


def uploadData(a1, a2, a3, a4, a5):
    driver = webdriver.Chrome(executable_path=a1)

    # read file
    table = pandas.read_csv(a4)

    # Create list of test case description
    testDescription = table['Test case description']

    # Create list of test steps
    testSteps = table['Test Steps']

    # Create list of test prerequisite
    testPrerequisite = table['Prerequisite']

    # Create list of test Data
    testData = table['Test Data']

    # Create list of test Priority
    testPriority = table['Priority']

    # Create list of Expected Result
    testExpectedResult = table['Expected Result']

    # Create list of Notes
    testNotes = table['Notes']

    # Create list of Module
    testModule = table['Module']

    driver.maximize_window()
    driver.get('https://tcms.chqbook.com/accounts/login/')
    driver.find_element_by_xpath("//input[@type=\"text\"]").send_keys(a2)
    driver.find_element_by_xpath("//input[@type=\"password\"]").send_keys(a3)
    driver.find_element_by_xpath("//button[@type=\"submit\"]").click()

    if driver.current_url == "https://tcms.chqbook.com/":

        index = []

        for i in range(len(table)):
            crdesc = testDescription[i]
            crsteps = cleanData(testSteps[i])
            crpre = cleanData(testPrerequisite[i])
            crdata = cleanData(testData[i])
            crpri = cleanData(testPriority[i])
            crexpected = cleanData(testExpectedResult[i])
            crmodule = cleanData(testModule[i])
            crnotes = cleanData(testNotes[i])

            time.sleep(1)

            try:
                driver.get(a5)

                if crdesc != "Empty data" and crexpected != "Empty data" and crsteps != "Empty data" and crpri != "Empty data":
                    driver.find_element_by_xpath("//input[@id=\"id_summary\"]").send_keys(crmodule + " : " + crdesc)
                    f = driver.find_element_by_xpath('//button[@data-id="id_priority"]')
                    f.click()
                    driver.find_element_by_xpath(
                        '''//span[text()="\n                                ''' + crpri +
                        '''\n                            "]''') \
                        .click()

                    des = ""

                    if crpre != "Empty data":
                        des += "**Prerequisite**\\n" + crpre + "\\n\\n"

                    if crsteps != "Empty data":
                        des += "**Test Steps**\\n" + crsteps + "\\n\\n"

                    if crdata != "Empty data":
                        des += "**Test Data**\\n" + crdata + "\\n\\n"

                    if crexpected != "Empty data":
                        des += "**Expected Result**\\n" + crexpected + "\\n\\n"

                    p = driver.find_element_by_xpath("//div[@class=\"CodeMirror cm-s-paper CodeMirror-wrap\"]")
                    driver.execute_script("arguments[0].CodeMirror.setValue(\"" + des + "\");", p)

                    if crnotes != "Empty data":
                        driver.find_element_by_xpath('//textarea[@id="id_notes"]').send_keys(crnotes)

                    driver.find_element_by_xpath('//button[@type="submit"]').click()
                else:
                    index.append(i)
            except:
                print(sys.exc_info()[0])
                index.append(i)

        driver.close()
        if len(index) == 0:
            messagelabel["text"] = "All testcases uploded successfully"
        else:

            header = list(table.columns)
            row = []

            for i in range(len(table)):
                if i in index:
                    row.append(table.iloc[i, :])

            print(row)

            filename = "C:/Users/jtg/Downloads/" + str(time.time()) + "report.csv"

            # writing to csv file
            with open(filename, 'w') as csvfile:
                # creating a csv writer object
                csvwriter = csv.writer(csvfile)

                # writing the fields
                csvwriter.writerow(header)

                # writing the data rows
                csvwriter.writerows(row)
                messagelabel["text"] = "Test Cases Uploaded successfully! check folder for unsuccessfull upload"
                B["state"] = "normal"
    else:
        messagelabel["text"] = "Error while logging"
        B["state"] = "normal"


def helloCallBack():
    a1, a2, a3, a4, a5 = driver_var.get(), kiwiid_var.get(), kiwipassword_var.get(), path_var.get(), planURL_var.get()
    if a1 == "" or a2 == "" or a3 == "" or a4 == "" or a5 == "":
        messagelabel["text"] = "Fill all feilds"
    else:
        print(a1, a2, a3, a4, a5)
        B["state"] = "disabled"

        uploadData(a1, a2, a3, a4, a5)


B = Button(top, text="Upload Data", command=helloCallBack)
driver_url = Label(top, text="Driver URL").place(x=30, y=50)
kiwi_id = Label(top, text="Kiwi User name").place(x=30, y=90)
kiwi_password = Label(top, text="Kiwi Password").place(x=30, y=130)
testcase_file_path = Label(top, text="CSV file Path").place(x=30, y=170)
testplan_URL = Label(top, text="Test Plan URL").place(x=30, y=210)
e1 = Entry(top, textvariable=driver_var).place(x=150, y=50)
e2 = Entry(top, textvariable=kiwiid_var).place(x=150, y=90)
e3 = Entry(top, textvariable=kiwipassword_var).place(x=150, y=130)
e4 = Entry(top, textvariable=path_var).place(x=150, y=170)
e5 = Entry(top, textvariable=planURL_var).place(x=150, y=210)

B.place(x=150, y=250)
messagelabel.place(x=10, y=280)

top.mainloop()
