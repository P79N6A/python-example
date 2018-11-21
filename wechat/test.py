#coding=utf8
import random

import thread
import time

print u'\u62bd\u5956\u6709\uff1f'
a=u'@周鹏举句'
print a[2:]

b=u"@周鹏举 到哪里了";
print b[b.find('')+1:]

print random.randint(1, 10)

import threading
import time

exitFlag = 0

USER_DICT={'a':('10',3)}

class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print "Starting " + self.name
        print_time(self.name, self.counter, 5)
        process_notResp();
        print "Exiting " + self.name


def process_notResp():
    while(True):
        print 'for for';
        time.sleep(5);
        global  USER_DICT;
        for k in USER_DICT.keys():
            v=USER_DICT.get(k);
            inst=v[0];
            gmt=v[1];
            nw=time.time();
            print 'see',k,inst,gmt,nw;


class myThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print "Starting " + self.name
        process_notResp();
        print "Exiting " + self.name

def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threading.Thread.exit()
        time.sleep(delay)
        print "%s: %s" % (threadName, time.ctime(time.time()))
        counter -= 1


# 创建新线程
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

# 开启线程
thread1.start()
thread2.start()

print "Exiting Main Thread"