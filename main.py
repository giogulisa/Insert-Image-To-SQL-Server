from tkinter import *
from tkinter import filedialog
import pyodbc
import os
from datetime import datetime

root = Tk()
root.title("Image Uploader To DB")

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


def folderPath():
    txtFolderPath.delete(0, END)
    txtFolderPath.insert(0, filedialog.askdirectory())


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

def CreateTXTFile(unSuccessfulIdProds, directory):
    try:
        txtFileileName = 'ErrorIdProds.txt'
        newFile= os.path.join(directory,txtFileileName)
        f = open(newFile, 'w+')
        f.write(str(datetime.now()) + ' \n')
        for i in unSuccessfulIdProds:
            f.write(i + "\n")
        f.close()
    except:
        print("ERROR")

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

    unSuccessfulIdProds = []

    # Loop Though Folder To Get All Images
    for filename in os.listdir(directory):

        IdProd = nameTrimer(filename)
        fileDirectory = directory + '/' + filename

        cursor.execute("SELECT Prod From Prod WHERE IdProd = ?", IdProd)

        if len(cursor.fetchall()) > 0:
            for picture in os.listdir(fileDirectory):
                PictureLocation = fileDirectory + '/' + picture
                saveImage(PictureLocation, IdProd, cursor)
        else:
            unSuccessfulIdProds.append(IdProd)

    cnxn.commit()
    laEndNotification = Label(root, text= str(datetime.now()) + " ატვირთვა დასრულდა")
    laEndNotification.pack()
    if len(unSuccessfulIdProds) > 0:
        CreateTXTFile(unSuccessfulIdProds, directory)


# Folder - ის არჩევა
myFButton = Button(root, text="Folder - ის არჩევა", command=folderPath)
myFButton.pack()

# ასატვირთვი ღილაკი
myButton = Button(root, text="ატვირთვა", command=myClick)
myButton.pack()

root.mainloop()