# -*- coding: utf-8 -*-
import re

pattern1 = ":[a-zA-Z1-3_()-]+:"  # 新增 "-" 修正先前的 demojize
pattern2 = "http[a-zA-Z0-9_()-./:%]+"  # 去網址
pattern3 = "[—-][—-][—-]+"  # 處理分隔線
# symbol = ".;:$%^*(:；”“：【「】﹖」，。（）？…『』+\"\']+|[+——！（），。？、~@#￥%…&*()⋯⋯"

# inputtext = "dcard_neg.txt"/"dcard_pos.txt"
# outputtext = "formal_dcard_neg.txt"/formal_dcard_pos.txt
def remove_url(inputtext, outputtext):
	fh1 = open(inputtext, "r", encoding="utf-8")
	fh2 = open(outputtext, "w", encoding="utf-8")
	fh = fh1.readlines()
	for line in fh:
		line = re.sub(pattern1, "", line)
		line = re.sub(pattern2, "，", line)
		line = re.sub(pattern3, "", line)
		line = re.sub(",", "，", line)  # 發現 snownlp 的斷句只會斷中文標點符號
#		line = re.sub("?", "？", line)
		line = re.sub("!", "！", line)
		line = re.sub(":", "：", line)

		fh2.write(line)
	fh1.close()
	fh2.close()

remove_url("dcard_neg.txt", "formal_dcard_neg.txt")




