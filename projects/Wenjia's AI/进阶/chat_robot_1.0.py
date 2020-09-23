
import asyncio
import time
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

###########
import itchat  #微信网页登陆，但是现在容易被封号

itchat.auto_login()  #连接微信号

itchat.send('这是一个测试', toUserName='filehelper')#发送内容
################



bot = ChatBot(
    "Godness",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database_uri="sqlite:///database.sqlite3",
)


godness_throne_trainer = ListTrainer(bot)
godness_throne_trainer.train(["干嘛", "睡觉", "去洗澡"])

channel_input_to_think = []
another_channel_input_to_think = []
channel_think_to_output = []
running = True


@itchat.msg_register(itchat.content.TEXT, isFriendChat=True)
def some_one_say_something(msg):
    if msg["FromUserName"] == "newsapp":
        return
    channel_input_to_think.append(msg)


async def another_input_system():
    while running:
        localtime = time.localtime(time.time())
        another_channel_input_to_think.append(localtime)
        await asyncio.sleep(1)
    return


async def think_system():
    while running:
        if (
            len(channel_input_to_think) == 0
            and len(another_channel_input_to_think) == 0
        ):
            await asyncio.sleep(1)
        else:
            think()
    return


async def output_system():
    while running:
        if len(channel_think_to_output) == 0:
            await asyncio.sleep(1)
        else:
            output()
    return


def think():
    while len(channel_input_to_think) > 0:
        msg = channel_input_to_think.pop()
        if msg["Type"] == itchat.content.TEXT:
            friend = itchat.search_friends(userName=msg["FromUserName"])
            if friend == "圣斗士":
                reply = bot.get_response(msg["Text"])
                channel_think_to_output.append(
                    {"action": "send_text", "to": msg["FromUserName"], "content": reply}
                )

    while len(another_channel_input_to_think) > 0:
        local_time = another_channel_input_to_think.pop()
        if (
            local_time.tm_hour == 21
            and local_time.tm_minute == 0
            and local_time.tm_second == 0
        ):
            toUserNameList = itchat.search_friends(remarkName="圣斗士")
            for name in toUserNameList:
                channel_think_to_output.append(
                    {"action": "send_text", "to": name, "content": "好好睡，晚安"}
                )
        pass

    return


def output():
    while len(channel_think_to_output) > 0:
        event = channel_think_to_output.pop()
        if event["action"] == "send_text":
            to = event["to"]
            content = event["content"]
            itchat.send_msg(msg=content, toUserName=to)
            pass
    return


if __name__ == "__main__":
    # 启动itchat并且登录
    itchat.auto_login(hotReload=True)
    itchat.run(blockThread=False)

    # 启动系统循环
    loop = asyncio.get_event_loop()
    system_list = [another_input_system(), output_system(), think_system()]
    loop.run_until_complete(asyncio.wait(system_list))