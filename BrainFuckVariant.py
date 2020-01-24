#!/usr/bin/env python
# -*- coding: utf-8 -*-
## Python3

import sys
import BrainFuck

## Ook language
class Ook (BrainFuck.BrainFuck):
    """Ook language class
    http://www.dangermouse.net/esoteric/ook.html

    Replace token designed for orang-utans.
    """
    TOKENS = ['Ook. Ook?','Ook? Ook.','Ook. Ook.','Ook! Ook!','Ook. Ook!','Ook! Ook.','Ook! Ook?','Ook? Ook!']
    DEM = ' '

def test_ook():
    o = Ook()
    o.printparams()
    print('** Convert Hello World BraiFuck code to Ook code:')
    b = BrainFuck.BrainFuck()
    bf_opcodes = b.opcodes(b.BF_HELLO_WORLD_SRC)
    ook_src = o.src(bf_opcodes)
    print(ook_src)
    print('** Hello World test:')
    o.test(ook_src)
    print('')

## BrainCrash language
class BrainCrash (BrainFuck.BrainFuck):
    """BrainCrash language
    https://enpedia.rxy.jp/wiki/BrainCrash
    
    Add 4 new opcode, or, and, not, and xor.
    Store ord('Hello, world!') at begining of data cell
    output byte in data cell and increment pointer until byte==0
    """
    EXTRA_OPTOKEN_DICT = {
        'or':'|',
        'and':'&',
        'not':'~',
        'xor':'^'
    } # extra 4 opcode and token
    OPTOKEN_DICT = dict(BrainFuck.BrainFuck.OPTOKEN_DICT.items())
    OPTOKEN_DICT.update(EXTRA_OPTOKEN_DICT)
    def preproc(self):
        """store "Hello, world!" at the begining of data cell, and move pointer to run BF code
        """
        self.cell[0:12] = [ord(s) for s in 'Hello, world!']
        if len(self.code)>0:
            self.code = ['nxt']*13 + self.code
        return True
    def postproc(self):
        """after run opcodes, increment pointer to output the byte at pointer until byte==0
        """
        while self.cell[self.ptr]!=0:
            sys.stdout.write(chr(self.cell[self.ptr]))
            self.ptr+=1
        return True
    def op_or(self):
        """*ptr++ or *ptr => *ptr++"""
        self.cell[self.ptr+1] = self.cell[self.ptr] | self.cell[self.ptr+1]
        self.ptr+=1
        return True
    def op_and(self):
        """*ptr++ and *ptr => *ptr++"""
        self.cell[self.ptr+1] = self.cell[self.ptr] & self.cell[self.ptr+1]
        self.ptr+=1
        return True
    def op_xor(self):
        """*ptr++ xor *ptr => *ptr++"""
        self.cell[self.ptr+1] = self.cell[self.ptr] ^ self.cell[self.ptr+1]
        self.ptr+=1
        return True
    def op_not(self):
        """not *ptr => *ptr"""
        self.cell[self.ptr] = ~ self.cell[self.ptr]
        return True

def test_bc():
    bc=BrainCrash()
    bc.printparams()
    print('** Run without argument:')
    bc.run('')
    print('')
    print('** BrainFuck code test:')
    bc.test(bc.BF_HELLO_WORLD_SRC)
    bc.initializer()
    print('** Another test (output "Enpedia"):')
    out_Enpedia_src = '[-]&&&&&&&&&&&&&+++++++[>++++++++++<-]>-.<+++++++[>++++++<-]>-.++.-----------.-.+++++.--------'
    bc.test(out_Enpedia_src)
    print('')
    print('')

## コミュ障プログラミング言語
class CommDis(BrainCrash):
    """Communication disorder language (コミュ障プログラミング言語)
    http://www.moonroom.mydns.jp/ls/software/commdis.htm
    
    Add 6 new opcode to BrainCrash, shl, shr, njm, pjm, zro, and hom.
    Replace token designed for Communication disorder in Japanese
    """
    EXTRA_OPTOKEN_DICT = dict(
        shl = '*', # bit shift left
        shr = '/', # bit shift right
        njm = '{', # jump to next
        pjm = '}', # jump to previous
        zro = '!', # set zero
        hom = '?'  # jump to home
    ) # extra 6 opcodes to BrainCrash
    OPTOKEN_DICT = dict(BrainCrash.OPTOKEN_DICT.items())
    OPTOKEN_DICT.update(EXTRA_OPTOKEN_DICT)
    ARRAY_SIZE = 32767
    TOKENS = ['ｱｱ…','ｱｱ､','ｱ…','ｱ､','ｴｯﾄ…','ｴｯﾄ､','ｻｾﾝ…','ｯｽ…','ｱｯ…','ｱｯ､','ｱﾉ…','ｱﾉ､','ｱｰ…','ｱｰ､','ｴ…','ｴ､','ｴｯ…','ｴｯ?']
    def op_shl(self):
        """*ptr bit shift left"""
        self.cell[self.ptr]<<1
        return True
    def op_shr(self):
        """*ptr bit shift right"""
        self.cell[self.ptr]>>1
        return True
    def op_njm(self):
        """increase ptr by *ptr"""
        self.ptr+=self.cell[self.ptr]
        return True
    def op_pjm(self):
        """decrease ptr by *ptr"""
        self.ptr-=self.cell[self.ptr]
        return True
    def op_zro(self):
        """*ptr = 0""" 
        self.cell[self.ptr] = 0
        return True
    def op_hom(self):
        """ptr = 0"""
        self.ptr=0
        return True

