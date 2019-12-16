#!/usr/bin/env python
import random
from tkinter.ttk import *

from ImageLoader import *
from RequestMaker import *
from SheetsCredCreator import getSheetsService

words = []
count = 1


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
    newButton = Button(root, text="Create Sheet", command=lambda: newSheet(nameEntry, root))
    newButton.grid(row=1, column=1, sticky=W, pady=20)
    root.mainloop()


def newSheet(entry, prevMaster):
    if entry.get() != "":
        sheetname = entry.get()
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
        imagesize = numwords * 2
        init(imagesize)

        sheet = service.spreadsheets()
        values = service.spreadsheets().values()
        requests = []
        valrequests = []
        # Merging the left hand cells into 2x2s
        requests.append(get_col_resize_request(50))
        requests.append(get_row_resize_request(50))
        for i in range(numwords):
            requests.append(get_merge_request(0, 2, i * 2, i * 2 + 2))
            requests.append(get_merge_request(2, 4, i * 2, i * 2 + 2))
            valrequests.append(write_words_request(words[i], 2 * (i + 1)))

        for x in range(imagesize):
            for y in range(imagesize):
                question_row = (random.randint(0, 9) * y + random.randint(0, 9) * x + random.randint(0, 9)) % numwords
                color = get_color_at_pos(x, y)
                answer = words[question_row]
                requests.append(get_format_request(x, y, color, 2 * question_row, answer))

        writebody = {"valueInputOption": "USER_ENTERED", "data": [valrequests]}
        values.batchUpdate(spreadsheetId=spreadsheetID, body=writebody).execute()
        body = {'requests': requests}
        sheet.batchUpdate(spreadsheetId=spreadsheetID, body=body).execute()

        # print("done?")
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
