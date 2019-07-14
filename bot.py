import discord

TOKEN = ''
with open('discord_token.txt', 'r') as f:
    TOKEN = f.read()

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        #botへのメンションのみ反応
        if self.user in message.mentions: # 話しかけられたかの判定
            reply = f'{message.author.mention} 呼んだ？' # 返信メッセージの作成
            await message.channel.send(reply) # 返信メッセージを送信

x = MyClient()
x.run(TOKEN)