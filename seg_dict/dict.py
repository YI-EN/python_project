# -*- coding: utf-8 -*-
import csv

'''
同時仍然可以訓練分詞：seg

看到在同一個目錄下，有個data.txt，這個就是訓練的樣本，開啟樣本可以發現：
邁/b 向/e 充/b 滿/e 希/b 望/e 的/s 新/s 世/b 紀/e中/b 共/m 中/m 央/e 總/b 書/m 記/e
其中b代表begin，m代表middle，e代表end，分別代表一個詞語的開始，中間詞和結尾，s代表single，一個字是一個詞的意思。
將訓練樣本放入data1.txt中，進行訓練：
seg.train('data1.txt')
如果下次還需要使用的話，將結果保留到seg2.marshal當中，使用的時候只要更改data_path改為seg2.marshal的路徑即可

參考網址：https://www.itread01.com/content/1544379321.html
'''

csvfile = open("senti_dict.csv", "r")
rows = csv.DictReader(csvfile)

fh1 = open("dict.txt", "w", encoding="utf-8")
number = 0
for row in rows:
	word = row["lemma"].strip()
	print(word)
	print(len(word))
	if len(word) == 0:
		continue
	elif len(word) == 1:
		segword = word[0] + "/" + "s "
	elif len(word) == 2:
		segword = word[0] + "/" + "b "
		segword += word[-1] + "/" + "e "
	elif len(word) >= 3:
		segword = word[0] + "/" + "b "
		for i in range(1, len(word) - 1):
			segword += word[i] + "/" + "m "
		segword += word[-1] + "/" + "e "

	number += 1
	if number % 100 != 0:
		fh1.write(segword + "，/s ")
	else:
		fh1.write(segword + "。/s" + "\n")
fh1.close()
