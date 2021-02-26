
import sys
import getopt
import requests
import regions as cfg
import xml.etree.ElementTree as ET

def main(argv):
    try:
        opts, arg = getopt.getopt(argv, "h:")
    except getopt.GetoptError:
        print (sys.argv[0] + ' <search_string>')
        sys.exit(2)
    # If i need to, I can do "for opt, arg in opts"
    for opt in opts:
        if opt == '-h':
            print (sys.argv[0] + ' <search_string>')
            sys.exit(1)
    
    bucket = arg[0]

    for key in cfg.regions:
        root = ''
        code = ''
        redirect = ''

        url = 'http://' + cfg.regions[key] + '/' + bucket

        try:
            r = requests.get(url, timeout=(3.05))
        except:
            print(url + " : Server did not respond ")
            continue

        #print(cfg.regions["US_EAST_1"])

        root = ET.fromstring(r.text)
        if root.tag.__contains__("ListBucketResult"):
            print(url + ' : ' + code + ' : JACKPOT, give this URL a try!!!')
            continue
        

        code = root.find("Code").text

        #for child in root:
        #    print(child.tag, child.attrib, child.text)
        if code == "PermanentRedirect":
            redirect = root.find("Endpoint").text
            print(url + ' : ' + code + ' to ' + redirect)
        else:
            print(url + ' : ' + code)

if __name__ == "__main__":
    main(sys.argv[1:])
