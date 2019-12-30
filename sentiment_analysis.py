#coding:UTF-8
import sys
from snownlp import SnowNLP
from snownlp import sentiment

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



text = u"氣氛開始轉換，突然一股溫熱從我耳後散開。"

s = SnowNLP(text)

for sentence in s.sentences:
	print(sentence)

print(s.sentiments)
print(s.words)


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


