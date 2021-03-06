from tkinter import *
import regions as REGIONS
import config as OPTIONS
import requests
import xml.etree.ElementTree as ET

class CheckList(Frame):
    def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
        Frame.__init__(self, parent)
        row = 0
        # When Select All button is selected, all checkboxes are selected
        def selectAllCheckBoxes():
            self.selectAll()
        Button(self, text='ALL', command=selectAllCheckBoxes).grid(row=row, sticky=W)

        # When Clear All button is selected, all checkboxes are deselected
        def clearAllCheckBoxes():
            self.deselectAll()
        Button(self, text='CLR', command=clearAllCheckBoxes).grid(row=row, sticky=E)
        row = row+1

        self.list = []
        self.chk = []
        count = 0
        for pick in picks:
            var = IntVar()
            self.chk.append(Checkbutton(self, text=pick, variable=var))
            self.chk[count].grid(row=row, sticky=W)
            row = row+1
            count= count+1
            self.list.append([var,pick])
    def selected(self):
        sList = []
        for i in range(len(self.list)):
            if self.list[i][0].get() == 1:
                sList.append(self.list[i][1])
        return sList
    def selectAll(self):
        for i in self.chk:
            i.select()
    def deselectAll(self):
        for i in self.chk:
            i.deselect()
def checkBuckets(protocol):
    def displayResults(path, data, code, status):
        text_results.insert(END, path + ' : ' + code + ' : '+ data + '\n', status)
        text_results.see(END)
        text_results.update()
    def displayContents(path):
        text_contents.insert(END, path + '\n')
        text_contents.see(END)
        text_contents.update()

    for ep in endpoints.selected():
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

            # Get the namespace out of the XML 
            # TODO: Messy way to do it, find a better way
            namespace = str(root)
            junk,namespace = namespace.split('{')
            namespace,junk = namespace.split('}')
            namespace = '{' + namespace + '}'

            # Get the contents and display path in Contents Pane
            for contents in root.findall(namespace + 'Contents'):
                displayContents(url + '/' + contents.find(namespace + "Key").text)
            continue

        code = root.find("Code").text        
        if code == "PermanentRedirect":
            redirect = root.find("Endpoint").text
            displayResults(url, redirect, code, 'POSSIBLE')
        else:
            displayResults(url, '', code, 'FAIL')

if __name__ == '__main__':
    #Create the window
    window = Tk()
    window.title("Check AWS Buckets")

    #Get the list of endpoints and create a CheckButton for each one
    #TODO: Add vertical scroll bar
    endpoints = CheckList(window, list(REGIONS.endpoint))
    endpoints.pack(side=LEFT, fill=Y)
    endpoints.config(relief=GROOVE, bd=2)

    #Get the list of options and create a CheckButton for each one
    #For now, this only handling http and https
    options = CheckList(window,list(OPTIONS.protocol))
    options.pack(side=LEFT, fill=Y)
    options.config(relief=GROOVE, bd=2)

    # When Check button is selected, or enter is pressed, check each
    # selected endpoint to see if there is bucket with the specified name
    #  event=None has to be added to handle pressing <Return>, not clicking the button
    def check(event=None):
        for protocol in options.selected():
            checkBuckets(OPTIONS.protocol[protocol])
    Button(window, text='Check', command=check).pack(side=LEFT)
    window.bind('<Return>', check)

    # resultsFrame is for displaying the results of the search/check
    # TODO: Add button to clear text
    resultsFrame = Frame(window, relief=RAISED, bd=2)
    resultsFrame.pack(side=LEFT, fill=BOTH, expand=True)
    resultsFrame.config(relief=GROOVE, bd=2)

    # contentsFrame is for displaying the contents of found bucket
    # TODO: Add button to clear text
    contentsFrame = Frame(window, relief=RAISED, bd=2)
    contentsFrame.pack(side=LEFT, fill=BOTH, expand=True)
    contentsFrame.config(relief=GROOVE, bd=2)

    entry_bucket = Entry(master=resultsFrame, width=40) 
    label_bucket = Label(master=resultsFrame, text="Bucket Name To Check For")
    entry_bucket.insert(0, 'public')
    label_bucket.pack(side=TOP, fill=NONE)
    entry_bucket.pack(side=TOP, fill=NONE)

    text_results = Text(master=resultsFrame, selectbackground="grey", wrap="none")
    text_results_vsb = Scrollbar(master=resultsFrame, orient="vertical", command=text_results.yview)
    text_results_hsb = Scrollbar(master=resultsFrame, orient="horizontal", command=text_results.xview)
    text_results.configure(yscrollcommand=text_results_vsb.set)
    text_results.configure(xscrollcommand=text_results_hsb.set)
    text_results_vsb.pack(side=RIGHT, fill=Y)
    text_results_hsb.pack(side=BOTTOM, fill=X)
    text_results.pack(side=LEFT, fill=BOTH, expand=True)
    text_results.tag_config('SUCCESS', font="bold", foreground="green")
    text_results.tag_config('FAIL', foreground="orange")
    text_results.tag_config('POSSIBLE', foreground="blue")
    text_results.tag_config('DOWN', foreground="red")
    text_results.tag_add('sel', '1.0')

    text_contents = Text(master=contentsFrame, selectbackground="grey", wrap="none")
    text_contents_vsb = Scrollbar(master=contentsFrame, orient="vertical", command=text_contents.yview)
    text_contents_hsb = Scrollbar(master=contentsFrame, orient="horizontal", command=text_contents.xview)
    text_contents.configure(yscrollcommand=text_contents_vsb.set)
    text_contents.configure(xscrollcommand=text_contents_hsb.set)
    text_contents_vsb.pack(side=RIGHT, fill=Y)
    text_contents_hsb.pack(side=BOTTOM, fill=X)
    text_contents.pack(side=LEFT, fill=BOTH, expand=True)
    text_contents.tag_add('sel', '1.0')

    window.mainloop()