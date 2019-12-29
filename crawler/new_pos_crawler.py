# -*- coding: utf-8 -*-
import requests
import re
import json
import emoji

header = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}
# Pos topics : 閃光(16073) 感情版(relationship)
# 			   有趣版(funny)、曬貓版(show_cats)、寵物版(pet)
#              4000 + 3000 + 3000
'''
感情版(relationship):
		12/27 17:15 232770854（喜歡-是痛苦還是快樂的？）
有趣版(funny):
		12/29 16:24 232775039（好想睡覺可是床上有...）

'''

def check_topics(reqjson, idlist):
	# print(idlist)
	# print("check_topics")
	for article in reqjson:
		topics = article["topics"]  # 會是一個list，若沒有則為空list
		if "閃光" in topics:
			idlist.append(article["id"])  # 紀錄id，以便等等爬正文
			# print(article["title"])
			break  # 如果有找到了就不要繼續看，趕快檢查下一篇
	return idlist

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
		print("last ID is : " + str(newlastid))
		return None
	else:
		crawl_article(newlastid, forum, newlist, number)  # 如果還沒爬完指定的數量，就繼續爬

# 爬感情版(relaitionship)
idlist = []
forum = "relationship"
number = 100  # 自訂，每次會爬(30 * number)篇
crawl_article(225477814, forum, idlist, number)
print(idlist)
print(len(idlist))

# 輸出成 dcard_pos.txt  注意模式是 w 還是 a !!!!
with open("dcard_pos.txt", "a", encoding="utf-8") as fh1:
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

#=================================================================================
# def check_topics(reqjson, idlist):
# 	# print(idlist)
# 	# print("check_topics")
# 	for article in reqjson:
# 		idlist.append(article["id"])  # 紀錄id，以便等等爬正文
# 		# print(article["title"])
# 	return idlist

# def crawl_article(lastid, forum, idlist, number):
# 	url = "https://www.dcard.tw/_api/forums/" + forum
# 	url += "/posts?popular=false&before=" + str(lastid)  # 現在從他下一篇開始爬
# 	req = requests.get(url, headers=header)
# 	print(req.status_code)
	
# 	newjson = json.loads(req.text)
# 	newlist = check_topics(newjson, idlist)
# 	# print(newlist)
# 	# print("crawl_article")
# 	# print(len(id_list))

# 	number -= 1  # 每爬一頁（30個文章）就減一
# 	newlastid = newjson[-1]["id"]  # 這是前三十個爬文中最後一篇的id
# 	if number == 0:
# 		print("finish")
# 		print("last ID is : " + str(newlastid))
# 		return None
# 	else:
# 		crawl_article(newlastid, forum, newlist, number)  # 如果還沒爬完指定的數量，就繼續爬


# # 爬有趣版(funny)/寵物版(pet)
# idlist = []
# forum = "funny"
# number = 5  # 自訂，每次會爬(30 * number)篇。各需爬 3000 篇
# crawl_article(232404551, forum, idlist, number)
# print(idlist)
# print(len(idlist))

# # 輸出成 dcard_pos.txt  注意模式是 w 還是 a !!!!
# with open("dcard_pos.txt", "a", encoding="utf-8") as fh1:
# 	for Id in idlist:
# 		url = "https://www.dcard.tw/_api/posts/" + str(Id)
# 		req = requests.get(url, headers=header)
# 		reqjson = json.loads(req.text)
# 		content = reqjson["content"].split()  # content 是一個 list，裡面有一句一句話

# 		symbol = ".;:!？?_,$%^*(:；”“：【「】﹖」，。（）？…『』+\"\']+|[+——！（），。？、~@#￥%…&*()⋯⋯"
# 		pattern = ":[a-zA-Z1-3_()]+:"
# 		for i in range(len(content) - 1):  # 第一句到倒數第二句
# 			line = emoji.demojize(content[i])  # 從emoji轉成編碼
# 			line = re.sub(pattern, "", line).strip()  # 用regex把編碼去掉
# 			if line != "":
# 				if line[-1] in symbol:
# 					fh1.write(line.strip())
# 				else:
# 					fh1.write(line.strip() + ",")  # 有一些直接換行，現在分開後會沒有標點符號，幫他補上
# 			else:
# 				continue
		
# 		last_line = emoji.demojize(content[-1])  # 最後一句，從emoji轉成編碼
# 		last_line = re.sub(pattern, "", last_line).strip()  # 用regex把編碼去掉
# 		if last_line != "":
# 			if last_line[-1] in symbol:
# 				fh1.write(last_line.strip())
# 			else:
# 				fh1.write(last_line.strip() + "。")  # 補句號
# 		else:
# 			continue

# 		fh1.write("\n")  # 一編文章結束後記得換行
# 		# fh1.write("================")
# 	fh1.close()
