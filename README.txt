mm_crawler
==========
该爬虫功能是下载22mm.cc上的美女图片
命令行-h可以查看程序运行帮助，-n可以指定并发线程数（默认10个），-o可以指定图片存储在哪个目录（默认当前运行目录的pics目录下），-l可以限制爬多少图片就结束（默认不限制）

爬取流程：
    1.以主页url为起始url放入category_url_queue
    2.循环从category_url_queue中取出url打开，正则匹配查找包含/mm/的url
    3.获得的包含/mm/的url有两种，一种是图片类别url，一种是一组图片的url，分别放入category_url_queue和detail_url_queue中
    4.循环从detail_url_queue中取出url，并下载该组图片，每下载一张图片后判断是否达到上限，若有，则发出退出信号量

//run
mm_crawler -l 5 -o /tmp/pics -l 200
