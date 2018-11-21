# coding=utf8
import requests
import itchat
import time
import random
import threading

KEY = '80dccee6a96d48949f267122f8d64dc5'
SWITCH = False;
SWITCHGROUP = False;
USER_DICT = {};

newInstance = itchat.new_instance();


def get_response(msg):
    # 这里我们就像在“3. 实现最简单的与图灵机器人的交互”中做的一样
    # 构造了要发送给服务器的数据
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': KEY,
        'info': msg,
        'userid': 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
        return r.get('text')
    # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        # 将会返回一个None
        return


@newInstance.msg_register(itchat.content.PICTURE, isFriendChat=True)
def picture_reply(msg):
    newInstance.send(u'[好]', msg.FromUserName)


@newInstance.msg_register(itchat.content.RECORDING, isFriendChat=True)
def picture_reply(msg):
    a = random.randint(1, 10)
    if (a % 2 == 3):
        return u'噪音太大听不清，发文字吧哈';


# 带对象参数注册，对应消息对象将调用该方法
@newInstance.msg_register(itchat.content.TEXT, isFriendChat=True)
def text_reply_contact(msg):
    print 'to:' + msg.ToUserName;
    print 'from:' + msg.FromUserName;

    # print 'ctx:' + msg.Content;
    # print 'text:' + msg.Text;
    # print 'switch:' + str(SWITCH);
    if (msg.ToUserName == msg.FromUserName or 'filehelper' == msg.ToUserName):
        if (msg.Content == u'开启' or
                    msg.Content == u'出来' or
                    msg.Content == u'开始'):
            global SWITCH
            SWITCH = True;
            newInstance.send(u'C机器人已经出来接客了', 'filehelper')
            return
        if (msg.Content == u'关闭' or
                    msg.Content == u'滚蛋' or
                    msg.Content == u'结束'):
            global SWITCH
            SWITCH = False;
            newInstance.send(u'C机器人已经关闭啦', 'filehelper')
        if (msg.Content == u'开启群'):
            global SWITCHGROUP
            SWITCHGROUP = True;
            newInstance.send(u'G机器人已经出来接客了', 'filehelper')
            return
        if (msg.Content == u'关闭群'):
            global SWITCHGROUP
            SWITCHGROUP = False;
            newInstance.send(u'G机器人已经关闭啦', 'filehelper')
    elif (SWITCH):
        if (msg.Text.startswith('[')):
            newInstance.send(msg.Text, msg.FromUserName)
        else:
            reply = get_response(msg.Text);
            a = random.randint(1, 5)
            # print 'time=',a
            time.sleep(a)
            newInstance.send(reply, msg.FromUserName)
            if (a % 2 == 1):
                newInstance.send(reply, msg.FromUserName)
            global USER_LIST;
            USER_DICT[msg.FromUserName] = [ time.time(), 0];
    # print msg;
    defaultReply = u"你在说什么嘛";


# 带对象参数注册，对应消息对象将调用该方法
@newInstance.msg_register(itchat.content.TEXT, isGroupChat=True)
def text_reply_group(msg):
    global SWITCHGROUP
    print 'to:' + msg.ToUserName;
    print 'from:' + msg.FromUserName;
    # print 'ctx:' + msg.Content;
    # print 'text:' + msg.Text;
    # print 'switchgroup:'+ str(SWITCHGROUP);
    if (SWITCHGROUP):
        if (msg.isAt):
            reply = get_response(msg.Text[msg.Text.find(' ') + 1:])
            msg.user.send(reply);


# 自动回复，如果和你聊天的人，2分钟内不回复你，可以主动发送3次信息来挑动她或他
class autoRespThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def auto_talking(self):
        while (True):
            time.sleep(30);
            global USER_DICT;
            for userName in USER_DICT.keys():
                v = USER_DICT.get(userName);
                lastTalkTime = v[0];
                autoSendCount = v[1];
                currentTime = time.time();
                # 大于2分钟未回复，且撩动次数小于3次，则主动发信息
                if (currentTime - lastTalkTime >= 120 and autoSendCount < 3):
                    v[1] += 1;
                    global newInstance
                    newInstance.send(u"忙什么呢，聊会儿呗", userName);
                if(autoSendCount==3):
                    del USER_DICT[userName];  # 删除条目

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print "Starting auto talking " + self.name
        self.auto_talking();
        print "Exiting auto talking" + self.name


if (__name__ == '__main__'):
    try:
        thread1 = autoRespThread(1, "autoRespThread-monitor", 1)
        thread1.start();
    except Exception:
        print "Error: unable to start autoRespThread"

    # 为了让实验过程更加方便（修改程序不用多次扫码），我们使用热启动
    newInstance.auto_login(hotReload=True, enableCmdQR=-2, statusStorageDir='newInstance.pkl');
    newInstance.run(True)
