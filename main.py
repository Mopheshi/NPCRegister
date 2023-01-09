import csv
import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.scrolledtext import *

from tkcalendar import DateEntry

# Database
conn = sqlite3.connect("npcregister.db")
c = conn.cursor()


def creatTable():
    c.execute(
        'CREATE TABLE IF NOT EXISTS userdata(firstName TEXT, lastName TEXT, email TEXT, age TEXT, dob TEXT, '
        'address TEXT, phoneNumber REAL)')


def addDetails(firstName, lastName, email, age, dob, address, phoneNumber):
    c.execute('INSERT INTO userdata(firstName, lastName, email, age, dob, address, phoneNumber) VALUES (?,?,?,?,?,?,?)',
              (firstName, lastName, email, age, dob, address, phoneNumber))
    conn.commit()


def viewAllUsers():
    c.execute('SELECT * FROM userdata')
    data = c.fetchall()
    for row in data:
        tree.insert("", tk.END, values=row)


def getSingleUser(firstname):
    c.execute(f'SELECT * FROM userdata WHERE firstName = "{firstname}"')
    # c.execute(f'SELECT * FROM userdata WHERE firstName = "{firstName}"'.format(firstName))
    data = c.fetchall()
    return data


def clearText():
    fName.delete('0', END)
    lName.delete('0', END)
    eMail.delete('0', END)
    age.delete('0', END)
    dob.delete('0', END)
    addre.delete('0', END)
    phone.delete('0', END)


def addData():
    firstname = str(fName.get())
    lastname = str(lName.get())
    mail = str(eMail.get())
    ag = str(age.get())
    date = str(dob.get())
    addr = str(addre.get())
    number = str(phone.get())
    addDetails(firstname, lastname, mail, ag, date, addr, number)
    result = f"First Name:{firstname}, \nLast Name:{lastname}, \nEmail:{mail}, \nAge:{ag}, \nDate of Birth:{date}, " \
             f"\nAddress:{addr}, \nPhone Number:{number} "
    homeDisplay.insert(END, result)
    messagebox.showinfo("Success", "Record added to database successfully!")


def clearDisp():
    homeDisplay.delete("1.0", END)


def searchUser():
    firstname = str(seach.get())
    result = getSingleUser(firstname)
    # c.execute(f'SELECT * FROM userdata WHERE firstName = "{firstName}"')
    # data = c.fetchall()
    # print(data)
    searchDisplay.insert(END, result)


def clearSearch():
    seach.delete("0", END)


def clearResult():
    searchDisplay.delete("1.0", END)


def clearTable():
    tree.delete("1.0", tk.END)


def exportCSV():
    file = str(fileName.get()) + ".csv"
    with open(file, 'w') as f:
        writer = csv.writer(f)
        c.execute('SELECT * FROM userdata')
        data = c.fetchall()
        writer.writerow(['First Name', 'Last Name', 'Email', 'Age', 'Date of Birth', 'Address', 'Phone Number'])
        writer.writerows(data)
        messagebox.showinfo("Success", f"{file} exported successfully!")


def exportExcel():
    pass


# Structure and Layout
window = Tk()
window.title("NPC Register")
window.geometry("1080x500")

style = ttk.Style(window)
style.configure("lefttab.TNotebook", tabposition="wn")

# Tab layout
tabControl = ttk.Notebook(window, style="lefttab.TNotebook")
home = ttk.Frame(tabControl)
view = ttk.Frame(tabControl)
search = ttk.Frame(tabControl)
export = ttk.Frame(tabControl)
about = ttk.Frame(tabControl)

# Add Tabs to Notebook
tabControl.add(home, text=f'{"Home":^20s}')
tabControl.add(view, text=f'{"View":^20s}')
tabControl.add(search, text=f'{"Search":^20s}')
tabControl.add(export, text=f'{"Export":^20s}')
tabControl.add(about, text=f'{"About":^20s}')

tabControl.pack(expand=1, fill="both")

creatTable()

label1 = Label(home, text="NPC Register", padx=5, pady=5)
label1.grid(row=0, column=0)

label2 = Label(view, text="View", padx=5, pady=5)
label2.grid(row=0, column=0)

label3 = Label(search, text="Search", padx=5, pady=5)
label3.grid(row=0, column=0)

label4 = Label(export, text="Export", padx=5, pady=5)
label4.grid(row=0, column=0)

label5 = Label(about, text="About", padx=5, pady=5)
label5.grid(row=0, column=0)

