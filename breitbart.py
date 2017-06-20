import getopt
import os
import sys
import urllib2
from time import sleep

from common import *


def main(argv):
    usage = 'breitbart.py -p <pages> -b <start-page> -s <section,e.g.,big-government>'
    pages = 1
    start_page = 1
    segment = "big-government"
    try:
        opts, args = getopt.getopt(argv, "hp:s:b:")
    except getopt.GetoptError:
        print usage
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print usage
            sys.exit()
        elif opt == '-p':
            pages = int(arg)
        elif opt == '-b':
            start_page = int(arg)
        elif opt == '-s':
            segment = arg
    log("# of Pages = " + str(pages))
    log("Start at Page = " + str(start_page))
    log("Segment = " + segment)
    list_file_name = "BREITBART_" + datetime.now().strftime('%Y%m%d%H%M%S')
    list_file = open(list_file_name + ".csv", "w")
    list_file.write("id,title,time,topics,url\n")
    if not os.path.exists(list_file_name + "/"):
        os.makedirs(list_file_name + "/")
    for page in range(start_page, start_page + pages):
        url = "http://www.breitbart.com/" + segment + "/page/" + str(page) + "/"
        log(url)
        response = urllib2.urlopen(url).read()
        matches = re.findall(r'<a href="/' + segment + '/(.*?)" title="(.*?)" class="thumb-container"', response)
        aid = 0
        for match in matches:
            title = match[1]
            log(title)
            url, time, content, topics = article(segment + "/" + match[0])
            file_name = "P" + str(page).zfill(3) + "A" + str(aid).zfill(3)
            aid += 1
            # Write contents
            with open(list_file_name + "/" + file_name + ".txt", 'w') as f:
                f.write(content)
            # Update list
            list_file.write('"' + file_name + '","' + title + '","' + time + '","' + ";".join(topics) + '","' + url + '"\n')
            # Cool down
            sleep(3)
    list_file.close()
    log("Finished.")


def article(url):
    url = "http://www.breitbart.com/" + url
    log(url)
    response = urllib2.urlopen(url).read()
    match = re.search(r'<div class="entry-content">(.*?)<footer class="articlefooter">', response, re.DOTALL)
    content = clean(match.group(1))
    match = re.search(r'<h3>Read More Stories About:</h3>(.*?)</aside>', response, re.DOTALL)
    topics = [x.strip() for x in clean(match.group(1)).split(",")]
    match = re.search(r'<time class="op-modified H" datetime="(.*?)">(.*?)</time>', response)
    time = match.group(1)
    return url, time, content, topics


if __name__ == "__main__":
    main(sys.argv[1:])
