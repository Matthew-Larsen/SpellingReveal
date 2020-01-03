#!/usr/bin/env python3
import random
from tkinter.ttk import *

from SpellingReveal.ImageLoader import *
from SpellingReveal.RequestMaker import *
from SpellingReveal.SheetsCredCreator import getSheetsService

words = []
count = 1


# PROMPTSIZE = 75
# PIXELSIZE = 15
# PIXELSPERPROMT = int(PROMPTSIZE / PIXELSIZE)


def main():
    # make the base bui, first ask for sheet name
    # Then for both go ot next screen
    # ask for words maybe have it so they click add more and
    # adds another fill in blank box and somewhere to add a picture
    # Then ask for solution picture
    # Finally say it works and just wait to be closed.

    root = Tk()

    Label(root, text="Sheet Name").grid(row=0, column=0, pady=30, padx=10)
    nameEntry = Entry(root)
    nameEntry.grid(row=0, column=1, padx=10)

    Label(master=root, text="Size of each \"pixel\"  in pixels").grid(row=1, column=0)
    pixelScale = Scale(master=root, from_=1, to_=50, orient=HORIZONTAL, resolution=5)
    pixelScale.grid(row=1, column=1)
    Label(master=root, text="Size of each question block in pixels").grid(row=2, column=0)
    promptScale = Scale(master=root, from_=1, to_=100, orient=HORIZONTAL, resolution=5)
    promptScale.grid(row=2, column=1)

    pixelScale.set(15)
    promptScale.set(60)

    newButton = Button(root, text="Create Sheet", command=lambda: newSheet(nameEntry, pixelScale, promptScale, root))
    newButton.grid(row=3, column=1, sticky=W, pady=20)
    root.mainloop()


def newSheet(entry, pixelScale, promptScale, prevMaster):
    if entry.get() != "":
        sheetname = entry.get()
        PIXELSIZE = pixelScale.get()
        PROMPTSIZE = promptScale.get()
        PIXELSPERPROMT = int(PROMPTSIZE / PIXELSIZE)
        prevMaster.destroy()

        service = getSheetsService()
        spreadsheet = service.spreadsheets().create(body=get_create_request(sheetname),
                                                    fields='spreadsheetId').execute()
        spreadsheetID = spreadsheet.get('spreadsheetId')

        root = Tk()
        get_names_window(root)

        while len(words) == 0:
            pass

        numwords = len(words)
        imagesize = numwords * PIXELSPERPROMT
        init(imagesize)

        sheet = service.spreadsheets()
        values = service.spreadsheets().values()
        requests = []
        valrequests = []

        requests.append(get_col_resize_request(PIXELSIZE))
        requests.append(get_row_resize_request(PIXELSIZE))

        if numwords * PIXELSPERPROMT > 26:
            requests.append(get_additional_col_request((numwords + 2) * PIXELSPERPROMT - 26))

        for i in range(numwords):
            requests.append(get_merge_request(0, PIXELSPERPROMT, i * PIXELSPERPROMT, (i + 1) * PIXELSPERPROMT))
            requests.append(
                get_merge_request(PIXELSPERPROMT, 2 * PIXELSPERPROMT, i * PIXELSPERPROMT, (i + 1) * PIXELSPERPROMT))
            valrequests.append(write_words_request(words[i], PIXELSPERPROMT, PIXELSPERPROMT * (i + 1)))

        print("SENDING VALUES REQUEST")
        values.batchUpdate(spreadsheetId=spreadsheetID,
                           body={"valueInputOption": "USER_ENTERED", "data": [valrequests]}).execute()

        print("SENDING SETUP REQUEST")
        sheet.batchUpdate(spreadsheetId=spreadsheetID, body={'requests': requests}).execute()

        thisrequest = []
        for x in range(imagesize):
            for y in range(imagesize):
                question_row = random.randint(0, 100000) % numwords
                color = get_color_at_pos(x, y)
                answer = words[question_row]
                thisrequest.append(
                    get_format_request(x, y, color, PIXELSPERPROMT * question_row, answer, PIXELSPERPROMT))
            if x % 3 == 0:
                print("SENDING ROW REQUEST: rows ", x, "-", x + 3)
                sheet.batchUpdate(spreadsheetId=spreadsheetID, body={'requests': thisrequest}).execute()
                thisrequest = []

        if thisrequest:
            sheet.batchUpdate(spreadsheetId=spreadsheetID, body={'requests': thisrequest}).execute()

        # writebody = {"valueInputOption": "USER_ENTERED", "data": [valrequests]}
        # values.batchUpdate(spreadsheetId=spreadsheetID, body=writebody).execute()

        # body = {'requests': requests}
        #
        # print("SENDING REQUEST")
        # sheet.batchUpdate(spreadsheetId=spreadsheetID, body=body).execute()

        root2 = Tk()
        Label(root2, text="You're all done").pack()
        root2.mainloop()


def get_names_window(root):
    global count
    count = 0
    Label(root, text="Enter the words they should write").grid(row=0, padx=20)
    Button(root, text="Add Another Word", command=lambda: addField(root)).grid(row=1)
    Button(root, text="Finished?", command=lambda: finishWords(root)).grid(row=1, column=1)
    entry1 = Entry(root)
    Label(root, text="1").grid(row=2, column=0)
    entry1.grid(row=2, column=1)
    count = count + 1
    root.mainloop()


def addField(master):
    global count
    Label(master, text=str(count + 1)).grid(row=2 + count, column=0)
    entry = Entry(master)
    entry.grid(row=2 + count, column=1)
    count = count + 1


def finishWords(master):
    global words
    words = []
    thesewords = []
    children = master.winfo_children()
    for child in children:
        if child.winfo_class() == "Entry" and child.get() != "":
            thesewords.append(child.get())
    words = thesewords
    master.destroy()


if __name__ == "__main__":
    main()
