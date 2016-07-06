#!/usr/bin/python
import getopt
import sys
import mechanicalsoup

def main(argv):
    houseNumber =''
    postCode =''

    try:
        opts, args = getopt.getopt(argv, "h:p:")
    except getopt.GetoptError:
        print('VDSLChecker.py -h <houseNumber> -p <postCode>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--houseNumber"):
            houseNumber = arg
        elif opt in ("-p", "--postCode"):
            postCode = arg

    browser = mechanicalsoup.Browser()
    #landing page populates some request variables, just need to select the proceed button and submit
    landing_page = browser.get("http://www.dslchecker.bt.com/adsl/ADSLChecker.Address?URL=&SP_NAME=a%20service%20provider&VERSION=41&MS=E&CAP=no&AEA=Y")
    proceed_form = landing_page.soup.select("form")[0]
    details_page = browser.submit(proceed_form,landing_page.url)
    query_form = details_page.soup.select("form")[0]
    query_form.find('input',{'name' :'buildingnumber'})['value'] = houseNumber
    query_form.find('input',{'name' :'PostCode'})['value'] = postCode
    result_page = browser.submit(query_form,details_page.url)
    result_table = result_page.soup.find('table', {'style' : 'border:1px solid black;border-collapse:collapse;'})
    #Nasty query to identify the VSDL Range A (Clean) availability result from the returned table
    result = result_table.select('tr')[2].select('td')[6].select('span')[0].text
    print(result)

if __name__ == "__main__":
   main(sys.argv[1:])