def test_cd():
    cd=CommDis()
    cd.printparams()
    print('** Run without argument:')
    cd.run('')
    print('')
    print('** Convert opcode to CommDiss token:')
    print(cd.translator(['nxt','prv','hom','pjm','cls'], reverse=True))
    print('')
    fizzbuzzsrc = """ｱ…ｱ…ｱ…ｱ…ｱ…ｱ…ｻｾﾝ…ｱ､ｱｱ…ｱ…ｱ…ｱ…ｱ…ｱｱ…ｱｱ…ｱ…ｱｱ…ｱ…
ｱｱ…ｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｯｽ…ｱｱ…ｻｾﾝ…ｱｱ､ｱ…ｱ…ｱ…ｱ…ｱｱ…ｱｱ…ｱ…
ｱ…ｱ…ｱｱ…ｱ…ｱ…ｱ…ｱ…ｱｱ…ｱｱ…ｱ…ｱ…ｱ…ｱｱ…ｱ…ｱ…ｱ…ｱ…ｱ…
ｱｱ…ｱ…ｱ…ｱ…ｱ…ｱ…ｱｱ…ｱｱ…ｱｱ…ｱｱ…ｱｱ…ｱｱ…ｱ…ｱ…ｱｱ…ｱｱ…ｱ…
ｱ…ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱ､ｯｽ…ｱｱ､ｱ…ｱ…
ｱ…ｱ…ｱｱ…ｱ…ｱ…ｱ…ｱｱ…ｱ､ｱ､ｱｱ…ｱ…ｱ…ｱ…ｱｱ…ｱ､ｱｱ…ｱｱ…ｱ､ｱ､ｱ､
ｱｱ…ｱ…ｱ…ｱｱ…ｱｱ…ｱｱ…ｱ…ｱ…ｱ…ｱ…ｱ…ｻｾﾝ…ｱ､ｱｱ…ｱ…ｱ…ｱｱ…ｱ…
ｱ…ｱｱ､ｱｱ､ｯｽ…ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｻｾﾝ…ｱ､ｱｱ…ｱ､ｻｾﾝ…
ｱｱ…ｱｱ…ｱｱ…ｱｱ…ｱｱ…ｱｱ…ｱｱ…ｯｽ…ｱｱ…ｻｾﾝ…ｱｱ､ｱ…ｱ…ｱ…ｱｱ…ｴｯﾄ…
ｱｱ…ｴｯﾄ…ｱｱ…ｱｱ…ｱｱ…ｱｱ…ｴｯﾄ…ｴｯﾄ…ｱｱ…ｱｱ…ｱｱ…ｱ…ｱｱ､ｯｽ…ｱｱ､
ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱ､ｻｾﾝ…ｱｱ…ｱｱ…ｱｱ…ｱｱ…ｯｽ…ｱｱ…ｻｾﾝ…ｱｱ､ｱ…ｱ…ｱ…
ｱ…ｱ…ｱｱ…ｴｯﾄ…ｱｱ…ｴｯﾄ…ｱｱ…ｴｯﾄ…ｴｯﾄ…ｱｱ…ｱｱ…ｱｱ…ｱ…ｱｱ､ｯｽ…
ｱｱ…ｱｱ…ｱｱ…ｱｱ…ｱ…ｱｱ､ｱ､ｻｾﾝ…ｱｱ､ｱｱ､ｱｱ､ｯｽ…ｱｱ､ｻｾﾝ…ｻｾﾝ…ｱ､ｱｱ､
ｱｱ､ｱ…ｱｱ…ｱｱ…ｯｽ…ｱｱ…ｱｱ…ｱｱ…ｱ…ｱｱ…ｱ…ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｻｾﾝ…
ｱ､ｱｱ…ｱｱ…ｱ…ｱｱ…ｱ…ｱｱ…ｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｯｽ…ｱｱ､ｯｽ…ｱｱ…ｱｱ…ｻｾﾝ…
ｻｾﾝ…ｱ､ｯｽ…ｱｱ､ｯｽ…ｱｱ…ｻｾﾝ…ｱｱ…ｱｱ…ｱｱ…ｻｾﾝ…ｱｱ…ｴｯﾄ…ｱｱ､ｱｱ､ｴｯﾄ…
ｱｱ､ｱｱ､ｱｱ､ｯｽ…ｱｱ､ｻｾﾝ…ｴｯﾄ…ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｯｽ…ｱｱ…ｯｽ…ｱｱ…ｴｯﾄ…
ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｱｱ､ｯｽ…"""
#    print('** Run FizzBuzz:')
#    cd.run(fizzbuzzsrc)
    print('** Convert FizzBuzz code to BrainFuck code:')
    opcodes = cd.opcodes(fizzbuzzsrc)
    b = BrainFuck.BrainFuck()
    bf_src = b.src(opcodes)
    print(bf_src)
    print('')

## プログラミング言語 ζ*'ヮ')ζ＜うっうー！
class Ut_U(BrainFuck.BrainFuck):
    """Programing language Ut-U (プログラミング言語 ζ*'ヮ')ζ＜うっうー！)
    
    Delete get and add new opcode nop.
    Change nxt and prv opcode to allow to loop (ptr==-1 => ptr==ARRAY_SIZE)
    Sync data cell and code cell (code cell and data cell are shared in according to spec)
    
    http://tackman.info/ut-u/
    """
    OPTOKEN_DICT = dict(
        nop = 'あうー',
        inc = 'うっうー',
        dec = 'ううー',
        nxt = 'イエイ',
        prv = 'おとく',
        put = 'ハイ、ターッチ',
        opn = 'かもー',
        cls = 'かなーって'
    ) # replace opcode and token
    def __init__(self, **kwargs):
        super().__init__(cell_size=3, delimiter=' ', wrap_cell=True, **kwargs)
    def copy_code2cell(self):
        """copy code area to data area"""
        ops = self.optoken.opcodes()
        opmap = dict(zip(ops, [x for x in range(len(ops))]))
        for i in range(len(self.code)):
            self.cell[i] = opmap[self.code[i]]
        return True
    def copy_cell2code(self):
        """copy data area to code area"""
        for ei in range(len(self.cell)-1, -1, -1):
            if self.cell[ei]!=0: break
        ei = max(ei, len(self.code))
        for i in range(len(self.cell[0:ei])):
            self.code[i] = self.optoken.opcodes()[(self.cell[i])]
        return True
    def preproc(self):
        """call copy_code2cell() to initialize data area"""
        self.copy_code2cell()
        return True
    def stepproc(self):
        """sync data area and code area at each code step"""
        self.copy_cell2code()
        self.copy_code2cell()
        return True
    def op_nop(self):
        """do nothing"""
        pass
        return True
    def op_put(self):
        """output token related with the byte at the pointer"""
        sys.stdout.write(self.optoken.tokens()[self.cell[self.ptr]]+self.delimiter[0])
        return True
    def op_inc(self):
        """increment the byte at pointer (++*ptr)
            behave as full adder
        """
        for i in range(len(self.code)-self.ptr):
            i = i + self.ptr
            self.cell[i] += 1
            if self.cell[i] != 0:
                break
        if self.cell[self.ptr]>self.cell_max:
            if self.wrap_cell:
                self.cell[self.ptr] = self.cell_min
            else:
                raise ValueError('Byte at cell pointer is set as '+str(self.cell[self.ptr])+' over maximum value='+str(self.cell_max))
        return True
    def op_dec(self):
        """decrement the byte at pointer (--*ptr)
            behave as full substractor
        """
        for i in range(self.ptr):
            i = self.ptr - i
            self.cell[i] -= 1
            if self.cell[i] != 7:
                break
        if self.cell[self.ptr]<self.cell_min:
            if self.wrap_cell:
                self.cell[self.ptr] = self.cell_max
            else:
                raise ValueError('Byte at cell pointer is set as '+str(self.cell[self.ptr])+' under minimum value='+str(self.cell_min))
        return True


