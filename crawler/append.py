# -*- coding: utf-8 -*-

# 將爬好的文加入原有的訓練文本內
def append_text(inputtext, outputtext):
	fh1 = open(inputtext, "r", encoding="utf-8")
	fh2 = open(outputtext, "a", encoding="utf-8")
	fh = fh1.readlines()
	for line in fh:
		fh2.write(line)
	fh1.close()
	fh2.close()
'''
formal_dcard_neg : 6997 篇
formal_dcard_pos : 6836 篇

'''
# append_text("formal_dcard_neg.txt", "neg.txt")
append_text("formal_dcard_pos.txt", "pos.txt")

# 進行情緒文本訓練
import sys
from snownlp import SnowNLP
from snownlp import sentiment

sentiment.train('neg.txt',
				'pos.txt')
sentiment.save('sentiment.marshal')
