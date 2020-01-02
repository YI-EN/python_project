#coding:UTF-8
import sys
from snownlp import SnowNLP
from snownlp import sentiment
import emoji
import re

# sentiment.train('./crawler/formal_dcard_neg.txt',
# 				'./crawler/formal_dcard_pos.txt')
# sentiment.save('sentiment.marshal')


# f = open("neg.txt", "r", encoding="utf-8")

# f = f.read()
# s = SnowNLP(f)
# for sentence in s.sentences:
# 	print(sentence)
# print(s.sentiments)

# while True:
# 	line = f.readline()
# 	line = line.strip()

all_post = ["現在的我，想開了看淡了，什麼事情都是一句：算了！", "乾 跨年不就是要跟一群魯肥宅一起耍廢嗎 怎麼每年年底都在趕專案啊啊啊", "debug底到快瘋了啦幹"]


adjusted_list = []
for article in all_post:
    text = ""
    content = article.split("\n")  # content 是一個 list，裡面有一句一句話

    symbol = ".;:!？?_,$%^*(:；”“：【「】﹖」，。（）？…『』+\"\']+|[+——！（），。？、~@#￥%…&*()⋯⋯"
    pattern1 = ":[a-zA-Z1-3_()-]+:"  # 新增 "-" 修正先前的 demojize
    pattern2 = "http[a-zA-Z0-9_()-./:%]+"  # 去網址
    pattern3 = "[—-][—-][—-]+"  # 處理分隔線
    for i in range(len(content) - 1):  # 第一句到倒數第二句
        line = emoji.demojize(content[i])  # 從emoji轉成編碼
        line = re.sub(pattern1, "", line).strip()  # 用regex把編碼去掉
        line = re.sub(pattern2, "", line)
        line = re.sub(pattern3, "", line)
        line = re.sub(",", "，", line)  # 發現 snownlp 的斷句只會斷中文標點符號
        line = re.sub("!", "！", line)
        line = re.sub(":", "：", line)
        if line != "":
            if line[-1] in symbol:
                text += line.strip()
            else:
                text += line.strip() + "，"  # 有一些直接換行，現在分開後會沒有標點符號，幫他補上
        else:
            continue
        
    last_line = emoji.demojize(content[-1])  # 最後一句，從emoji轉成編碼
    last_line = re.sub(pattern1, "", last_line).strip()  # 用regex把編碼去掉
    last_line = re.sub(pattern2, "，", last_line)
    last_line = re.sub(pattern3, "", last_line)
    last_line = re.sub(",", "，", last_line)  # 發現 snownlp 的斷句只會斷中文標點符號
    last_line = re.sub("!", "！", last_line)
    last_line = re.sub(":", "：", last_line)
    if last_line != "":
        if last_line[-1] in symbol:
            text = last_line.strip()
        else:
            text = last_line.strip() + "。"  # 補句號
        adjusted_list.append(text)
    else:
        continueindexsum = 0
number = 0
alist = []
for text in adjusted_list:
    s = SnowNLP(text)
    print(text)
    alist.append(s.sentiments)
print(alist)

# #coding:UTF-8
# import sys
# from snownlp import SnowNLP

# def read_and_analysis(input_file, output_file):
# 	f = open(input_file, "r", encoding="utf-8")
# 	fw = open(output_file, "w", encoding="utf-8")
# 	while True:
# 		line = f.readline()
# 		print(line)
# 		if not line:
# 			break
# 		line = line.strip()

# 		s = SnowNLP(line)
# 		# s.words 查询分词结果
# 		seg_words = ""
# 		for x in s.words:
# 			seg_words += "_"
# 			seg_words += x
# 			print(seg_words)
# 		# s.sentiments 查询最终的情感分析的得分
# 		fw.write(line + "\t" + seg_words + "\t" + str(s.sentiments) + "\n")
# 	fw.close()
# 	f.close()

# # if __name__ == "__main__":
# #   input_file = sys.argv[1]
# #   output_file = sys.argv[2]
# input_file = "neg.txt"
# output_file = "sentiments_try.txt"
# read_and_analysis(input_file, output_file)


