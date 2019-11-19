from compe import sdvx_ir
#from compe import iidx_ir
#etc...

#import db

class Compe_manager:
    """
    全ての大会に関するデータを持つclass。bot.pyの最初でglobalに1つだけ作られる。
    チャンネル1つにつき.compe以下に置かれたいずれかのモジュールのインスタンス(大会データ)が1つ生成される。
    モジュールの違いは大会種別の違いに対応、大会データが実際の大会1つ1つに対応。
    大会データの実体はチャンネルID=cidとして、self.cid_to_compedata[cid]で参照できる。
    """
    def __init__(self):
        self.cid_to_competype={} #チャンネルID:大会データの種類(モジュール)
        self.cid_to_compedata={} #チャンネルID:大会データ
        self.uids=[] #guildに所属するユーザーIDのlist。中身はbotのon_readyで埋める
        self.uid_to_name={} #ユーザーID:ユーザーネーム
        # self.scheduled=[] #大会の開始と終了など、スケジュールされたイベントを持っておく？詳細未定
        # self.active_competitions #後でinitすべき大会一覧？

        #ここでDBからデータ読み込んで各種データを初期化
        #<guildのレベル=大会ごとより上の階層=Compe_managerのフィールドに関する操作>
        self.cid_to_competype[599809803191058445]=sdvx_ir #debug "一般"をSDVXのIRチャンネルに
        self.cid_to_competype[633598972510076938]=sdvx_ir #debug "nadchu_test"をSDVXのIRチャンネルに
        #<大会ごとのレベル=Compe_manager.cid_to_compedataのフィールドに関する操作>
        #TBA

    def init_compedata(self, cid):
        if cid in self.cid_to_competype.keys():
            module=self.cid_to_competype[cid] #該当する大会データの種類
            self.cid_to_compedata[cid]=module.compe.Compe() #大会データをインスタンス化
            #cidをキーとしてDBからデータ取得(self.cid_to_compedata[cid]のフィールドを埋める)
            self.cid_to_compedata[cid].uids=self.uids #debug
            for uid in self.uids: #debug 全員未提出でスコアを初期化
                self.cid_to_compedata[cid].scores[uid]=-1 #debug

    def get_compedata(self, cid): #チャンネルIDから大会データを返す。外から呼ばれるので関数化
        return self.cid_to_compedata[cid]
