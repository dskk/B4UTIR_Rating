import discord
from parsedmention import ParsedMention
from responder import Responder


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
            responder.process(pm)


if __name__ == '__main__':
    with open('discord_token.txt', 'r') as f:
        TOKEN = f.read()
    responder=Responder("data.dat")
    MyClient().run(TOKEN)
