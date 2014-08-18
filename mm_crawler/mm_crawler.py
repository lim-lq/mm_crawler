#coding=utf-8

import re
import os
import time
import signal
import requests
import threading

from Queue import Empty


class MmCrawler(threading.Thread):
    def __init__(self, host, output, ppid, category_url_queue,
                 detail_url_queue, photo_url_queue, limit_queue):
        super(MmCrawler, self).__init__()
        self.host = host
        self.output = output
        self.ppid = ppid

        self.reg_detail_obj = re.compile(r'href="(/mm/.+?)"')
        self.reg_photo_obj = re.compile(r'arrayImg\[0\]="(.+?)"')
        self.reg_next_obj = re.compile(r'上.+?<a href="(.+?)">下一页</a>')

        self.category_url_queue = category_url_queue
        self.detail_url_queue = detail_url_queue
        self.photo_url_queue = photo_url_queue
        self.limit_queue = limit_queue

        self.lock = threading.Lock()

    def run(self):
        while True:
            try:
                try:
                    url = self.category_url_queue.get(timeout=30)
                except Empty:
                    continue
                self.get_detail_urls(url)
                while self.detail_url_queue.qsize():
                    try:
                        detail_url = self.detail_url_queue.get(timeout=30)
                    except Empty:
                        continue
                    if not self.download(detail_url):
                        os.kill(self.ppid, signal.SIGTERM)
            except Exception:
                pass

    def get_detail_urls(self, url):
        if url.startswith('/'):
            url = ''.join([self.host, url])
        try:
            #print "Begin open url '%s' --- %s --- %s" % (url, time.time(), threading.currentThread().name)
            res = requests.get(url)
        except Exception:
            return None
        #print "End open url '%s' --- %s --- %s" % (url, time.time(), threading.currentThread().name)
        detail_urls = self.reg_detail_obj.findall(res.content)
        for url in detail_urls:
            if url.endswith('.html'):
                self.detail_url_queue.put(url)
            else:
                self.category_url_queue.put(url)

    def get_next_url(self, content, pre_url):
        next_url = self.reg_next_obj.findall(content)
        if len(next_url):
            try:
                next_url = ''.join(['/'.join(pre_url.split('/')[:-1]), next_url[0]])
            except TypeError:
                return ""
            return next_url
        else:
            return ''

    def download(self, url):
        if url.startswith('/'):
            url = ''.join([self.host, url])

        while True:
            try:
                res = requests.get(url)
            except Exception:
                break
            if res.status_code != 200:
                break
            photo_url = self.reg_photo_obj.findall(res.content)
            if len(photo_url):
                photo_url = photo_url[0].replace('/big/', '/pic/')
                try:
                    res = requests.get(photo_url)
                except Exception, e:
                    print "Download '%s' failure: %s --- %s" % (photo_url, e, threading.currentThread().name)
                    continue
                self.lock.acquire()
                while True:
                    try:
                        limit, number = self.limit_queue.get(timeout=30)
                        break
                    except Empty:
                        continue
                if limit == number:
                    #self.limit_queue.put((limit, number))
                    return False
                with open("%s/%d.jpg" % (self.output, number + 1), 'w') as fp:
                    fp.write(res.content)
                print "Download '%s' success %d --- %s" % (photo_url, number + 1, threading.currentThread().name)
                number += 1
                self.limit_queue.put((limit, number))
                self.lock.release()
            url = self.get_next_url(res.content, url)
            if not url:
                return True