# -*- coding: utf-8 -*-
import requests  # 對dcard爬文(api)
import json  # 以json形式處理文章
import re  # 處理正規表達式
import emoji  # 處理現代網路文章表情符號過多，可能影響判讀的因素
import time  # 延遲爬取文章，因dcard會阻止使用者連續爬取

header = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}

def check_topics(reqjson, idlist):
	'''
	檢查文章內是否具有我們要的標籤，有則將文章id計入list中，以便下載內文
	'''
	for article in reqjson:
		for keyword in ["心累了", "壓力", "憂鬱", "鬱悶", "自私", "騙子"]:
			topics = article["topics"]  # 會是一個list，若沒有則為空list
			if keyword in topics:
				idlist.append(article["id"])  # 紀錄id，以便等等爬正文
				break  # 如果有找到了就不要繼續看，趕快檢查下一篇
	return idlist

def crawl_article(lastid, forum, idlist, number):
	'''
	運用check_topics函數搜集的列表搜集內文。dcard的api設定每次只能爬取30篇，
	因此將最後一篇文章的id存為lastid，當作爬取下一輪的第一個id（運用api url 中的參數before）
	'''
	url = "https://www.dcard.tw/_api/forums/" + forum
	url += "/posts?popular=false&before=" + str(lastid)
	req = requests.get(url, headers=header)
	print(req.status_code)
	
	# 將爬取的資料用json解析，並使用check_topic得出符合規則的文章
	newjson = json.loads(req.text)
	newlist = check_topics(newjson, idlist)

	# 用來限制文章的爬取數量（因為dcard會阻止用戶連續爬取）
	number -= 1  # 每爬一頁（30個文章）就減一
	newlastid = newjson[-1]["id"]  # 這是前三十個爬文中最後一篇的id，這個id將會被當作爬取下一輪的第一個id（運用api url 中的參數before）
	
	if len(idlist) >= 500:  # 每取得300篇文章就結束
		return None
	else:
		if number == 0:
			# 每爬完30 * number篇文章，休息60秒，再繼續爬
			time.sleep(60)
			number = 100
			crawl_article(newlastid, forum, newlist, number)
		else:
			# 如果還沒爬完number指定的數量，便不間斷地持續爬取，直到number歸0為止
			crawl_article(newlastid, forum, newlist, number)


# 爬心情版(mood)/感情版(relationship)/閒聊版(talk)
# 會依據爬取的狀況更改各項數值
idlist = []
forum = "mood"
number = 100  # 每次會爬(30 * number)篇(3000篇)
crawl_article(232770428, forum, idlist, number)
print(idlist)
print(len(idlist))

# 輸出成 dcard_neg.txt  注意模式是 w 還是 a !!!!
with open("dcard_neg.txt", "a", encoding="utf-8") as fh1:
'''
利用爬取的idlist（符合規定的文章id），抓取文章內文，分兩次做（記id與抓內文）的原因
是因為兩者所需的url格式不同。抓下內文後，經過regex的處理去掉不要的網址、emoji等後
將其寫入至一個txt檔中
'''
	for Id in idlist:
		url = "https://www.dcard.tw/_api/posts/" + str(Id)
		req = requests.get(url, headers=header)
		reqjson = json.loads(req.text)
		content = reqjson["content"].split()  # content 是一個 list，裡面有一句一句話

		# 此處是要利用正規表達式，去除文章內不符合中文書寫模式的符號、emoji、網址、分隔線
		symbol = ".;:!？?_,$%^*(:；”“：【「】﹖」，。（）？…『』+\"\']+|[+——！（），。？、~@#￥%…&*()⋯⋯"
		pattern1 = ":[a-zA-Z1-3_()-]+:"  # 去除emoji的unicode
		pattern2 = "http[a-zA-Z0-9_()-./:%]+"  # 去除網址
		pattern3 = "[—-][—-][—-]+"  # 去除分隔線
		for i in range(len(content) - 1):  # 第一句到倒數第二句
			line = emoji.demojize(content[i])  # 此method會將emoji從圖形轉成unicode編碼
			line = re.sub(pattern1, "", line).strip()  # 去除emoji的unicode
			line = re.sub(pattern2, "", line).strip()  # 去除網址
			line = re.sub(pattern3, "", line).strip()  # 去除分隔線
			if line != "":
				if line[-1] in symbol:
					fh1.write(line.strip())
				else:
					fh1.write(line.strip() + ",")  # 現代網路文章有些不會打標點符號，而是直接換行，現在幫他補上
			else:
				continue
		
		last_line = emoji.demojize(content[-1])  # 最後一句，從emoji轉成編碼
		last_line = re.sub(pattern, "", last_line).strip()  # 用regex把編碼去掉
		if last_line != "":
			if last_line[-1] in symbol:
				fh1.write(last_line.strip())
			else:
				fh1.write(last_line.strip() + "。")  # 因最後一句，故補句號
		else:
			continue

		fh1.write("\n")  # 一篇文章結束後記得換行
		# fh1.write("================")
	fh1.close()

# 進行情緒文本訓練
import sys
from snownlp import SnowNLP
from snownlp import sentiment

sentiment.train('neg.txt',
				'pos.txt')
sentiment.save('sentiment.marshal')

