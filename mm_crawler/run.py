#!/usr/bin/env python
#coding=utf-8

import os
import time
import signal
import argparse
from Queue import Queue
from mm_crawler import MmCrawler

category_url_queue = Queue()
detail_url_queue = Queue()
photo_url_queue = Queue()
limit_queue = Queue()
host = "http://www.22mm.cc"
category_url_queue.put(host)
state = True


def exit_crawler(*args):
    global state
    state = False

signal.signal(signal.SIGTERM, exit_crawler)


def main():
    host = "http://www.22mm.cc"
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--number', help="the number of thread default 10", type=int, default=10)
    parser.add_argument('-o', '--output', help="the output directory default current directory", default="./pics")
    parser.add_argument("-l", '--limit', help="limit of photo number crawled default ulimit", type=int, default=-1)

    args = parser.parse_args()
    limit_queue.put((args.limit, 0))
    pid = os.getpid()

    if not os.path.exists(args.output):
        os.makedirs(args.output)
    start_time = time.time()
    crawlers = [MmCrawler(host, args.output, pid, category_url_queue, detail_url_queue,photo_url_queue, limit_queue)
                for _i in xrange(args.number)]
    for crawler in crawlers:
        crawler.daemon = True
        crawler.start()
    while state:
        time.sleep(3600)
    end_time = time.time()
    print "Spend time %s sec" % (end_time - start_time)

if __name__ == "__main__":
    main()