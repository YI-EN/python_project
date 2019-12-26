# -*- coding: utf-8 -*-
import requests
import re
import json
import emoji

# Neg topics : 心累了(2997)、壓力(4763)、憂鬱(462)、鬱悶(26)、自私(157)、騙子(60).共 8365 篇
# 			   forum: 心情(mood)、感情(relationship)、閒聊(talk)
header = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}


def find_neg_article_id(neg_id_list, json):
	for content in json:
		for keyword in ["心累了", "壓力", "憂鬱", "鬱悶", "自私", "騙子"]:
			if keyword in content["topics"]:
				neg_id_list.append(content["id"])  # 未爆彈，要處理
				print(content["title"])
				break
	return neg_id_list

def find_the_neg_last_id_loop(number, neg_id_list, forum, reqjson):
	last_id = reqjson[-1]["id"]

	url = "https://www.dcard.tw/_api/forums/" + forum
	url += "/posts?popular=false&before=" + str(last_id)

	req = requests.get(url, headers=header)
	print(req.status_code)
	reqjson = json.loads(req.text)
	
	neg_id_list = find_neg_article_id(neg_id_list, reqjson)
	
	print(len(neg_id_list))

	number -= 1
	if number == 0:
		return neg_id_list
	else:
		find_the_neg_last_id_loop(number, neg_id_list, forum, reqjson)


neg_id_list = []
amount_of_id_in_each_forum = []
for forum in ["mood", "relationship", "talk"]:
	number = 1000
	url = "https://www.dcard.tw/_api/forums/" + forum
	url += "/posts?popular=false"

	req = requests.get(url)
	print(forum)
	print(req.status_code)

	reqjson = json.loads(req.text)

	neg_id_list = find_neg_article_id(neg_id_list, reqjson)
	find_the_neg_last_id_loop(number, neg_id_list, forum, reqjson)

	amount_of_id_in_each_forum.append(len(neg_id_list))


print(neg_id_list)

# 輸出成 dcard_neg.txt
with open(" dcard_neg.txt", "w", encoding="utf-8") as fh1:
	
	for article_id in neg_id_list:
		url = "https://www.dcard.tw/_api/posts/" + str(article_id)
		req = requests.get(url)
		reqjson = json.loads(req.text)
		article = reqjson["content"].split()  # article 是一個 list

		# fh1.write(str(article_id))
		
		symbol = ".;:!？?_,$%^*(:；”“：【「】﹖」，。（）？…『』+\"\']+|[+——！（），。？、~@#￥%…&*()⋯⋯"
		pattern = ":[a-zA-Z1-3_()]+:"
		for i in range(len(article) - 1):
			line = emoji.demojize(article[i])
			# line = article[i]
			line = re.sub(pattern, "", line).strip()
			if line != "":
				if line[-1] in symbol:
					fh1.write(line.strip())
				else:
					fh1.write(line.strip() + ",")
			else:
				continue
		
		last_line = emoji.demojize(article[-1])
		# last_line = article[-1]
		last_line = re.sub(pattern, "", last_line).strip()
		if last_line != "":
			if last_line[-1] in symbol:
				fh1.write(last_line.strip())
			else:
				fh1.write(last_line.strip() + "。")
		else:
			continue

		fh1.write("\n")
		# fh1.write("================")

	for amount in amount_of_id_in_each_forum:
		fh1.write(str(amount) + "\n")
	fh1.close()


# Pos topics : 閃光(16073) 感情版(relationship)
# 			   有趣版(funny)、曬貓版(show_cats)、寵物版(pet)
#              4000+3000+3000


def find_pos_article_id(pos_id_list, reqjson):
	for content in reqjson:
		for keyword in ["閃光"]:
			if keyword in content["topics"]:
				pos_id_list.append(content["id"])  # 未爆彈，要處理
				print(content["title"])
				break
	return pos_id_list

