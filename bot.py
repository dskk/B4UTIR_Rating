import discord
import responder

class ParsedMention():

    def __init__(self, message):
        self.debug=""
        self.message=message #未実装の内容を無理にでも抜いてきたいときにmessageそのものが必要になるので一応保存
        self.text_properties=self.parse_text(message.content) # メンションのscore=1000000みたいなkey:valペアを保存するdict。key,valともstringのまま保存する。
        self.attachments=message.attachments
        #以下同様に、discordライブラリのmessageにぶら下がっているものたちを必要なだけ埋める。

    def parse_text(self, mention_text): # mention_textはメンション本文(string)
        text_properties={}
        for line in mention_text.splitlines(): #行ごとにメンションを分解
            if line.count("=") == 1: # [key]=[val]の形をした行は意味のある入力とみなす
                key, val = line.split("=")
                self.debug+="key="+key+", val="+val+"\n"
                text_properties[key]=val #辞書に要素を追加する。もし同じkeyを持つ行が複数あった場合は後に出てきたほうで上書きされる。
            else:
                self.debug+="この行に情報はありません:"+line+"\n"
        return text_properties


class MyClient(discord.Client):

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if self.user in message.mentions: # botへのメンションのみ反応
            if message.author.bot: # メッセージ送信者がBotだった場合は無視する
                return
            if "kill" in message.content:
                await self.logout()
                return
            pm=ParsedMention(message)
            print(pm.debug)
            responder.Responder(pm)


if __name__ == '__main__':
    TOKEN = ''
    with open('discord_token.txt', 'r') as f:
        TOKEN = f.read()
    x = MyClient()
    x.run(TOKEN)
