class ParsedMention():

    def __init__(self, message):
        self.message=message #未実装の内容を無理にでも抜いてきたいときにmessageそのものが必要になるので一応保存
        self.text_properties=self.parse_text(message.content) # メンションのscore=1000000みたいなkey:valペアを保存するdict。key,valともstringのまま保存する。
        self.attachments=message.attachments
        self.author=message.author
        #以下同様に、discordライブラリのmessageにぶら下がっているものたちを必要なだけ埋める。

    def parse_text(self, mention_text): # mention_textはメンション本文(string)
        text_properties={}
        for line in mention_text.splitlines(): #行ごとにメンションを分解
            if line.count("=") == 1: # [key]=[val]の形をした行は意味のある入力とみなす
                key, val = line.split("=")
                text_properties[key]=val #辞書に要素を追加する。もし同じkeyを持つ行が複数あった場合は後に出てきたほうで上書きされる。
        return text_properties
