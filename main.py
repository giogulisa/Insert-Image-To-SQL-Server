from tkinter import *
import pyodbc
import os

root = Tk()

# SQL Server Name Input
laServerName = Label(root, text="სერვერის დასახელება")
laServerName.pack()

txtServerName = Entry(root, width=50, borderwidth=5)
txtServerName.pack()

# DB Name Input
laDBName = Label(root, text="ბაზის დასახელება")
laDBName.pack()

txtDBName = Entry(root, width=50, borderwidth=5)
txtDBName.pack()

# User Input
laUN = Label(root, text="მომხმარებლის სახელი")
laUN.pack()

txtUN = Entry(root, width=50, borderwidth=5)
txtUN.pack()

# User Password Input
laUNPassword = Label(root, text="მომხმარებლის პაროლი")
laUNPassword.pack()

txtUNPassword = Entry(root, width=50, borderwidth=5)
txtUNPassword.pack()

# FolderPath
laFolderPath = Label(root, text="ფაილის მისამართი")
laFolderPath.pack()

txtFolderPath = Entry(root, width=50, borderwidth=5)
txtFolderPath.pack()


# Trimming IdProd From FileName
def nameTrimer(fileName):
    trimPosition = fileName.find('#', 0)
    trimmedFileName = fileName[:trimPosition]
    return trimmedFileName


# Saveing TO DB
def saveImage(PictureLocation, IdProd, cursor):
    with open(PictureLocation, 'rb') as f:
        bindata = f.read()

        strcomm = "insert into ProdPicture (ProdPicture, Idprod) values (?,?) "

        cursor.execute(strcomm, (bindata, IdProd))


def myClick():
    # Connection String
    server = txtServerName.get()
    database = txtDBName.get()
    username = txtUN.get()
    password = txtUNPassword.get()

    cnxn = pyodbc.connect(
        'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor = cnxn.cursor()

    # Folder Path
    directory = str(txtFolderPath.get())

    # Loop Though Folder To Get All Images
    for filename in os.listdir(directory):

        IdProd = nameTrimer(filename)
        filedirectory = directory + '/' + filename

        for picture in os.listdir(filedirectory):
            PictureLocation = filedirectory + '/' + picture
            saveImage(PictureLocation, IdProd, cursor)

    cnxn.commit()
    laEndNotification = Label(root, text="ატვირთვა დასრულდა")
    laEndNotification.pack()


# ასატვირთვი ღილაკი
myButton = Button(root, text="ატვირთვა", command=myClick)
myButton.pack()

root.mainloop()
