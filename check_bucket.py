
import sys
import getopt
import requests
import regions as cfg
import xml.etree.ElementTree as ET

# Test Commit

def check_bucket(argv):
    protocol = 'http://'

    try:
        opts, arg = getopt.getopt(argv, "hu:s:")
        if len(arg) == 1:
            bucket = arg[0]
        elif len(sys.argv) == 1:
            print(sys.argv[0] + ' [-s,-u] <search_string>')
            sys.exit(2)
    except getopt.GetoptError:
        print(sys.argv[0] + ' [-s, -u] <search_string>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print(sys.argv[0] + ' [-s,  -u] <search_string>')
            sys.exit(1)
        if opt == '-u':
            print('http selected')
            protocol = 'http://'
            bucket = arg
        elif opt == '-s':
            print('https selected')
            protocol = 'https://'
            bucket = arg

    rList = []

    for key in cfg.endpoint:
        root = ''
        code = ''
        redirect = ''

        url = protocol + cfg.endpoint[key] + '/' + bucket
        
        try:
            r = requests.get(url, timeout=(3.05))
        except:
            rList.append(url + " : Server did not respond ")
            continue

        #print(cfg.endpoint["US_EAST_1"])

        root = ET.fromstring(r.text)
        if root.tag.__contains__("ListBucketResult"):
            rList.append(url + ' : ' + code + ' : JACKPOT, give this URL a try!!!')
            continue
        
        code = root.find("Code").text

        #for child in root:
        #    print(child.tag, child.attrib, child.text)
        if code == "PermanentRedirect":
            redirect = root.find("Endpoint").text
            rList.append(url + ' : ' + code + ' to ' + redirect)
        else:
            rList.append(url + ' : ' + code)

    return rList

if __name__ == "__main__":
    results = check_bucket(sys.argv[1:])
    for i in results:
        print(i)