def test_utu():
    u=Ut_U()
    u.printparams()
    print('** test (output "うっうー"x7):')
    u.test('あうー うっうー かもー イエイ ハイ、ターッチ おとく うっうー かなーって')
    print('')
    print('')
    u.initializer()
    print('** Another test (output "うっうー"x7):')
    src="""\
うっうー！私はりきっちゃうかもー！
イエイってなっちゃうかなーって。

高槻やよいでーっす、イエイ！
なんだか「ぷろぐらみんぐげんご」になっちゃうらしくて、うっうーってなっちゃいます！ イエイ！
うっうーって私の口癖なんですけど、うっうーって言うとうっうーってなっちゃって、もううっうーうっうーうっうーイエイって感じです！
モニタの前のみなさんも、うっうーって言ってうっうーってなっちゃいましょう！うっうー、イエイ！
あのあの、うっうーって言うと「ぽいんたの指す値」がうっうーってなって、うっうーって感じで増えて、うっうーがうっうーでイエイになるらしいです。よく分かりません…
とにかくうっうーって叫べば、どんどんうっうーってなって、もううっうーが止まらなくてうっうーイエイってなります！
うっうーばっかりで苦しくなってきましたけど、イエイってがんばります！
もう一息、うっうーうっうーうっうーうっうーうっうーうっうーうっうー！！！

このページは、おとくです！えむ、あい、てぃーライセンスで配布するそうなのでおとく！お金がかからないのでおとく、再配布も出来ておとく、おとくでおとくなのですっごくおとくです！

あうー、がんばって説明しましたけど、あうーって感じでよく分からないです、あうー… あうー、ボロが出ないうちに退散します、あうー…え、あうーってまだ言わなきゃですか？ あうー あうー。
"""
    u.test(src)
    print('')
    print('')

## ジョジョ言語
class JoJo (BrainFuck.BrainFuck):
    """JoJo language (ジョジョ言語)
    http://d.hatena.ne.jp/toyoshi/touch/20100208/1265587511
    
    Replace token as "JoJo's Bizarre Adventure" in Japanese
    """
    TOKENS = [
        ['スターフィンガ','やれやれだぜ'],
        ['ロードローラ','貧弱'],
        'オラ',
        '無駄',
        'ハーミットパープル',
        '新手のスタンド使いか',
        'あ・・・ありのまま今起こったことを話すぜ',
        'ザ・ワールド'
    ] # replace token

def test_jojo():
    j=JoJo()
    j.printparams()
    src = """\
オラオラオラオラオラオラオラオラオラッ！！

「あ・・・ありのまま今起こったことを話すぜ
俺は奴の前で階段を登っていたと思ったら、いつの間にか降りていた
な…何を言っているのかわからねーと思うが、
俺も何をされたのかわからなかった…
頭がどうにかなりそうだった…催眠術だとか超スピードだとか、
そんなチャチなもんじゃあ断じてねえ。
もっと恐ろしいものの片鱗を味わったぜ…」

スターフィンガー！
オラオララララ！
オラッ！オラオラララララオラオラオラァ！！！
スターフィンガー！！！
オラァオラオラオラオラオラオラッオラ！！
オラオラァァァァァオララララララララララ！
スターフィンガー！

オラオラオラオラオラ！　つけの領収書だぜ！

力比べというわけか！
知るがいい…！『ザ・ ワールド』の真の能力は…まさに！『世界を支配する』能力だと言うことを！

「ロードローラだ！ロードローラだ！ロードローラだ！」
無駄ッッッ！

ザ・ワールドッッ

スターフィンガー！
「ハーミットパープル」
スターフィンガー
オラオラ！

「ハーミットパープル」

オラオラオラオラオラオラオラ
ハーミットパープル！ハーミットパープル！

オラオラオラ

ハーミットパープル！
スターフィンガー！

無駄ァ！
ハーミットパープル

無駄！無駄！
無駄無駄無駄無駄無駄無駄無駄無駄無駄無駄
WRYYYYYYYYYYYYYY！
“ジョースター・エジプト・ツアー御一行様”は貴様にとどめを刺して全滅の最後というわけだな

ハーミットパープル！
ロードローラだ！

オーラオラオーラオラオラオラオーラオラオラオラオラッ！
ハーミットパープル！
無駄無駄無駄無駄無駄無駄無駄無駄ッ
ハーミットパープル！
オラオラオラアアアアアアアア！
ハーミットパープル！
無駄ッ無駄ッ無駄ッ無駄無駄無駄ァツ！

ハーミットパープル

もうおそい！　脱出不可能よッ！ 無駄無駄無駄無駄無駄無駄無駄無駄ぁぁ！
ハーミットパープル！

最高に『ハイ！』ってやつだアアアアア！アハハハハハハハハハーッ！！
スターフィンガー
オラ
ハーミットパープル！

てめーの敗因は・・・たったひとつだぜ・・・ＤＩＯ　たったひとつの単純（シンプル）な答えだ・・・　『てめーは　おれを怒らせた』"""
    j.test(src)
    print('')
    print('')

## プログラミング言語フレンズ
class Kemono (BrainFuck.BrainFuck):
    """Programing language Friends (プログラミング言語フレンズ)
    https://github.com/consomme/kemono_friends_lang
    
    Replace token as Serval in Kemono Friends in Japanese.
    See https://en.wikipedia.org/wiki/Kemono_Friends about Kemono Friends
    """
    OPTOKEN_DICT = dict( # BrainFuck opcode and token
        nxt = "たのしー！",
        inc = "たーのしー！",
        prv = "すごーい！",
        dec = "すっごーい！",
        opn = "うわー！",
        cls = "わーい！",
        put = "なにこれなにこれ！",
        get = "おもしろーい！")

def test_kemono():
    k = Kemono()
    k.printparams()
    src = """たのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！うわー！すごーい！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！たのしー！すっごーい！わーい！すごーい！なにこれなにこれ！たのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！うわー！すごーい！たーのしー！たーのしー！たーのしー！たーのしー！たのしー！すっごーい！わーい！すごーい！たーのしー！なにこれなにこれ！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！なにこれなにこれ！なにこれなにこれ！たーのしー！たーのしー！たーのしー！なにこれなにこれ！うわー！すっごーい！わーい！たのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！うわー！すごーい！たーのしー！たーのしー！たーのしー！たーのしー！たのしー！すっごーい！わーい！すごーい！なにこれなにこれ！たのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！うわー！すごーい！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！たのしー！すっごーい！わーい！すごーい！なにこれなにこれ！たのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！うわー！すごーい！たーのしー！たーのしー！たーのしー！たのしー！すっごーい！わーい！すごーい！なにこれなにこれ！たーのしー！たーのしー！たーのしー！なにこれなにこれ！すっごーい！すっごーい！すっごーい！すっごーい！すっごーい！すっごーい！なにこれなにこれ！すっごーい！すっごーい！すっごーい！すっごーい！すっごーい！すっごーい！すっごーい！すっごーい！なにこれなにこれ！うわー！すっごーい！わーい！たのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！うわー！すごーい！たーのしー！たーのしー！たーのしー！たーのしー！たのしー！すっごーい！わーい！すごーい！たーのしー！なにこれなにこれ！うわー！すっごーい！わーい！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！たーのしー！なにこれなにこれ！"""
    k.test(src)
    print('')

