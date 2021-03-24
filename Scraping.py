from bs4 import BeautifulSoup
import requests
from lxml import html
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
import sys
import re

print(sys.argv)

#グーグル設定
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('Key/develop-308211-099cb82f48bc.json', scope)
#グーグル認証
gc = gspread.authorize(credentials)
# スプレッドシート設定
SPREADSHEET_KEY = '1VUWFG4P_EtbRWmz0_A6IltRICM2HOcILnoSBLlOiV1M'
worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

worksheet.update_cell(1,1, '出力します。')

to_url = sys.argv[1]#コマンド引数でURL指定
print(to_url.split("/"))
naibu_link = to_url.split("/")[2]
response = requests.get('https://alphardic.com/media/')
print(response)
print(response.url)

page_soup = BeautifulSoup(response.content, 'html.parser')
lxml_converted = html.fromstring(str(page_soup))

page_title = lxml_converted.xpath('//*[@id="st-text-logo"]/p/a')
title = page_title[0].text.replace("　","").replace(" ","").replace("\n","")
search_space = title.split(" ")
title = title.replace("\t","")

#全てのaタグを取得
a_tag_list = page_soup.find_all(["a"])

sp_tolist = []
#このページのタイトルとヘッダー
sp_tolist.append(["URL","テキスト","種別"])
sp_tolist.append([response.url,title])

for a_tag in a_tag_list:
    url = a_tag.get('href')
    naibu_check = ""
    content = a_tag.find_parents('div', id="content")
    side = a_tag.find_parents('div', id="side")
    head = a_tag.find_parents('header')
    footer = a_tag.find_parents('footer')
    footer_1 = a_tag.find_parents('div', id="footer")
    print(type(content))
    #どこの位置にあるか
    if side:
        print('side')
        locate = "side"
    elif head:
        print('head')
        locate = "head"
    elif content:
        print("content")
        locate = "content"
    elif footer or footer_1:
        print("footer")
        locate = "footer"
    else:
        print("不明")
        locate = "None"

    #外部リンクか内部リンク
    if url:
        if naibu_link in url:
            naibu_check = "内部リンク"
        else:
            naibu_check = "外部リンク"
    else:
        print(url)
    text = a_tag.get_text().replace("\n","").replace("\t","").replace(" ","")
    row_list = [url,text,naibu_check,locate]
    sp_tolist.append(row_list)


worksheet.update('A1:D1000', sp_tolist)
# worksheet.update_cell(1,1, title)

# ・ページURLとタイトルの一覧
# ・ページからの内部リンク先URLとアンカーテキスト一覧（ヘッダー、サイドバー、フッター、記事内のどこかを判別できるように）
# ・ページからの外部リンク先URLとアンカーテキスト一覧（ヘッダー、サイドバー、フッター、記事内のどこかを判別できるように）

# の抽出をお願いします。

# 吐き出しはグーグルスプレッドシートに行い、リンクを知っている全員が編集可能な状態での吐き出しをできるようにお願いします。
# フリーのGmailなどを取得してもらって、そのアカウントで吐き出すような感じでOKです。

# また、他のサイトURLを入力して調査できるようなツールとしての納品をお願いします。
# まず、応募者様のサーバー上で構築してもらえればと思います。