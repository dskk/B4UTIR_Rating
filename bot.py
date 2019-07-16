import discord

TOKEN = ''
with open('discord_token.txt', 'r') as f:
    TOKEN = f.read()

class MyClient(discord.Client):

    def error_type(self, txt_list): #適切なフォーマットの時はNoneを返し、それ以外の場合はケースに応じてstringをreturnする関数
        return None #これから埋める

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if self.user in message.mentions: # botへのメンションのみ反応
            if message.author.bot: # メッセージ送信者がBotだった場合は無視する
                return
            txt_list = message.content.split() #スペース区切りでメンションを分割、0は必ず@IR_Rating
            errors = self.error_type(txt_list)
            if errors:
                reply = f'{message.author.mention} {errors}'
                await message.channel.send(reply)
            else: 
                reply = f'{message.author.mention} User:{txt_list[1]} Score:{txt_list[2]} で提出を受理しました！'
                await message.channel.send(reply)

if __name__ == '__main__':
    x = MyClient()
    x.run(TOKEN)
