import discord
import asyncio
from compe_manager import Compe_manager
#import db #これからdbモジュールを書く

class MyClient(discord.Client):
    """
    on_~~~系の関数か、他の自作関数(例:regular_check)でキャッチすべきイベントを決める。
    キャッチしたら処理対象をそのままhub関数に投げることでbot.pyをシンプルに保つ。
    全ての大会(全てのチャンネル)を1つのbotで処理するので、キャッチするイベントはそれらの和集合になるように。
    ある大会に限定的かもしれない条件(...は大会に関係ないので無視する等)をここに書いてしまうと後々困りうるので注意。
    """

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        for guild in self.guilds: #所属guildは1つだけのはず
            for member in guild.members:
                compe_mgr.uids.append(member.id)
                # print(member.id, member.name)ユーザーID一覧は以下の通り
                # 429652694987178002 牛乳
                # 504114263070212097 nadchu
                # 599810351319482370 IR_Rating
            for channel in guild.channels: #全所属チャンネルについて処理
                compe_mgr.init_compedata(channel.id) #IRのデータを持つクラスをインスタンス化
                # print(channel.id,channel.name) #チャンネルID一覧は以下の通り
                # 599809803191058444 テキストチャンネル
                # 599809803191058445 一般
                # 599809803191058447 voice
                # 599858689368653825 test
                # 602690045044064297 gspreadサンプル
                # 602733557189836803 ir_admin
                # 602776246673473565 make_test
                # 603398450352226306 シート1
                # 633598972510076938 nadchu_test
        #asyncio.ensure_future(self.regular_check(60)) #定期実行タスクはバグっているので後で直す

    async def on_message(self, message):
        if   message.content.startswith("kill"): #debug botを停止
            #用例 "kill"
            await self.logout()
            return
        elif message.content.startswith("globals"): #debug global変数全てをprint
            #用例 "globals"
            for k, v in globals().items():
                print(k,":",v)
        elif message.content.startswith("exec"): #debug 任意コードの実行
            #用例 "exec print("Hello world!")"
            if len(message.content)>=5:
                toexec=message.content[5:]
                print(f"> exec({toexec})")
                exec(toexec)
        elif message.content.startswith("print"): #debug 変数名等を指定してprint
            #用例 "print compe_mgr.uids"
            if len(message.content)>=5:
                toeval=message.content[5:]
                print(f"> print({toeval})")
                toprint=eval(toeval)
                print(toprint)
        elif message.content.startswith("send"): #debug 変数名等を指定してチャンネルに投下してもらう
            #用例 "send compe_mgr.uids"
            if len(message.content)>=5:
                toeval=message.content[5:]
                await message.channel.send(f"> print({toeval})")
                tosend=eval(toeval)
                await message.channel.send(tosend)
        elif self.user in message.mentions and not message.author.bot: # botへ、他の人から為されたメンション
            await compe_mgr.get_compedata(message.channel.id).hub(message)

    async def regular_check(self, interval): #on_readyから呼ばれる。ensure_futureによる定期実行、間隔はinterval秒。
        while True:
            await print("hello") #debug
            #compe_mgr.check_schedule() こんな感じで時間経過に関した処理を実行？
            await asyncio.sleep(interval)

    #拡張例
    async def on_member_join(self, member): #メンバーはChannelではなくGuildへ所属することに注意
        pass #todo:compe_mgrのグローバルな設定項目を更新

    async def on_member_remove(self, member): #メンバーはChannelではなくGuildへ所属することに注意
        pass #todo:compe_mgrのグローバルな設定項目を更新


if __name__ == '__main__':
    with open('discord_token.txt', 'r') as f:
        TOKEN = f.read()
    compe_mgr=Compe_manager()
    MyClient().run(TOKEN)
