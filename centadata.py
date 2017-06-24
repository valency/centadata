import codecs
import getopt
import os
import sys
from time import sleep

import regex
import urllib3

from common import *

http = urllib3.PoolManager()


def show_help():
    print('centadata.py [-h] -m <mode> [-t <list_type> -c <list_code>]')
    print('-h\tHelp')
    print('-m\tCrawling Mode: must be "list"')
    print('-t\tList Type: District type when crawling in list mode, e.g., district17')
    print('-c\tList Code: District code when crawling in list mode, e.g., 101')


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hm:t:c:")
    except getopt.GetoptError:
        show_help()
        sys.exit(2)
    mode = None
    list_type = None
    list_code = None
    for opt, arg in opts:
        if opt == '-h':
            show_help()
            sys.exit()
        elif opt == '-m':
            mode = arg
        elif opt == '-t':
            list_type = arg
        elif opt == '-c':
            list_code = arg
    if mode is not None:
        log('Crawling Mode = ' + mode)
        if mode == 'list' and list_type is not None and list_code is not None:
            log('District Type = ' + list_type)
            log('District Code = ' + list_code)
            list_file_name = 'CENTADATA_' + list_type.upper() + '_' + list_code.upper() + '_' + datetime.now().strftime('%Y%m%d%H%M%S')
            list_file = codecs.open(list_file_name + '.csv', 'w', 'UTF-8')
            list_file.write('id,title,url\n')
            if not os.path.exists(list_file_name + "/"):
                os.makedirs(list_file_name + "/")
            log('Crawling...')
            url = 'http://www1.centadata.com/paddresssearch1.aspx?type=' + list_type + '&code=' + list_code
            log(url)
            response = http.request('GET', url).data.decode('BIG5')
            log('Analyzing...')
            matches = regex.findall(r'var arr.. = Array(.*?);', response, re.DOTALL)
            if len(matches) > 0:
                for match in matches:
                    plist = eval(match)
                    for i in range(0, len(plist)):
                        if i % 3 == 0:
                            pid = plist[i]
                            title = plist[i + 1].replace('?', '')
                            url = plist[i + 2]
                            log(pid + ' / ' + title)
                            trans = detail(url)
                            # Write contents
                            with codecs.open(list_file_name + "/" + title + ".csv", 'w', 'UTF-8') as f:
                                for tran in trans:
                                    f.write(','.join(map(clean, map(str, tran))) + '\n')
                            # Update list
                            list_file.write(pid + ',' + title + ',' + url + '\n')
                            # Cool down
                            sleep(5)
            else:
                log('List is not found, analysis failed.', 'red')
            list_file.close()
            log("Finished.")
        else:
            show_help()
    else:
        show_help()


def detail(url):
    url = 'http://www1.centadata.com/' + url
    try:
        response = http.request('GET', url).data.decode('BIG5')
    except UnicodeDecodeError:
        log('Error while handling response.', 'red')
        return []
    matches = regex.findall(r'<TD class="tdtr1addr">(.*?)</TD><TD class="tdtr1age">(.*?)</TD> <TD class="tdtr1reg">(.*?)</TD><TD class="tdtr1con">(.*?)</TD> <TD class="tdtr1area" style="background-color:#FFEFE5;">(.*?)</TD> <TD class="tdtr1area">(.*?)</TD> <TD class="tdtr1uprice" style="background-color:#FFEFE5;">(.*?)</TD><TD class="tdtr1Guprice">(.*?)</TD><td class="tdtr1ltdayheld.?">(.*?)</td><td class="tdtr1ltperc">(.*?)</td></tr></table></TR>', response)
    if not len(matches) > 0:
        log('Trading history is not found.', 'red')
    return matches


if __name__ == "__main__":
    main(sys.argv[1:])
