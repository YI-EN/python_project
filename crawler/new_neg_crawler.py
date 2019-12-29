# -*- coding: utf-8 -*-
import requests
import re
import json
import emoji

header = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}

'''
Neg topics : 心累了(2997)、壓力(4763)、憂鬱(462)、鬱悶(26)、自私(157)、騙子(60).共 8365 篇
 			   forum: 心情(mood)、感情(relationship)、閒聊(talk)
 			  補：絕望、放棄
'''

'''
心情版(mood):
		12/27 15:38 232770428（自己創業真的好嗎）
感情版(relationship):
		12/27 15:37 232770397（就算是渣女-有一天也會付出代價）
閒聊版(talk):
		12/27 15:36 232770383（低卡審查帳號的方法）
'''

def check_topics(reqjson, idlist):
'''
新增: 絕望、放棄 兩詞
'''
	for article in reqjson:
		oldlist = ["心累了", "壓力", "憂鬱", "鬱悶", "自私", "騙子"]
		newlist = ["絕望", "放棄"]
		for want in newlist:
			topics = article["topics"]  # 會是一個list，若沒有則為空list
			if want in topics:
				for forgo in oldlist:
					if forgo in topics:
						break
					else:
						idlist.append(article["id"])  # 紀錄id，以便等等爬正文
						# print(article["title"])
						break  # 如果有找到了就不要繼續看，趕快檢查下一篇
				break
			else:
				pass
	return idlist

# def check_topics(reqjson, idlist):
# 	# print(idlist)
# 	# print("check_topics")
# 	for article in reqjson:
# 		for keyword in ["心累了", "壓力", "憂鬱", "鬱悶", "自私", "騙子"]:
# 			topics = article["topics"]  # 會是一個list，若沒有則為空list
# 			if keyword in topics:
# 				idlist.append(article["id"])  # 紀錄id，以便等等爬正文
# 				# print(article["title"])
# 				break  # 如果有找到了就不要繼續看，趕快檢查下一篇
# 	return idlist

def crawl_article(lastid, forum, idlist, number):
	url = "https://www.dcard.tw/_api/forums/" + forum
	url += "/posts?popular=false&before=" + str(lastid)  # 現在從他下一篇開始爬
	req = requests.get(url, headers=header)
	print(req.status_code)
	
	newjson = json.loads(req.text)
	newlist = check_topics(newjson, idlist)
	# print(newlist)
	# print("crawl_article")
	# print(len(id_list))

	number -= 1  # 每爬一頁（30個文章）就減一
	newlastid = newjson[-1]["id"]  # 這是前三十個爬文中最後一篇的id
	if number == 0:
		print("finish")
		print("last ID is : " + str(newlastid))  # number 的第 62 次發現 logical bug，故修正
		return None
	else:
		crawl_article(newlastid, forum, newlist, number)  # 如果還沒爬完指定的數量，就繼續爬

# 爬心情版(mood)/感情版(relationshop)/閒聊版(talk)
idlist = []
forum = "mood"
number = 200  # 自訂，每次會爬(30 * number)篇
crawl_article(225831060, forum, idlist, number)
print(idlist)
print(len(idlist))

# 輸出成 dcard_neg.txt  注意模式是 w 還是 a !!!!
with open(" dcard_neg.txt", "a", encoding="utf-8") as fh1:
	for Id in idlist:
		url = "https://www.dcard.tw/_api/posts/" + str(Id)
		req = requests.get(url, headers=header)
		reqjson = json.loads(req.text)
		content = reqjson["content"].split()  # content 是一個 list，裡面有一句一句話

		symbol = ".;:!？?_,$%^*(:；”“：【「】﹖」，。（）？…『』+\"\']+|[+——！（），。？、~@#￥%…&*()⋯⋯"
		pattern = ":[a-zA-Z1-3_()]+:"
		for i in range(len(content) - 1):  # 第一句到倒數第二句
			line = emoji.demojize(content[i])  # 從emoji轉成編碼
			line = re.sub(pattern, "", line).strip()  # 用regex把編碼去掉
			if line != "":
				if line[-1] in symbol:
					fh1.write(line.strip())
				else:
					fh1.write(line.strip() + ",")  # 有一些直接換行，現在分開後會沒有標點符號，幫他補上
			else:
				continue
		
		last_line = emoji.demojize(content[-1])  # 最後一句，從emoji轉成編碼
		last_line = re.sub(pattern, "", last_line).strip()  # 用regex把編碼去掉
		if last_line != "":
			if last_line[-1] in symbol:
				fh1.write(last_line.strip())
			else:
				fh1.write(last_line.strip() + "。")  # 補句號
		else:
			continue

		fh1.write("\n")  # 一編文章結束後記得換行
		# fh1.write("================")
	fh1.close()
