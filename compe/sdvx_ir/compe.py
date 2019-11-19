import asyncio
import discord

class Compe:
    """
    モジュールごとに実装。チャンネル(=大会)1つにつき1インスタンス。
    hub関数は必須。
    """
    def __init__(self):
        self.uids=[] #ユーザーIDのリスト
        self.scores={} #key=ユーザーID val=score
        self.perfs={} #key=ユーザーID val=perf
        #self.channel #対応するdiscord.channel。後で必要になる気がする
        #self.last_update #最終更新日時。botを再起動する際にログを遡るのに必要？

    async def hub(self, item):
        """
        起こったイベントの種類を判別、適切な関数を判断してitemを横流しする。
        if (itemが満たすべき条件):
            渡す先の関数(item)
        の形式で、条件を満たすブロックが全て実行される仕様が良さそう。
        処理を独立に書けるため機能の追加が楽なはず。
        下記の通りitemの素性が全く不明のため、条件文を書くときは注意
        (存在しない関数を呼んでしまうなど)。

        Parameters
        ----------
        item : unknown_type
            イベントで処理すべき対象。例えばメンションならdiscord.messageのインスタンス。
        """

        if type(item)==discord.Message:
            content=item.content.split()
            if len(content)==2 and content[1].isdecimal() and item.attachments: #メッセージ本文が単発の数字のみ&&添付ファイルあり
                await self.submit(item, content[1]) #提出処理

    async def submit(self, message, score_str):
        min_score=0; max_score=1000000
        uid=message.author.id
        reply=message.author.mention+" "
        score=int(score_str)
        if not min_score <= score <= max_score:
            reply += "Error: スコアがありえない値になっています！"
        elif self.scores[uid]>score:
            reply += "Error: 提出スコアがあなたのベストスコア未満です！"
        else:
            reply += f"Score:{score_str}で提出を受理しました！"
            self.scores[uid]=score
        await message.channel.send(reply)
        #self.log.update(...) 時系列データとしてのロギングもする。詳細未定。

    async def calc_perf(self):
        """
        現在の提出状況から各ユーザーのパフォーマンスを計算。
        コンテスト中に呼べば暫定のパフォーマンスが出せるので
        レート変動のpredictor等の実装に使えるはず。
        """
        for uid in self.uids: #debug めっちゃ仮。スコア=perfで実装してある。
            self.perfs=scores[uid]
