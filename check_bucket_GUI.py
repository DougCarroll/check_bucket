from tkinter import *
import regions as REGIONS
import requests
import xml.etree.ElementTree as ET

class CheckList(Frame):
    def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
        Frame.__init__(self, parent)
        self.list = []
        row = 0
        for pick in picks:
            var = IntVar()
            chk = Checkbutton(self, text=pick, variable=var).grid(row=row, sticky=W)
            row = row+1
            self.list.append([var,pick])
    def selected(self):
        sList = []
        for i in range(len(self.list)):
            if self.list[i][0].get() == 1:
                sList.append(self.list[i][1])
        return sList

class SelectedList(Frame):
    def __init__(self, parent=None, items=[], side=LEFT, anchor=W):
        print("SelectedList()")
        print(list(items))
        Frame.__init__(self, parent)
        row = 0
        if len(items) == 0:
            self.selectedItem = Label(self, text="Empty").grid(row=row, sticky=W)
            return
        for item in items:
            print("Suposed to display")
            self.selectedItem = Label(self, text=item).grid(row=row, sticky=W)
            row = row+1

if __name__ == '__main__':
    window = Tk()
    window.title("Check AWS Buckets")

    buckets = CheckList(window, list(REGIONS.endpoint))
    resultsFrame = Frame(window, relief=RAISED, bd=2, height=285, width = 300)
  
    buckets.pack(side=LEFT, fill=Y)
    buckets.config(relief=GROOVE, bd=2)
    resultsFrame.pack(side=LEFT, fill=Y)
    resultsFrame.config(relief=GROOVE, bd=2)

    text_results = Text(master=resultsFrame)
    text_results.grid(row=0, column=1, sticky="nesw")


    entry_bucket = Entry(master=resultsFrame, width=40) 
    label_bucket = Label(master=resultsFrame, text="Search String")
    entry_bucket.insert(0, 'public')
    label_bucket.grid(row=1, column=0, sticky="w")
    entry_bucket.grid(row=1, column=1, sticky="w")

    protocol = 'https://'

    def check():
        for ep in buckets.selected():
            url = protocol + REGIONS.endpoint[ep] + '/' + entry_bucket.get()
            #text_results.insert(END, url + '\n')
            try:
                r = requests.get(url, timeout=(3.05))
            except:
                text_results.insert(END, url + " : Server did not respond " + '\n')
                text_results.update()
                continue

            root = ET.fromstring(r.text)
            if root.tag.__contains__("ListBucketResult"):
                text_results.insert(END, url + ' : ' + code + ' : JACKPOT, give this URL a try!!!' + '\n')
                text_results.update()
                continue
            
            code = root.find("Code").text

            #for child in root:
            if code == "PermanentRedirect":
                redirect = root.find("Endpoint").text
                text_results.insert(END, url + ' : ' + code + ' to ' + redirect + '\n')
                text_results.update()
            else:
                text_results.insert(END, url + ' : ' + code + '\n')
                text_results.update()

    Button(window, text='Check', command=check).pack(side=RIGHT)

    window.mainloop()