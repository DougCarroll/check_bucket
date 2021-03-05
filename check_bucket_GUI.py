from tkinter import *
import regions as REGIONS
import config as OPTIONS
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

def checkBuckets(protocol):
    def displayResults(path, data, code, status):
        text_results.insert(END, path + ' : ' + code + ' : '+ data + '\n', status)
        text_results.see(END)
        text_results.update()

    for ep in buckets.selected():
        url = protocol + REGIONS.endpoint[ep] + '/' + entry_bucket.get()
        try:
            r = requests.get(url, timeout=(3.05))
        except:
            code = "ERROR"
            displayResults(url, "Server did not respond", code, 'DOWN')
            continue

        root = ET.fromstring(r.text)
        if root.tag.__contains__("ListBucketResult"):
            code = 'JACKPOT'
            displayResults(url, "Give This URL a try!", code, 'SUCCESS')
            continue

        code = root.find("Code").text        
        if code == "PermanentRedirect":
            redirect = root.find("Endpoint").text
            displayResults(url, redirect, code, 'POSSIBLE')
        else:
            displayResults(url, '', code, 'FAIL')

if __name__ == '__main__':
    window = Tk()
    window.title("Check AWS Buckets")

    buckets = CheckList(window, list(REGIONS.endpoint))
    buckets.pack(side=LEFT, fill=Y)
    buckets.config(relief=GROOVE, bd=2)

    options = CheckList(window,list(OPTIONS.protocol))
    options.pack(side=LEFT, fill=Y)
    options.config(relief=GROOVE, bd=2)

    resultsFrame = Frame(window, relief=RAISED, bd=2)
    resultsFrame.pack(side=LEFT, fill=Y)
    resultsFrame.config(relief=GROOVE, bd=2)

    entry_bucket = Entry(master=resultsFrame, width=40) 
    label_bucket = Label(master=resultsFrame, text="Bucket Name To Search For")
    entry_bucket.insert(0, 'public')
    label_bucket.pack(side=TOP, fill=NONE)
    entry_bucket.pack(side=TOP, fill=NONE)

    text_results = Text(master=resultsFrame)
    text_results_sb = Scrollbar(master=resultsFrame, orient="vertical", command=text_results.yview)
    text_results.configure(yscrollcommand=text_results_sb.set)
    text_results_sb.pack(side=RIGHT, fill=Y)
    text_results.pack(side=LEFT, fill=BOTH)
    text_results.tag_config('SUCCESS', background="light grey", foreground="green")
    text_results.tag_config('FAIL', background="light grey", foreground="red")
    text_results.tag_config('POSSIBLE', background="light grey", foreground="yellow")
    text_results.tag_config('DOWN', background="red", foreground="white")

    def check():
        for protocol in options.selected():
            checkBuckets(OPTIONS.protocol[protocol])

    Button(window, text='Check', command=check).pack(side=RIGHT)

    window.mainloop()