def find_the_pos_last_id_loop(pos_id_list, forum, reqjson):
	last_id = reqjson[-1]["id"]

	url = "https://www.dcard.tw/_api/forums/" + forum
	url += "/posts?popular=false&before=" + str(last_id)

	req = requests.get(url, headers=header)
	print(req.status_code)
	reqjson = json.loads(req.text)
	
	pos_id_list = find_pos_article_id(pos_id_list, reqjson)
	
	print(len(pos_id_list))

	if len(pos_id_list) >= 4000:  # should be 4000
		return pos_id_list
	else:
		find_the_pos_last_id_loop(pos_id_list, forum, reqjson)


pos_id_list = []
forum = "relationship"
url = "https://www.dcard.tw/_api/forums/" + forum
url += "/posts?popular=false"

req = requests.get(url)
print(forum)
print(req.status_code)

reqjson = json.loads(req.text)
pos_id_list = find_pos_article_id(pos_id_list, reqjson)
find_the_pos_last_id_loop(pos_id_list, forum, reqjson)
print(pos_id_list)


def find_pos_article_id_in_a_single_forum(pos_id_list, reqjson):
	for content in reqjson:
		pos_id_list.append(content["id"])  # 未爆彈，要處理
		print(content["title"])
		break
	return pos_id_list

def find_article_in_a_single_forum(number, pos_id_list, forum, reqjson):
	last_id = reqjson[-1]["id"]

	url = "https://www.dcard.tw/_api/forums/" + forum
	url += "/posts?popular=false&before=" + str(last_id)

	req = requests.get(url, headers=header)
	print(req.status_code)
	reqjson = json.loads(req.text)
	
	pos_id_list = find_pos_article_id_in_a_single_forum(pos_id_list, reqjson)
	print(len(pos_id_list))

	number -= 1
	if number == 0:
		return pos_id_list
	else:
		find_article_in_a_single_forum(number, pos_id_list, forum, reqjson)


for forum in ["funny", "relationship"]:
	number = 100  # should be 100 s.t. 30 * 100 = 3000
	url = "https://www.dcard.tw/_api/forums/" + forum
	url += "/posts?popular=false"

	req = requests.get(url)
	print(forum)
	print(req.status_code)
	reqjson = json.loads(req.text)

	pos_id_list = find_pos_article_id_in_a_single_forum(pos_id_list, reqjson)
	find_article_in_a_single_forum(number, pos_id_list, forum, reqjson)
print(pos_id_list)


# 輸出成 dcard_pos.txt
with open(" dcard_pos.txt", "w", encoding="utf-8") as fh1:
	
	for article_id in pos_id_list:
		url = "https://www.dcard.tw/_api/posts/" + str(article_id)
		req = requests.get(url)
		reqjson = json.loads(req.text)
		article = reqjson["content"].split()  # article 是一個 list

		# fh1.write(str(article_id))
		
		symbol = ".;:!？?_,$%^*(:；”“：【「】﹖」，。（）？…『』+\"\']+|[+——！（），。？、~@#￥%…&*()⋯⋯"
		pattern = ":[a-zA-Z1-3_()]+:"
		for i in range(len(article) - 1):
			line = emoji.demojize(article[i])
			# line = article[i]
			line = re.sub(pattern, "", line).strip()
			if line != "":
				if line[-1] in symbol:
					fh1.write(line.strip())
				else:
					fh1.write(line.strip() + ",")
			else:
				continue
		
		last_line = emoji.demojize(article[-1])
		# last_line = article[-1]
		last_line = re.sub(pattern, "", last_line).strip()
		if last_line != "":
			if last_line[-1] in symbol:
				fh1.write(last_line.strip())
			else:
				fh1.write(last_line.strip() + "。")
		else:
			continue

		fh1.write("\n")
	fh1.write(str(len(pos_id_list)))
		# fh1.write("================")
	fh1.close()
# header = {
#     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
# }

# url = "https://www.dcard.tw/_api/forums/mood/posts?popular=false"
# req = requests.get(url, headers=header)
# print(req.content.decode())
# print(req.status_code)


