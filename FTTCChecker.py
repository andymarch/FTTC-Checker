#!/usr/bin/python
import getopt
import sys
import mechanicalsoup


def main(argv):
    house_number = ''
    post_code = ''

    try:
        opts, args = getopt.getopt(argv, "h:p:")
    except getopt.GetoptError:
        print('FTTCChecker.py -h <houseNumber> -p <postCode>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--houseNumber"):
            house_number = arg
        elif opt in ("-p", "--postCode"):
            post_code = arg

    browser = mechanicalsoup.Browser()
    # landing page populates some request variables, just need to select the proceed button and submit
    landing_page = browser.get("https://www.dslchecker.bt.com/#")
    proceed_form = landing_page.soup.select("form")[3]
    warning_page = browser.submit(proceed_form, landing_page.url)
    warning_form = warning_page.soup.select("form")[0]
    query_submit = browser.submit(warning_form, warning_page.url)
    query_form = query_submit.soup.select("form")[0]
    query_form.find('input', {'name': 'buildingnumber'})['value'] = house_number
    query_form.find('input', {'name': 'PostCode'})['value'] = post_code
    result_page = browser.submit(query_form, query_submit.url)
    result_table = result_page.soup.find('table', {'style': 'border:1px solid black;border-collapse:collapse;'})
    # # Nasty query to identify the VSDL Range A (Clean) availability result from the returned table
    clean_result = result_table.select('tr')[2].select('td')[6].select('span')[0].text
#     impacted_result = result_table.select('tr')[3].select('td')[6].select('span')[0].text
    print(clean_result)
#     print(impacted_result)


if __name__ == "__main__":
    main(sys.argv[1:])
