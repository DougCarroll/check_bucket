import sys
import getopt
import requests
import regions as regions
import xml.etree.ElementTree as ET

def check_bucket(argv):
    # Default to HTTP if not specified
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

    # Loop through all of the endpoints, and check to see if there is a bucket
    #  with the name passed in as an argument
    rList = []
    for key in regions.endpoint:
        root = ''
        code = ''
        redirect = ''

        url = protocol + regions.endpoint[key] + '/' + bucket
        
        try:
            r = requests.get(url, timeout=5)
        except:
            rList.append(url + " : Server did not respond ")
            continue

        root = ET.fromstring(r.text)
        if root.tag.__contains__("ListBucketResult"):
            rList.append(url + ' : ' + code + ' : JACKPOT, give this URL a try!!!')
            continue
        
        code = root.find("Code").text

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
