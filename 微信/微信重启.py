#coding=utf-8
import itchat
from itchat.content import *


groups={}


@itchat.msg_register([TEXT, SHARING], isGroupChat=True)
def group_reply_text(msg):

    source = msg['FromUserName']  # 来自哪一个群信群
    groups[source]=msg['ActualNickName'] # 把群聊的ID和名称加入groups

    print msg['ActualNickName']

    print msg['Content']

    # 处理文本消息
    if msg['Type'] == TEXT:

        for item in groups.keys():

            if not item == source:
                itchat.send('robot --> %s:\n%s' % (msg['ActualNickName'], msg['Content']), item)


    # 处理分享消息
    elif msg['Type'] == SHARING:

        for item in groups.keys():

            if not item == source:
                itchat.send('robot --> %s (share): %s\n%s' % ( msg['ActualNickName'], msg['Text'], msg['Url']), item)

itchat.auto_login()
itchat.run()