## プログラミング言語「長門有希」
class Nagato(BrainFuck.BrainFuck):
    """ Programing language "Yuki Nagato" (プログラミング言語「長門有希」)
    http://web.archive.org/web/20080331053354/http://not6.blog.shinobi.jp/Entry/103/
    
    Replace token as Yuki Nagato in novel/animation "Haruhi Suzumiya" in Japanese.
    See https://en.wikipedia.org/wiki/Haruhi_Suzumiya about Haruhi Suzumiya.
    """
    TOKEN_UNIT = '…'
    OPTOKEN_DICT = dict( # BrainFuck opcode and token
        inc = TOKEN_UNIT * 1,
        dec = TOKEN_UNIT * 2,
        nxt = TOKEN_UNIT * 3,
        prv = TOKEN_UNIT * 4,
        get = TOKEN_UNIT * 5,
        put = TOKEN_UNIT * 6,
        opn = '「',
        cls = '」'
    )
    DEM = '。'

def test_nagato():
    n = Nagato(wrap_array=True)
    n.printparams()
    src = """\
…………。…。…。…。…。…。…。…。…。…。
「………。…。…。…。…。…。…。…。…。…………。……長門有希」
………。………………。…………。…。…。…。…。…。…。…。
「………。…。…。…。…。…………。……そう」
………。…。………………。…。…。…。…。…。…。…。………………。
………………。…。…。…。………………。
「……」
…………。…。…。…。…。…。…。…。…。
「………。…。…。…。…。…………。……そう」
………。………………。…………。…。…。…。…。…。…。…。…。…。…。…。
「………。…。…。…。…。…。…………。……別に」
………。………………。…………。…。…。…。…。…。…。…。…。
「………。…。…。…。…………。……どうぞ」
………。………………。…。…。…。………………。
……。……。……。……。……。……。………………。
……。……。……。……。……。……。……。……。………………。
「……わりと」
…………。…。…。…。…。…。…。…。…。
「………。…。…。…。…。…………。……」
………。…。………………。
「……怒り君」
…。…。…。…。…。…。…。…。…。…。
………………。"""
    n.test(src)
    print('')

## NekoMimiF*ck
class NekoMimi(BrainFuck.BrainFuck):
    """NekoMimiF*ck
    http://web.archive.org/web/20080415234349/http://d.hatena.ne.jp/tokuhirom/20041015/p14
    """
    OPTOKEN_DICT = dict( # BrainFuck opcode and token
        nxt = 'ネコミミ！',
        prv = 'ネコミミモード',
        inc = 'おにいさま',
        dec = '私のしもべー',
        put = 'や・く・そ・く・よ',
        get = 'フルフルフルムーン',
        opn = 'キスキス…',
        cls = 'キス…したくなっちゃった…'
    )

def test_nekomimi():
    n = NekoMimi()
    n.printparams()
    src = """\
おにいさまおにいさまおにいさまおにいさまキスキス…ネコミミ！おにいさまおにいさま
おにいさまおにいさまキスキス…ネコミミ！おにいさまおにいさまおにいさまおにいさま
ネコミミ！おにいさまおにいさまおにいさまおにいさまおにいさまおにいさまネコミミ！
おにいさまおにいさまネコミミモードネコミミモードネコミミモード私のしもべー
キス…したくなっちゃった…ネコミミ！おにいさまおにいさまネコミミ！おにいさま
ネコミミモードネコミミモードネコミミモード私のしもべーキス…したくなっちゃった…
ネコミミ！ネコミミ！や・く・そ・く・よネコミミ！おにいさまや・く・そ・く・よ
おにいさまおにいさまおにいさまおにいさまおにいさまおにいさまおにいさま
や・く・そ・く・よや・く・そ・く・よおにいさまおにいさまおにいさまや・く・そ・く・よ
ネコミミ！や・く・そ・く・よネコミミモードネコミミモード私のしもべーネコミミモード
おにいさまおにいさまおにいさまおにいさまキスキス…ネコミミ！おにいさまおにいさま
おにいさまおにいさまネコミミモード私のしもべーキス…したくなっちゃった…ネコミミ！
や・く・そ・く・よネコミミ！や・く・そ・く・よおにいさまおにいさまおにいさま
や・く・そ・く・よ私のしもべー私のしもべー私のしもべー私のしもべー私のしもべー
私のしもべーや・く・そ・く・よ私のしもべー私のしもべー私のしもべー私のしもべー
私のしもべー私のしもべー私のしもべー私のしもべーや・く・そ・く・よネコミミ！
おにいさまや・く・そ・く・よ
"""
    n.test(src)
    print('')
    print('')

## 名状しがたいプログラミング言語のようなもの Nyaruko
## https://github.com/masarakki/nyaruko_lang
class Nyaruko(BrainFuck.BrainFuck):
    """名状しがたいプログラミング言語のようなもの Nyaruko
    https://github.com/masarakki/nyaruko_lang
    """
    OPTOKEN_DICT = dict( # BrainFuck opcode and token
        nxt = '(」・ω・)」うー(／・ω・)／にゃー',
        inc = '(」・ω・)」うー!(／・ω・)／にゃー!',
        prv = '(」・ω・)」うー!!(／・ω・)／にゃー!!',
        dec = '(」・ω・)」うー!!!(／・ω・)／にゃー!!!',
        opn = 'CHAOS☆CHAOS!',
        cls = 'I WANNA CHAOS!',
        put = 'Let\'s＼(・ω・)／にゃー',
        get = 'cosmic!',
    )

