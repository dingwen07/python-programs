import itchat, time, re
from itchat.content import *
import os


@itchat.msg_register(
    TEXT, isFriendChat=True, isGroupChat=False, isMpChat=False)
def text_reply(msg):
    match = msg['FromUserName'] == username
    if match:
        message = msg['Text']
        if message[:8] == '##CMD##>':
            if message[8:] == 'EXIT':
                itchat.send('WeChat terminal will be terminated...',
                            msg['FromUserName'])
                os._exit(0)
        else:
            itchat.send(os.popen(msg['Text']).read(), msg['FromUserName'])


itchat.auto_login(hotReload=True, enableCmdQR=1)
print(itchat.get_friends(update=True)[0:])
username = input('Input username:')
itchat.run()