# Home page
fn = Label(home, text="First Name", padx=5, pady=5)
fn.grid(row=1, column=0)
firstName = StringVar()
fName = Entry(home, textvariable=firstName, width=50)
fName.grid(row=1, column=1)

ln = Label(home, text="Last Name", padx=5, pady=5)
ln.grid(row=2, column=0)
lastName = StringVar()
lName = Entry(home, textvariable=lastName, width=50)
lName.grid(row=2, column=1)

em = Label(home, text="Email", padx=5, pady=5)
em.grid(row=3, column=0)
email = StringVar()
eMail = Entry(home, textvariable=email, width=50)
eMail.grid(row=3, column=1)

ag = Label(home, text="Age", padx=5, pady=5)
ag.grid(row=4, column=0)
Age = IntVar()
age = Entry(home, textvariable=Age, width=50)
age.grid(row=4, column=1)

db = Label(home, text="Date of Birth", padx=5, pady=5)
db.grid(row=5, column=0)
DOB = StringVar()
dob = DateEntry(home, textvariable=DOB, background="green", foreground="white", borderwidth=2, year=2010)
dob.grid(row=5, column=1, padx=10, pady=10)

ad = Label(home, text="Address", padx=5, pady=5)
ad.grid(row=6, column=0)
address = StringVar()
addre = Entry(home, textvariable=address, width=50)
addre.grid(row=6, column=1)

pn = Label(home, text="Phone Number", padx=5, pady=5)
pn.grid(row=7, column=0)
phoneNumber = StringVar()
phone = Entry(home, textvariable=phoneNumber, width=50)
phone.grid(row=7, column=1)

add = Button(home, text="Add", width=12, bg="green", fg="white", command=addData)
add.grid(row=8, column=0, padx=5, pady=5)

clear = Button(home, text="Clear", width=12, bg="green", fg="white", command=clearText)
clear.grid(row=8, column=1, padx=5, pady=5)

# Display Screen
homeDisplay = ScrolledText(home, height=10)
homeDisplay.grid(row=9, column=0, padx=5, pady=5, columnspan=3)

clearDisplay = Button(home, text="Clear Submission", width=12, bg="green", fg="white", command=clearDisp)
clearDisplay.grid(row=10, column=1, padx=10, pady=10)

# View page
viewAll = Button(view, text="View All", width=12, bg="green", fg="white", command=viewAllUsers)
viewAll.grid(row=1, column=0, padx=10, pady=10)
tree = ttk.Treeview(view, column=("column1", "column2", "column3", "column4", "column5", "column6", "column7"),
                    show="headings")
tree.heading("#1", text="First Name")
tree.heading("#2", text="Last Name")
tree.heading("#3", text="Email")
tree.heading("#4", text="Age")
tree.heading("#5", text="Date of Birth")
tree.heading("#6", text="Address")
tree.heading("#7", text="Phone Number")
tree.grid(row=10, column=0, columnspan=3, padx=5, pady=5)

clearTree = Button(view, text="Clear Table", width=12, bg="green", fg="white", command=clearTable)
clearTree.grid(row=1, column=1, padx=10, pady=10)

# Search page
sc = Label(search, text="Search by Name", padx=5, pady=5)
sc.grid(row=1, column=0)
searchValue = StringVar()
seach = Entry(search, textvariable=searchValue, width=50)
seach.grid(row=1, column=1)

searchUser = Button(search, text="Search", width=12, bg="green", fg="white", command=searchUser)
searchUser.grid(row=1, column=2, padx=10, pady=10)

clearSearch = Button(search, text="Clear Search", width=12, bg="green", fg="white", command=clearSearch)
clearSearch.grid(row=2, column=1, padx=10, pady=10)

clearResult = Button(search, text="Clear Results", width=12, bg="green", fg="white", command=clearResult)
clearResult.grid(row=2, column=2, padx=10, pady=10)

# Display Screen
searchDisplay = ScrolledText(search, height=10)
# searchDisplay = Listbox(search, width=60, height=5)
searchDisplay.grid(row=10, column=0, padx=5, pady=5, columnspan=3)

# Export page
ex = Label(export, text="File Name", padx=5, pady=5)
ex.grid(row=2, column=0)
filename = StringVar()
fileName = Entry(export, textvariable=filename, width=30)
fileName.grid(row=2, column=1)

toCSV = Button(export, text="Export CSV", width=12, bg="green", fg="white", command=exportCSV)
toCSV.grid(row=3, column=0, padx=10, pady=10)

toExcel = Button(export, text="Export Excel", width=12, bg="green", fg="white", command=exportExcel)
toExcel.grid(row=3, column=1, padx=10, pady=10)

# About page

window.mainloop()