def test_nyaruko():
    n = Nyaruko()
    n.printparams()
    src = """(」・ω・)」うー(／・ω・)／にゃー(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!CHAOS☆CHAOS!(」・ω・)」うー!!(／・ω・)／にゃー!!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー(／・ω・)／にゃー(」・ω・)」うー!!!(／・ω・)／にゃー!!!I WANNA CHAOS!(」・ω・)」うー!!(／・ω・)／にゃー!!Let's＼(・ω・)／にゃー(」・ω・)」うー(／・ω・)／にゃー(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!CHAOS☆CHAOS!(」・ω・)」うー!!(／・ω・)／にゃー!!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー(／・ω・)／にゃー(」・ω・)」うー!!!(／・ω・)／にゃー!!!I WANNA CHAOS!(」・ω・)」うー!!(／・ω・)／にゃー!!(」・ω・)」うー!(／・ω・)／にゃー!Let's＼(・ω・)／にゃー(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!Let's＼(・ω・)／にゃーLet's＼(・ω・)／にゃー(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!Let's＼(・ω・)／にゃーCHAOS☆CHAOS!(」・ω・)」うー!!!(／・ω・)／にゃー!!!I WANNA CHAOS!(」・ω・)」うー(／・ω・)／にゃー(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!CHAOS☆CHAOS!(」・ω・)」うー!!(／・ω・)／にゃー!!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー(／・ω・)／にゃー(」・ω・)」うー!!!(／・ω・)／にゃー!!!I WANNA CHAOS!(」・ω・)」うー!!(／・ω・)／にゃー!!Let's＼(・ω・)／にゃー(」・ω・)」うー(／・ω・)／にゃー(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!CHAOS☆CHAOS!(」・ω・)」うー!!(／・ω・)／にゃー!!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー(／・ω・)／にゃー(」・ω・)」うー!!!(／・ω・)／にゃー!!!I WANNA CHAOS!(」・ω・)」うー!!(／・ω・)／にゃー!!Let's＼(・ω・)／にゃー(」・ω・)」うー(／・ω・)／にゃー(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!CHAOS☆CHAOS!(」・ω・)」うー!!(／・ω・)／にゃー!!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー(／・ω・)／にゃー(」・ω・)」うー!!!(／・ω・)／にゃー!!!I WANNA CHAOS!(」・ω・)」うー!!(／・ω・)／にゃー!!Let's＼(・ω・)／にゃー(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!Let's＼(・ω・)／にゃー(」・ω・)」うー!!!(／・ω・)／にゃー!!!(」・ω・)」うー!!!(／・ω・)／にゃー!!!(」・ω・)」うー!!!(／・ω・)／にゃー!!!(」・ω・)」うー!!!(／・ω・)／にゃー!!!(」・ω・)」うー!!!(／・ω・)／にゃー!!!(」・ω・)」うー!!!(／・ω・)／にゃー!!!Let's＼(・ω・)／にゃー(」・ω・)」うー!!!(／・ω・)／にゃー!!!(」・ω・)」うー!!!(／・ω・)／にゃー!!!(」・ω・)」うー!!!(／・ω・)／にゃー!!!(」・ω・)」うー!!!(／・ω・)／にゃー!!!(」・ω・)」うー!!!(／・ω・)／にゃー!!!(」・ω・)」うー!!!(／・ω・)／にゃー!!!(」・ω・)」うー!!!(／・ω・)／にゃー!!!(」・ω・)」うー!!!(／・ω・)／にゃー!!!Let's＼(・ω・)／にゃーCHAOS☆CHAOS!(」・ω・)」うー!!!(／・ω・)／にゃー!!!I WANNA CHAOS!(」・ω・)」うー(／・ω・)／にゃー(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!CHAOS☆CHAOS!(」・ω・)」うー!!(／・ω・)／にゃー!!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー(／・ω・)／にゃー(」・ω・)」うー!!!(／・ω・)／にゃー!!!I WANNA CHAOS!(」・ω・)」うー!!(／・ω・)／にゃー!!(」・ω・)」うー!(／・ω・)／にゃー!Let's＼(・ω・)／にゃーCHAOS☆CHAOS!(」・ω・)」うー!!!(／・ω・)／にゃー!!!I WANNA CHAOS!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!(」・ω・)」うー!(／・ω・)／にゃー!Let's＼(・ω・)／にゃー"""
    n.test(src)
    print('')

## プログラム言語「てってってー」
class Tettette(BrainFuck.BrainFuck):
    """プログラム言語「てってってー」
    http://chiraura.hhiro.net/?page=%A5%D7%A5%ED%A5%B0%A5%E9%A5%E0%B8%C0%B8%EC%A1%D6%A4%C6%A4%C3%A4%C6%A4%C3%A4%C6%A1%BC%A1%D7

    Note: this class does not support sequence in buffer, "\xAB", '\uABCD', and '\dABCDE'.
    """
    OPTOKEN_DICT = dict( # BrainFuck opcode and token
        buf = 'ー',
        end_buf = 'てー',
        com = '{',
        end_com = '}',
        nxt = 'てってー',
        prv = 'てっててー',
        inc = 'ててー',
        dec = 'てっー',
        put = 'てってっー',
        get = 'てってってー',
        opn = 'てってっててー',
        cls = 'てってってっー'
    )
    ARRAY_SIZE = 65536
    def initializer(self):
        """add stack attribute to store string for op_buf()"""
        super().initializer()
        self.stack=[] # stack to store strings
        return True
    def op_put(self):
        """output the byte at the pointer (putchar(*ptr))"""
        sys.stdout.write(chr(self.cell[self.ptr]))
        self.op_nxt() # increment pointer
        return True
    def op_get(self):
        """input a byte and store it in the byte at the pointer (*ptr = getchar())"""
        self.cell[self.ptr] = ord(raw_input("Enter>")[0])
        self.op_nxt() # increment pointer
        return True
    def op_buf(self):
        """write strings to current cell"""
        buf = self.stack.pop()
        for i in range(len(buf)):
            self.cell[self.ptr] = ord(buf[i])
            self.op_nxt()
        return True
    def lexer(self, src):
        """lexical analysis of src code and return tokens list
        
        Args:
            src (str): source code
            
        Returns:
            list: token list
        """
        ## delimit src by multiple delimiter
        def _delimit(src, dem):
            if type(src)==str: src = [src]
            if len(dem)==1 and dem[0]=='': return src
            if len(dem)==0: return src
            else:
                d=dem.pop()
                o=[]
                for s in src:
                    o+=s.split(d)
                return _delimit(o, dem)
        ## core of lexer
        def _lexer(src, tokenlist):
            READ_AHEAD_BYTE = 64 # read ahead byte for debugging output
            tokens = [] # output tokens list
            cur = 0 # current position in src
            ctoken = None # token candidate
            while cur <= len(src)-1:
                cstr = src[cur:]
                start = len(cstr)
                for token in tokenlist:
                    index = cstr.find(token)
                    if index>=0 and (index<start or (index==start and start+len(ctoken)<index+len(token))):
                        ctoken = token
                        start = index
                if self.debug:
                    print('LEXER:', len(tokens), cur, ctoken, cstr[start:READ_AHEAD_BYTE])
                ## buffering
                if ctoken in self.optoken['buf']: # if current token is related with buf opcode
                    cur+=cstr.find(ctoken)+len(ctoken)
                    etoken = None
                    cstr = src[cur:]
                    eindex = len(cstr)
                    for token in self.optoken['end_buf']:
                        index = cstr.find(token)
                        if index>=0 and (index<eindex or (index==eindex and eindex+len(etoken)<index+len(token))):
                            etoken = token
                            eindex = index
                    if etoken!=None:
                        cur+=cstr.find(etoken)+len(etoken)
                        tokens.append(ctoken)
                        self.stack.insert(0,cstr[:eindex])
                    ctoken = None
                    continue
                ## comment
                elif ctoken in self.optoken['com']: # if current token is related with com opcode
                    cur+=cstr.find(ctoken)+len(ctoken)
                    etoken = None
                    cstr = src[cur:]
                    eindex = len(cstr)
                    for token in self.optoken['end_com']:
                        index = cstr.find(token)
                        if index>=0 and (index<eindex or (index==eindex and eindex+len(etoken)<index+len(token))):
                            etoken = token
                            eindex = index
                    if etoken!=None:
                        cur+=cstr.find(etoken)+len(etoken)
                    else:
                        raise SyntaxError('comment token pair are not matched')
                    ctoken = None
                    continue
                ## add token list
                if ctoken!=None:
                    tokens.append(ctoken)
                    cur += cstr.find(ctoken)+len(ctoken)
                    ctoken = None
                else:
                    break
            return tokens
        ## main of lexer function
        tokens = []
        dsrc = [src]
        if self.delimit_input:
            dsrc = _delimit(src, self.delimiter)
        for src in dsrc:
            tokens += _lexer(src, self.optoken.alltokens())
        return tokens

