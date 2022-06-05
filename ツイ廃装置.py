from dataclasses import replace
from http.client import responses
from itertools import count
import tkinter, tkinter.messagebox as tk 
import tkinter.font as f
from functools import partial
import sys
from unittest import result
from urllib import response
import tweepy
import urllib.request
import requests
import re
import datetime

#Tkinterメインウィンドウコード
tki = tkinter.Tk()
tki.geometry('280x250')
tki.title("ついはい")
tki.resizable(0,0)
dt_now = str(datetime.datetime.now())

#APIKey--対応するキーを "" で囲む
Consumer = ""
ConsumerSecret = ""
AccessToken = ""
AccessTokenSecret = ""
client = tweepy.Client(
    consumer_key=Consumer, consumer_secret=ConsumerSecret, access_token=AccessToken, access_token_secret=AccessTokenSecret
    )

#オンライン判定
#Twitterへの接続をリクエストして失敗ならexceptへ。成功ならelseへ
try:
    respose = requests.get('https://twitter.com')
    respose.raise_for_status()
except requests.exceptions.RequestException as e:
    print(dt_now + "  ConnectionERROR")
    tkinter.messagebox.showerror(
        "警告", "twitter.comに接続できません。\nインターネットの状態を確認してください。")
    tki.destroy()

else:
#テキストボックスを設置する。
#ifconfigへ接続しIPアドレスを取得。失敗ならexceptへ（処理続行）
    box = tkinter.Text(font=('', 16))
    box.place(x=40, y=40, width=200, height=68)
    try:
        ip = urllib.request.urlopen('https://ifconfig.me').read().decode('utf8')
        lbl = tkinter.Label(tki, text="Global IP:" + ip)
        lbl.place(x=110, y=10)
    except Exception as e:
        print(dt_now + "IPGETERROR")
        lbl = tkinter.Label(tki, text="Global IP:" + "不明")
        lbl.place(x=160, y=10)


def test():
    sendtext = str(box.get("1.0", "end -1c"))
    count = len(
        sendtext.replace("　", "").replace(" ", "").replace("\n", "").replace("\t", "").replace("\v", "")
            )
    print(count)
    if 140 >= count > 0 :
        try :
            respose = requests.get('https://twitter.com')
            respose.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(dt_now + "  ConnectionERROR")
            tkinter.messagebox.showerror(
                "警告", "twitter.comに接続できません。\nインターネットの状態を確認してください。")
        else: #ツイート成功パターン
            tweet = str(box.get("1.0", "end -1c"))
            client.create_tweet(text=tweet)
            print(dt_now + "  OK")
            tkinter.messagebox.showinfo("おしらせ", "ツイートしました")
            box.delete("1.0", "end -1c")
    else:
        if count == 0:
            print(dt_now + "  Word Count (=0) ERROR")
            tkinter.messagebox.showerror(
                "警告", "文字が入力されていないためツイートできません。")
            box.delete("1.0", "end -1c")
        else:
            mojisu = len(str(box.get("1.0", "end -1c"))) - 141
            print(dt_now + "Word Count (over" + str(mojisu) + ")Error")
            #tkinter.messagebox.showerror(
               # "警告", "文字数超過のためツイートできません。\nあと" + str(mojisu) + " 減らしてください")
            #box.delete("1.0", "end -1c")


def baind(self):
    tki.after(1, test)

btn = tkinter.Button(
   tki, text='ツイート', command = test, width= 27, height = 3, bd = 2)
#func = partial(test, btn, 0 ,0)
btn.place(x=40, y=130)

tkinter.Button.bind(tki, "<Control-Key-Return>", baind)

tki.mainloop()