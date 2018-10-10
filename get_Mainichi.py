#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from time import sleep

def mainichi_server():
	#アクセス先のURL
	access_url = "https://mainichi.jp/"

	res = requests.get(access_url)
	soup = BeautifulSoup(res.text, 'lxml')
	#print(soup)

	#ファイル名
	now_time = datetime.now().strftime("%Y%m%d_%H_%M_%S")
	out_put = "mainichi_"+str(now_time)+".txt" 

	with open(out_put, mode='a', encoding='utf-8') as f:
		#href属性に「//mainichi.jp/articles」を含むリンクを取得
		for line in soup.find_all(href=re.compile("//mainichi.jp/articles")):
			article_href = line.get("href")
			if not "http:" or not "https:" in article_href:
				article_url = "http:"+article_href
			else:
				article_url = article_href
			#print(article_url)
			article_res = requests.get(article_url)
			article_soup = BeautifulSoup(article_res.text, 'lxml')

			#タグ<p>かつclassがtxtで抽出
			article_text = ""
			for article_line in article_soup.find_all("p", class_="txt"):
				#　記事本文だけ出力
				if not article_line.string is None:
					if not "…" in article_line.string:
						article_text += article_line.string
			#print(article_text)
			article_text = article_text.replace('\r\n','')
			if article_text != "":
				f.write(article_text+"\n")
	now_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
	print(str(access_url)+" : "+now_time)