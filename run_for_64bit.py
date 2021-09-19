from msl.loadlib import Client64
from ctypes import c_wchar_p

class MyClient(Client64):

    def __init__(self):
        super(MyClient, self).__init__(module32='my_server')

    def translate(self, text: str):
        return self.request32('RunTranslate', text ) 

    


if __name__ == '__main__':
    c = MyClient()
    translated_text = c.translate("長いです、しかも地の文が多すぎて読みにくいです。") 
    print(translated_text) # print any int???
