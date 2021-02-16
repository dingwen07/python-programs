from wxpy import *
bot = Bot()
# 获取好友
friend = bot.friends().search('extra')[0]
#  注册获得个人的图灵机器人key 填入
tuling = Tuling(api_key='17b9cac64a6f4f77b570f0d6c520deb9')


# 使用图灵机器人自动与指定好友聊天
@bot.register(friend)
def reply_my_friend(msg):
    print(msg)
    tuling.do_reply(msg)


embed()
