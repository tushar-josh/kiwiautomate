# importing libraries
import time
import math
import csv
import pandas
from selenium import webdriver
from tkinter import *

# Create Window for GUI with size 450 * 380
top = Tk()
top.geometry("450x380")
top.title("KIWI Astra")
top.maxsize(450, 380)
top.minsize(450, 380)

# Set GUI background
C = Canvas(top, bg="blue", height=10, width=20)
filename = PhotoImage(file="C:\\Users\\jtg\\PycharmProjects\\kiwiautomate\\jtg.png")
background_label = Label(top, image=filename)
background_label.place(x=0, y=0, relwidth=0.2, relheight=0.2)

# Define Stringvar to get editbox inputs
driver_var = StringVar()
kiwiid_var = StringVar()
kiwipassword_var = StringVar()
path_var = StringVar()
planURL_var = StringVar()

# Message box to display messages and information about execution
messagelabel = Label(top, text="")


# Function to clean( add / character before newline and double quotes) string
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


# function to read the data from csv and upload it to the kiwi using selenium

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

    # Get elements access for login
    driver.maximize_window()
    driver.get('https://tcms.chqbook.com/accounts/login/')
    driver.find_element_by_xpath("//input[@type=\"text\"]").send_keys(a2)
    driver.find_element_by_xpath("//input[@type=\"password\"]").send_keys(a3)
    driver.find_element_by_xpath("//button[@type=\"submit\"]").click()

    # check for login
    if driver.current_url == "https://tcms.chqbook.com/":
        index = []

        # loop to access every row of the table
        for i in range(len(table)):

            # store the row values and clean them
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

                # check that all the required entry are available
                if crdesc != "Empty data" and crexpected != "Empty data" and crsteps != "Empty data" and \
                        crpri != "Empty data":

                    # access summary and priority element
                    driver.find_element_by_xpath("//input[@id=\"id_summary\"]").send_keys(crmodule + " : " + crdesc)
                    f = driver.find_element_by_xpath('//button[@data-id="id_priority"]')
                    f.click()
                    driver.find_element_by_xpath(
                        '''//span[text()="\n                                ''' + crpri +
                        '''\n                            "]''') \
                        .click()

                    des = ""

                    # combine test steps, test data, test prerequisite, test expected to desc to add it to summary
                    if crpre != "Empty data":
                        des += "**Prerequisite**\\n" + crpre + "\\n\\n"

                    if crsteps != "Empty data":
                        des += "**Test Steps**\\n" + crsteps + "\\n\\n"

                    if crdata != "Empty data":
                        des += "**Test Data**\\n" + crdata + "\\n\\n"

                    if crexpected != "Empty data":
                        des += "**Expected Result**\\n" + crexpected + "\\n\\n"

                    # access editor provided by Codemirror
                    p = driver.find_element_by_xpath("//div[@class=\"CodeMirror cm-s-paper CodeMirror-wrap\"]")
                    driver.execute_script("arguments[0].CodeMirror.setValue(\"" + des + "\");", p)

                    #accessing notes element and adding notes if available
                    if crnotes != "Empty data":
                        driver.find_element_by_xpath('//textarea[@id="id_notes"]').send_keys(crnotes)

                    driver.find_element_by_xpath('//button[@type="submit"]').click()
                # Store index of unsuccessful upload
                else:
                    index.append(i)
            # Store index of unsuccessful upload
            except:
                print(sys.exc_info()[0])
                index.append(i)
        # close driver window after uploading ends
        driver.close()

        # check for unsuccessful entry count
        if len(index) == 0:
            messagelabel["text"] = "All testcases uploaded successfully"
        else:

            # creating csv for unsuccessful data entry
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
                messagelabel["text"] = "Test Cases Uploaded successfully! check folder for unsuccessful upload"
                B["state"] = "normal"
    else:
        messagelabel["text"] = "Error while logging"
        B["state"] = "normal"

# getting all edit box values on GUI
def helloCallBack():
    a1, a2, a3, a4, a5 = driver_var.get(), kiwiid_var.get(), kiwipassword_var.get(), path_var.get(), planURL_var.get()
    if a1 == "" or a2 == "" or a3 == "" or a4 == "" or a5 == "":
        messagelabel["text"] = "Fill all feilds"
    else:
        print(a1, a2, a3, a4, a5)
        B["state"] = "disabled"

        uploadData(a1, a2, a3, a4, a5)

# defining all the elements on the GUI
B = Button(top, text="Upload Data", command=helloCallBack)
driver_url = Label(top, text="Driver URL").place(x=30, y=70)
kiwi_id = Label(top, text="Kiwi User name").place(x=30, y=110)
kiwi_password = Label(top, text="Kiwi Password").place(x=30, y=150)
testcase_file_path = Label(top, text="CSV file Path").place(x=30, y=190)
testplan_URL = Label(top, text="Test Plan URL").place(x=30, y=230)
e1 = Entry(top, textvariable=driver_var, width=40).place(x=150, y=70)
e2 = Entry(top, textvariable=kiwiid_var, width=40).place(x=150, y=110)
e3 = Entry(top, textvariable=kiwipassword_var, width=40).place(x=150, y=150)
e4 = Entry(top, textvariable=path_var, width=40).place(x=150, y=190)
e5 = Entry(top, textvariable=planURL_var, width=40).place(x=150, y=230)

B.place(x=170, y=270)
messagelabel.place(x=10, y=300)

# running the GUI interface
top.mainloop()
