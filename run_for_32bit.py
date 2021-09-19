#-*- coding:utf-8 -*-

from ctypes import (
    WinDLL,
    c_char_p,
    c_int,
    c_wchar_p,
    wintypes,
)

import re
from os.path import abspath

J2K_ENGINE_H_DLL = abspath('.\\utils\\J2KEngine.dll')
DAT_DIRECTORY = abspath('.\\utils\\Dat\\')


class TranslateEngine:

    def __init__(self):
        self.LoadDLL = WinDLL(J2K_ENGINE_H_DLL)

        self.Engine = self.LoadDLL.J2K_InitializeEx
        self.Engine.argtypes = [c_char_p, c_char_p]
        self.Engine.restype = wintypes.BOOL

        self.Translate = self.LoadDLL.J2K_TranslateMMNTW

        self.Translate.argtypes = [c_int, c_wchar_p]
        self.Translate.restype = c_wchar_p

        self.StartTranslate = self.Engine('CSUSER123455'.encode(), DAT_DIRECTORY.encode())

        

    def DecodeText(self, japanese: str):
        chars = "↔◁◀▷▶♤♠♡♥♧♣⊙◈▣◐◑▒▤▥▨▧▦▩♨☏☎☜☞↕↗↙↖↘♩♬㉿㈜㏇™㏂㏘＂＇∼ˇ˘˝¡˚˙˛¿ː∏￦℉€㎕㎖㎗ℓ㎘㎣㎤㎥㎦㎙㎚㎛㎟㎠㎢㏊㎍㏏㎈㎉㏈㎧㎨㎰㎱㎲㎳㎴㎵㎶㎷㎸㎀㎁㎂㎃㎄㎺㎻㎼㎽㎾㎿㎐㎑㎒㎓㎔Ω㏀㏁㎊㎋㎌㏖㏅㎭㎮㎯㏛㎩㎪㎫㎬㏝㏐㏓㏃㏉㏜㏆┒┑┚┙┖┕┎┍┞┟┡┢┦┧┪┭┮┵┶┹┺┽┾╀╁╃╄╅╆╇╈╉╊┱┲ⅰⅱⅲⅳⅴⅵⅶⅷⅸⅹ½⅓⅔¼¾⅛⅜⅝⅞ⁿ₁₂₃₄ŊđĦĲĿŁŒŦħıĳĸŀłœŧŋŉ㉠㉡㉢㉣㉤㉥㉦㉧㉨㉩㉪㉫㉬㉭㉮㉯㉰㉱㉲㉳㉴㉵㉶㉷㉸㉹㉺㉻㈀㈁㈂㈃㈄㈅㈆㈇㈈㈉㈊㈋㈌㈍㈎㈏㈐㈑㈒㈓㈔㈕㈖㈗㈘㈙㈚㈛ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓧⓨⓩ①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⒜⒝⒞⒟⒠⒡⒢⒣⒤⒥⒦⒧⒨⒩⒪⒫⒬⒭⒮⒯⒰⒱⒲⒳⒴⒵⑴⑵⑶⑷⑸⑹⑺⑻⑼⑽⑾⑿⒀⒁⒂"
        for c in chars:
            if c in japanese:
                japanese = japanese.replace(c, f'\\u{str(hex(ord(c)))[2:]}')
        return japanese



    def EncodeText(self, japanese: str):
        return str(
            re.sub(
                r'(?i)(?<!\\)(?:\\\\)*\\u([0-9a-f]{4})',
                lambda m: chr(int(m.group(1), 16)),
                japanese
            )
        )



    def RunTranslate(self, japanese: str):
        return self.EncodeText(
            self.Translate(
                0,
                self.DecodeText(japanese)
            )
        )






if __name__ == '__main__':
    t = TranslateEngine()
    translated_text = t.RunTranslate('長いです、しかも地の文が多すぎて読みにくいです。')
    print(translated_text) # print "깁니다, 게다가 지문이 너무 많아서 읽기 어렵습니다."


