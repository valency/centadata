import getopt
import sys
import urllib2
from collections import Counter
from os import listdir
from os.path import isfile, join

from common import *


def main(argv):
    usage = 'wordcount.py -d <directory>'
    article_dir = None
    try:
        opts, args = getopt.getopt(argv, "hd:")
    except getopt.GetoptError:
        print usage
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print usage
            sys.exit()
        elif opt == '-d':
            article_dir = arg
    if article_dir is None:
        print usage
        sys.exit(2)
    log(article_dir)
    log("Loading data...")
    article_words = dict()
    for f in listdir(article_dir):
        filename = join(article_dir, f)
        if isfile(filename):
            # log(f)
            with open(filename, 'r') as article_file:
                article_words[f] = Counter(extract_words(article_file.read().lower()).split())
    log("Aggregating...")
    word_list = set()
    for item in article_words.values():
        for entity in item.items():
            if entity[1] >= 2: word_list.add(entity[0])
            # word_list = word_list.union(item.keys())
    word_list = list(word_list)
    log("# of Words = " + str(len(word_list)))
    with open(article_dir + ".words.txt", "w") as f:
        f.write("\n".join(word_list))
    with open(article_dir + ".mat.csv", "w") as f:
        for item in article_words.items():
            f.write(item[0])
            for word in word_list:
                if word in item[1]:
                    f.write("," + str(item[1][word]))
                else:
                    f.write(",0")
            f.write("\n")
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
