#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from time import sleep

def livedoor_server():
	#アクセス先のURL
	access_url = "http://news.livedoor.com/"

	res = requests.get(access_url)
	soup = BeautifulSoup(res.text, 'lxml')
	#print(soup)

	#ファイル名
	now_time = datetime.now().strftime("%Y%m%d_%H_%M_%S")
	out_put = "livedoor_"+str(now_time)+".txt" 

	with open(out_put, mode='a', encoding='utf-8') as f:
		for line in soup.find_all("a", class_="rewrite_ab"):
			if not line.string is None:
				#print(line.string)
				article_url = line.get("href")
				#記事詳細ページへのURLへ一部変更
				article_url = article_url.replace('topics','article')
				#print(article_url)

				article_res = requests.get(article_url)
				article_soup = BeautifulSoup(article_res.text, 'lxml')

				for article_line in article_soup.find_all("span", itemprop="articleBody"):
					text = ""
					for article_text in article_line.find_all("p"):
						if not article_text.string is None:
							text += article_text.string
					#print(text)

				if text != "":
					f.write(text+"\n")

	now_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
	print(str(access_url)+" : "+now_time)