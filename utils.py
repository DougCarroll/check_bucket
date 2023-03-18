# Takes a list as an argument, and returns an HTML table
def toHTMLTable(l):
    s = '<table>'
    for i in l:
        s = s + '<tr><td>' + i + '</tr></td>'
    s = s + '</table>'
    return s

# Takes the list of results, and changes URL text to Link
def toLink(l):
    newList = []
    for i in l:
        j = i.split(" : ")
        j[0] = "<a href=\"" + j[0] + "\">" + j[0] + "</a>"
        if len(j) == 2:
            newList.append(j[0] + " : " + j[1])     
        elif len(j) == 3:   
            newList.append(j[0] + " : " + j[1] + " : " + j[2])
        else:        
            newList.append(j[0])     
    return newList