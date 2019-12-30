# -*- coding: utf-8 -*-
# def append_text(inputtext, outputtext):
# 	fh1 = open(inputtext, "r", encoding="utf-8")
# 	fh2 = open(outputtext, "a", encoding="utf-8")
# 	fh = fh1.readlines()
# 	for line in fh:
# 		fh2.write(line)
# 	fh1.close()
# 	fh2.close()

# append_text("dict.txt", "data.txt")


'''
中文分詞訓練庫
一開始遇到：ValueError: too many values to unpack (expected 2)
刪除含符號（顏文字等）後即可運行
'''
from snownlp import seg
seg.train('data.txt')
seg.save('seg.marshal')



