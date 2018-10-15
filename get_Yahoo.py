#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from time import sleep

def yahoo_server():
	#アクセス先のURL
	access_url = "https://news.yahoo.co.jp/"

	res = requests.get(access_url)
	soup = BeautifulSoup(res.text, 'lxml')
	#print(soup)

	#ファイル名
	now_time = datetime.now().strftime("%Y%m%d_%H_%M_%S")
	out_put = "yahoo_"+str(now_time)+".txt" 

	with open(out_put, mode='a', encoding='utf-8') as f:
		article_url_list = []
		# 記事のリンク獲得
		for line in soup.find_all(["p", "h1"], class_="ttl"):
			for in_line in line.find_all("a"):
				article_url_list.append(in_line.get("href"))

		#  「もっと見る」、「全カテゴリのトピックス一覧」を獲得.
		more_look_url = soup.find("p", class_="more").find("a").get("href")
		all_topic_url = soup.find("p", class_="alltopi").find("a").get("href")
		
		more_res = requests.get(more_look_url)
		more_soup = BeautifulSoup(more_res.text, 'lxml')

		# 「もっと見る」のページでURLを拾う
		for line in more_soup.find_all("li", class_="ListBoxwrap"):
			for in_line in line.find_all("a"):
				article_url_list.append(in_line.get("href"))

		all_topic_res = requests.get(all_topic_url)
		all_topic_soup = BeautifulSoup(all_topic_res.text, 'lxml')

		# 「トピックス一覧」のページでURLを拾う
		num = 1
		for line in all_topic_soup.find_all("div", class_="list"):
			for in_line in line.find_all("ul"):
				for in_in_line in in_line.find_all("li", class_=""):
					for in_in_in_line in in_in_line.find_all("a"):
						#print(str(num)+":"+str(in_in_in_line.get("href")))
						#num += 1
						article_url_list.append(in_in_in_line.get("href"))

		#setによって重複するURLを削除する
		article_url_set = list(set(article_url_list))
		#print(article_url_set)

		for url in article_url_set:
			article_res = requests.get(url)
			article_soup = BeautifulSoup(article_res.content, 'lxml')

			article_url = article_soup.find("a", class_="newsLink")
			article_href = article_url.get("href")
			#print(article_href)

			#単純な地震の震度情報などはスキップ
			if "emergency-weather" in article_href:
				continue

			if article_href is None:
				article_text = article_soup.find_all("p", class_="hbody")
			else :
				article_url_res = requests.get(article_href)
				article_url_soup = BeautifulSoup(article_url_res.content, 'lxml')
				article_place = article_url_soup.find("p", class_="ynDetailText yjDirectSLinkTarget")

				#本文がない場合、映像メインの記事の可能性あり
				if(article_place is None):
					article_place = article_url_soup.find("div", class_=["yjDirectSLinkTarget", "bd"])
				#print(article_place.text)
				article_text = article_place.text
			#print(article_text)
			article_text = article_text.replace('\n','')
			f.write(str(article_href)+"\t"+str(article_text)+"\n")
		#f.write(str(soup))

	now_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
	print(str(access_url)+" : "+now_time)