def test_tettette():
    t = Tettette()
    t.printparams()
    out_tettette_src = """ーてってってー　{「てってっ」をメモリに書き込む}
てっててーてっててーてっててーてっててー　{ポインタを4つ戻す}
てってっーてってっーてってっーてってっー　{標準出力へ4文字出力する}
ーててーてっててーてってっー　{「て」をメモリに書き込み、ポインタを戻してから標準出力へ出力する}

ーーてってっててー　{「ーてってって」をメモリに書き込む}
てっててーてっててーてっててーてっててーてっててーてっててー　{ポインタを6つ戻す}
てってっーてってっーてってっーてってっーてってっーてってっー　{標準出力へ6文字出力する}
ーててーてっててーてってっー　{「て」をメモリに書き込み、ポインタを戻してから標準出力へ出力する}
ーーてーてっててーてってっー　{「ー」をメモリに書き込み、ポインタを戻してから標準出力へ出力する}"""
    t.test(out_tettette_src)
    print('')
    print('')

## 猫語
class Neko(BrainFuck.BrainFuck):
    """猫語
    https://qiita.com/zakuroishikuro/items/2acaaf174844b08495a7
    """
    OPTOKEN_DICT = dict( # BrainFuck opcode and token
        inc = 'にゃにゃ',
        dec = 'にゃー',
        nxt = 'にゃっ',
        prv = 'にゃん',
        put = 'にゃ。',
        get = 'にゃ、',
        opn = '「',
        cls = '」'
    )

def test_neko():
    n = Neko()
    n.printparams()
    src = """\
にゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃ

「にゃっにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃっにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃっにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃんにゃんにゃんにゃー」

にゃっにゃ。
にゃっにゃにゃにゃにゃにゃ。
にゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃ。
にゃ。
にゃにゃにゃにゃにゃにゃにゃ。
にゃっにゃーにゃ。

にゃーにゃーにゃーにゃーにゃーにゃーにゃーにゃーにゃーにゃーにゃーにゃーにゃ。
にゃんにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃにゃ。
にゃーにゃーにゃーにゃーにゃーにゃーにゃーにゃーにゃ。
にゃにゃにゃにゃにゃにゃにゃ。
にゃーにゃーにゃーにゃーにゃーにゃーにゃ。
にゃーにゃーにゃーにゃーにゃーにゃーにゃーにゃーにゃ。
にゃっにゃにゃにゃ。
"""
    n.test(src)
    print('')
    print('')

## プログラミング言語 Misa
class Misa(BrainFuck.BrainFuck):
    """プログラミング言語 Misa
    https://enpedia.rxy.jp/wiki/Misa_(%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9F%E3%83%B3%E3%82%B0%E8%A8%80%E8%AA%9E)
    """
    OPTOKEN_DICT = dict( # BrainFuck opcode and token
        nxt = ['>', '→', '～', 'ー'],
        prv = ['<', '←', '★', '☆'],
        inc = ['+', 'あ', 'ぁ', 'お', 'ぉ'],
        dec = ['-', 'っ', 'ッ'],
        put = ['.', '！'],
        get = [',', '？'],
        opn = ['[', '「', '『'],
        cls = [']', '」', '』']
    )

def test_misa():
    m = Misa(wrap_cell=True, wrap_array=True)
    m.printparams()
    src = """\
ごっ、ごぉおっ、ご～きげんよおぉおおぉおほっ。ほおぉおぉおっ。

「ごきげん☆みゃぁああ”あ”ぁ”ぁああ～っ」

さわやかな朝の☆ご挨拶！　お挨拶がっ。
澄みきった青空にこだましちゃうぉ～ああぉおおおぉん。

「は、はひっ、はろおぉっ☆わぁるどおおぉっぉ～っ」

こ、この文章は☆おサンプル！　おおぉおぉおおサンプルプログラム！！
どんなおプログラム言語でも基本のご挨拶させていただくのぉぉおッ！

「ぽうっ」

長々と書くのがこ、ここでの～、ここでのぉおおぉおぉぉおたしなみぃぃいぃ。

「長いぃ。長すぎましゅう。ご挨拶にこんなプログラム長すぎまひゅぅうぅ☆
　んおおぉぉ、ばかになる、おばかになっちゃいましゅ～ッ」

長いのがっ、バッファの奥まで入ってきましゅたぁあぁあっ！
ばっふぁ☆溢れちゃいまひゅぅ～。あみゃぁあ”あ”ぁ”ぁああ”あ”ぁぁ。

「で、出ます☆　んおおぉぉおおっ、エラー出ちゃいまひゅっ」

ほひぃ☆！　え、えらーっ、んお”お”ぉお”お”ぉおぉおおぉっっ。

「出た☆　出た出た出た出たぁぁあっ　えらあぴゅるーっって出たあぁっ」

はしたない☆！　ぉおおぉはしたないっ！　おはしたない言語ですっっっっっっっ！
おほっほおぉっっっほおぉっっっっっっっっっ！

「えらあらいしゅきぃぃぃいぃっっ」

止まらない　すごい　エラーみるく
こってりしたのがいっぱい出てるよぉぉぉおおぉぉおおぉぉおっっ。

「んほぉっ☆ っおぉぉぉおお国が分からなくなっちゃいまひゅう～っ」

ま、まだ出るぅ☆　出てるのおぉっ☆　エラーまだまだ出ましゅぅぅ！
ばんじゃ～ぁぁあい、ばんじゃいぃぃ、ばんにゃんじゃぁんじゃあぁぁああぁい！ 
"""
    m.test(src)
    print('')

