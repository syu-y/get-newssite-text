#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from time import sleep

def sankei_server():
	#アクセス先のURL
	access_url = "http://www.sankei.com/"

	res = requests.get(access_url)
	soup = BeautifulSoup(res.text, 'lxml')
	#print(soup)

	#ファイル名
	now_time = datetime.now().strftime("%Y%m%d_%H_%M_%S")
	out_put = "sankei_"+str(now_time)+".txt" 

	date = datetime.now().strftime("%y%m%d")

	article_url_list = []
	with open(out_put, mode='a', encoding='utf-8') as f:
		find_tag = "news/"+str(date)
		for line in soup.find_all(href=re.compile(find_tag)):
			# hrefの獲得と記事URLへの修正
			article_url = line.get("href")
			article_url = article_url.replace('./', access_url)
			#URLが重複する可能性があるのでいったんリストへ格納
			article_url_list.append(article_url)

		#setによって重複するURLを削除する
		article_url_set = list(set(article_url_list))
		#URLへアクセス
		for url in article_url_set:
			article_res = requests.get(url)
			article_soup = BeautifulSoup(article_res.text, 'lxml')

			article_text = ""
			for article_line in article_soup.find_all("div", class_="fontMiddiumText"):
				for in_line in article_line.find_all("p", class_=""):
					#print(in_line.string)
					if not in_line.string is None:
						article_text += in_line.string
			f.write(str(article_text+"\n"))

	now_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
	print(str(access_url)+" : "+now_time)