## プログラミング言語 KQ
class KQ(BrainFuck.BrainFuck):
    """プログラミング言語 KQ
    https://enpedia.rxy.jp/wiki/KQ_(%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9F%E3%83%B3%E3%82%B0%E8%A8%80%E8%AA%9E)
    """
    OPTOKEN_DICT = dict( # BrainFuck opcode and token
        nxt = ['ﾀﾞｧｲｪｽ', 'ｼｪﾘ'],
        prv = ['ｲｪｽﾀﾞｧ', 'ｼｴﾘ'],
        inc = ['ﾀﾞｧﾀﾞｧ', 'ﾀﾞｧ'],
        dec = ['ｼｪﾘｼｪﾘ', 'ﾀﾞｱ'],
        put = ['ｼｴﾘﾀﾞｧ', 'ｲｪｽ'],
        get = ['ﾀﾞｧｼｴﾘ', 'ｲｴｽ'],
        opn = ['ｼｴﾘｲｪｽ', '!'],
        cls = ['ｲｪｽｼｴﾘ', ',']
    )
    def preproc(self):
        """prepare put_buffer"""
        self.put_buffer=[]
        return True
    def op_put(self):
        """output the byte at the pointer (putchar(*ptr)).
        if the byte is not valid, store put_buffer until put_buffer is valid to be output
        """
        import locale
        try:
            self.put_buffer.append(self.cell[self.ptr].to_bytes(1, 'big'))
            sys.stdout.write(b''.join(self.put_buffer).decode(sys.getdefaultencoding()))
            self.put_buffer = []
        except UnicodeDecodeError:
            pass
        return True

def test_kq():
    k = KQ(cell_size=32)
    k.printparams()
    src = """ﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧｼｴﾘｲｪｽﾀﾞｧｲｪｽﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧｲｪｽﾀﾞｧｼｪﾘｼｪﾘｲｪｽｼｴﾘﾀﾞｧｲｪｽﾀﾞｧﾀﾞｧｼｴﾘﾀﾞｧｲｪｽﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧｼｴﾘｲｪｽﾀﾞｧｲｪｽｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｲｪｽﾀﾞｧｼｪﾘｼｪﾘｲｪｽｼｴﾘﾀﾞｧｲｪｽｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｴﾘﾀﾞｧｲｪｽﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧｼｴﾘｲｪｽﾀﾞｧｲｪｽｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｲｪｽﾀﾞｧｼｪﾘｼｪﾘｲｪｽｼｴﾘﾀﾞｧｲｪｽｼｴﾘﾀﾞｧｲｪｽﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧｼｴﾘｲｪｽﾀﾞｧｲｪｽﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧｲｪｽﾀﾞｧｼｪﾘｼｪﾘｲｪｽｼｴﾘﾀﾞｧｲｪｽｼｴﾘﾀﾞｧｲｪｽﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧｼｴﾘｲｪｽﾀﾞｧｲｪｽｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｲｪｽﾀﾞｧｼｪﾘｼｪﾘｲｪｽｼｴﾘﾀﾞｧｲｪｽｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｴﾘﾀﾞｧｲｪｽﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧｼｴﾘｲｪｽﾀﾞｧｲｪｽﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧｲｪｽﾀﾞｧｼｪﾘｼｪﾘｲｪｽｼｴﾘﾀﾞｧｲｪｽｼｴﾘﾀﾞｧｲｪｽﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧｼｴﾘｲｪｽﾀﾞｧｲｪｽﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧｲｪｽﾀﾞｧｼｪﾘｼｪﾘｲｪｽｼｴﾘﾀﾞｧｲｪｽｼｴﾘﾀﾞｧｲｪｽﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧｼｴﾘｲｪｽﾀﾞｧｲｪｽｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｲｪｽﾀﾞｧｼｪﾘｼｪﾘｲｪｽｼｴﾘﾀﾞｧｲｪｽｼｪﾘｼｪﾘｼｴﾘﾀﾞｧｲｪｽﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧｼｴﾘｲｪｽﾀﾞｧｲｪｽｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｲｪｽﾀﾞｧｼｪﾘｼｪﾘｲｪｽｼｴﾘﾀﾞｧｲｪｽｼｴﾘﾀﾞｧｲｪｽﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧｼｴﾘｲｪｽﾀﾞｧｲｪｽﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧｲｪｽﾀﾞｧｼｪﾘｼｪﾘｲｪｽｼｴﾘﾀﾞｧｲｪｽｼｴﾘﾀﾞｧｲｪｽﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧｼｴﾘｲｪｽﾀﾞｧｲｪｽｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｲｪｽﾀﾞｧｼｪﾘｼｪﾘｲｪｽｼｴﾘﾀﾞｧｲｪｽｼｪﾘｼｪﾘｼｴﾘﾀﾞｧｲｪｽﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧｼｴﾘｲｪｽﾀﾞｧｲｪｽｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｲｪｽﾀﾞｧｼｪﾘｼｪﾘｲｪｽｼｴﾘﾀﾞｧｲｪｽｼｪﾘｼｪﾘｼｴﾘﾀﾞｧｲｪｽﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧｼｴﾘｲｪｽﾀﾞｧｲｪｽﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧｲｪｽﾀﾞｧｼｪﾘｼｪﾘｲｪｽｼｴﾘﾀﾞｧｲｪｽｼｴﾘﾀﾞｧｲｪｽﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧｼｴﾘｲｪｽﾀﾞｧｲｪｽｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｲｪｽﾀﾞｧｼｪﾘｼｪﾘｲｪｽｼｴﾘﾀﾞｧｲｪｽｼｪﾘｼｪﾘｼｴﾘﾀﾞｧｲｪｽﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧｼｴﾘｲｪｽﾀﾞｧｲｪｽｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｲｪｽﾀﾞｧｼｪﾘｼｪﾘｲｪｽｼｴﾘﾀﾞｧｲｪｽｼｴﾘﾀﾞｧｲｪｽﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧｼｴﾘｲｪｽﾀﾞｧｲｪｽﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧｲｪｽﾀﾞｧｼｪﾘｼｪﾘｲｪｽｼｴﾘﾀﾞｧｲｪｽﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧｼｴﾘﾀﾞｧｲｪｽﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧｼｴﾘｲｪｽﾀﾞｧｲｪｽｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｼｪﾘｲｪｽﾀﾞｧｼｪﾘｼｪﾘｲｪｽｼｴﾘﾀﾞｧｲｪｽｼｴﾘﾀﾞｧｲｪｽﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧｼｴﾘｲｪｽﾀﾞｧｲｪｽﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧﾀﾞｧｲｪｽﾀﾞｧｼｪﾘｼｪﾘｲｪｽｼｴﾘﾀﾞｧｲｪｽｼｴﾘﾀﾞｧｲｪｽﾀﾞｧ"""
    k.test(src)
    print('')

## プログラミング言語 siro
class siro(BrainFuck.BrainFuck):
    """プログラミング言語 siro
    https://qiita.com/benisho_ga/items/50e674fded183a9e12f1
    """
    OPTOKEN_DICT = dict( # BrainFuck opcode and token
        nxt = "いーねっ！",
        inc = "おほほい",
        prv = "ｷｭｰｲ",
        dec = "ぱいーん",
        opn = "白組さん",
        cls = "救済",
        put = "なんて日だ！",
        get = "ズンドコズンドコ♪")

def test_siro():
    s = siro()
    s.printparams()
    src = """いーねっ！おほほいおほほいおほほいおほほいおほほいおほほいおほほいおほほいおほほい白組さんｷｭｰｲおほほいおほほいおほほいおほほいおほほいおほほいおほほいおほほいいーねっ！ぱいーん救済ｷｭｰｲなんて日だ！いーねっ！おほほいおほほいおほほいおほほいおほほいおほほいおほほい白組さんｷｭｰｲおほほいおほほいおほほいおほほいいーねっ！ぱいーん救済ｷｭｰｲおほほいなんて日だ！おほほいおほほいおほほいおほほいおほほいおほほいおほほいなんて日だ！なんて日だ！おほほいおほほいおほほいなんて日だ！白組さんぱいーん救済いーねっ！おほほいおほほいおほほいおほほいおほほいおほほいおほほいおほほい白組さんｷｭｰｲおほほいおほほいおほほいおほほいいーねっ！ぱいーん救済ｷｭｰｲなんて日だ！いーねっ！おほほいおほほいおほほいおほほいおほほいおほほいおほほいおほほいおほほいおほほいおほほい白組さんｷｭｰｲおほほいおほほいおほほいおほほいおほほいいーねっ！ぱいーん救済ｷｭｰｲなんて日だ！いーねっ！おほほいおほほいおほほいおほほいおほほいおほほいおほほいおほほい白組さんｷｭｰｲおほほいおほほいおほほいいーねっ！ぱいーん救済ｷｭｰｲなんて日だ！おほほいおほほいおほほいなんて日だ！ぱいーんぱいーんぱいーんぱいーんぱいーんぱいーんなんて日だ！ぱいーんぱいーんぱいーんぱいーんぱいーんぱいーんぱいーんぱいーんなんて日だ！白組さんぱいーん救済いーねっ！おほほいおほほいおほほいおほほいおほほいおほほいおほほいおほほい白組さんｷｭｰｲおほほいおほほいおほほいおほほいいーねっ！ぱいーん救済ｷｭｰｲおほほいなんて日だ！白組さんぱいーん救済おほほいおほほいおほほいおほほいおほほいおほほいおほほいおほほいおほほいおほほいなんて日だ！"""
    s.test(src)
    print('')

## プログラミング言語 Dragon Ball
class DB(BrainFuck.BrainFuck):
    """プログラミング言語 Dragon Ball
    https://spc-jpn.co.jp/blog/6657/
    """
    OPTOKEN_DICT = dict( # BrainFuck opcode and token
        nxt = 'クリリンのことかーーーっ！！！',
        inc = 'かめはめ波！！',
        prv = 'ナッパよけろーーーっ！！！',
        dec = '魔貫光殺砲！！',
        opn = 'ギャルのパンティおくれーーーっ！！！',
        cls = '戦闘力…たったの5か…ゴミめ…',
        put = 'がんばれカカロット…お前がナンバー1だ！！',
        get = 'へっ！きたねぇ花火だ')

def test_DB():
    d = DB()
    d.printparams()
    src = """かめはめ波！！かめはめ波！！かめはめ波！！かめはめ波！！かめはめ波！！ かめはめ波！！かめはめ波！！かめはめ波！！かめはめ波！！かめはめ波！！
ギャルのパンティおくれーーーっ！！！
  クリリンのことかーーーっ！！！ かめはめ波！！かめはめ波！！かめはめ波！！
  クリリンのことかーーーっ！！！ かめはめ波！！かめはめ波！！かめはめ波！！かめはめ波！！かめはめ波！！ かめはめ波！！かめはめ波！！
  クリリンのことかーーーっ！！！ かめはめ波！！かめはめ波！！かめはめ波！！かめはめ波！！かめはめ波！！ かめはめ波！！かめはめ波！！かめはめ波！！かめはめ波！！かめはめ波！！
  クリリンのことかーーーっ！！！ かめはめ波！！かめはめ波！！かめはめ波！！かめはめ波！！かめはめ波！！ かめはめ波！！かめはめ波！！かめはめ波！！かめはめ波！！かめはめ波！！ かめはめ波！！
  ナッパよけろーーーっ！！！ナッパよけろーーーっ！！！ナッパよけろーーーっ！！！ナッパよけろーーーっ！！！ 魔貫光殺砲！！
戦闘力…たったの5か…ゴミめ…
クリリンのことかーーーっ！！！クリリンのことかーーーっ！！！ 魔貫光殺砲！！魔貫光殺砲！！ がんばれカカロット…お前がナンバー1だ！！
クリリンのことかーーーっ！！！クリリンのことかーーーっ！！！ かめはめ波！！かめはめ波！！かめはめ波！！かめはめ波！！ がんばれカカロット…お前がナンバー1だ！！
ナッパよけろーーーっ！！！ 魔貫光殺砲！！魔貫光殺砲！！魔貫光殺砲！！ がんばれカカロット…お前がナンバー1だ！！
かめはめ波！！かめはめ波！！かめはめ波！！かめはめ波！！かめはめ波！！ かめはめ波！！ がんばれカカロット…お前がナンバー1だ！！
クリリンのことかーーーっ！！！ 魔貫光殺砲！！魔貫光殺砲！！魔貫光殺砲！！ がんばれカカロット…お前がナンバー1だ！！
魔貫光殺砲！！ がんばれカカロット…お前がナンバー1だ！！
ナッパよけろーーーっ！！！ナッパよけろーーーっ！！！ナッパよけろーーーっ！！！ かめはめ波！！かめはめ波！！ がんばれカカロット…お前がナンバー1だ！！
クリリンのことかーーーっ！！！ 魔貫光殺砲！！魔貫光殺砲！！ がんばれカカロット…お前がナンバー1だ！！
クリリンのことかーーーっ！！！ 魔貫光殺砲！！魔貫光殺砲！！魔貫光殺砲！！魔貫光殺砲！！魔貫光殺砲！！ 魔貫光殺砲！！がんばれカカロット…お前がナンバー1だ！！
クリリンのことかーーーっ！！！ 魔貫光殺砲！！魔貫光殺砲！！ がんばれカカロット…お前がナンバー1だ！！がんばれカカロット…お前がナンバー1だ！！"""
    
    d.test(src)
    print('')

## main for test
if __name__ == "__main__":
    test_ook()
    test_bc()
    test_cd()
    test_utu()
    test_jojo()
    test_kemono()
    test_nagato()
    test_nekomimi()
    test_nyaruko()
    test_tettette()
    test_neko()
    test_misa()
    test_kq()
    test_siro()
    test_DB()
