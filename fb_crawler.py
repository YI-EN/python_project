# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests, time
from selenium import webdriver
 
USERNAME="tienchu_liu@yahoo.com.tw"  # input("USERNAME:")
PASSWORD="klay11curry30"  # ("PASSWORD:")
link="https://www.facebook.com/vivianchao02?__tn__=%2CdC-R-R&eid=ARCoSj3S4Eew0_z4nlTvmQvnlhmM_IrsBKGuvv-03cG9U3PXHZjRUHVec55HWXUoJtNxrjZRrmRDZ2nT&hc_ref=ARQPzzdmL3_nXvYFYyEwBmgfc9Nx_FW5sy3GoCDY4CPAwfyALasuchl2ASkPgxKsDfc&fref=nf"  # input("paste you or your friends's fb link here:")
options = webdriver.ChromeOptions()
prefs = {'profile.default_content_setting_values':{'notifications': 2}}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver",options=options)
 
driver.get("https://www.facebook.com")
account = driver.find_element_by_name("email")
account.send_keys(USERNAME)
password = driver.find_element_by_name("pass")
password.send_keys(PASSWORD)
try: # old version
    button = driver.find_element_by_id("loginbutton")
    button.click()
except: # new version
    button = driver.find_element_by_name("login")
    button.click()
   
   
   
   
 
driver.get(link)
for i in range(5):
    driver.execute_script(f"window.scrollTo(0, {5000 * (i + 1)})")
    time.sleep(3)
html = driver.page_source
 
all_post=list()
soup = BeautifulSoup(html, 'html.parser')
divs = soup.find_all('div', class_="text_exposed_root")
 
for div in divs:
    p = div.find_all('p')
    itemm=""
    for item in p:
        item=item.get_text()
        itemm+=item
    all_post.append(itemm)


# 將讀進的文章做出整理
import re
import emoji

with open("fb_text.txt", "w", encoding="utf-8") as fh1:
    for article in all_post:
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
                    fh1.write(line.strip())
                else:
                    fh1.write(line.strip() + "，")  # 有一些直接換行，現在分開後會沒有標點符號，幫他補上
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
                fh1.write(last_line.strip())
            else:
                fh1.write(last_line.strip() + "。")  # 補句號
        else:
            continue

        fh1.write("\n")  # 一編文章結束後記得換行
        # fh1.write("================")
    fh1.close()

import sys
from snownlp import SnowNLP

# def read_and_analysis(input_file, output_file):
#     f = open(input_file, "r", encoding="utf-8")
#     fw = open(output_file, "w", encoding="utf-8")
#     while True:
#         line = f.readline()
#         print(line)
#         if not line:
#             break
#         line = line.strip()

#         s = SnowNLP(line)
#         for sentence in s.sentences:
#             i = SnowNLP(sentence)
#             print(i)
#         # s.words 查询分词结果
#             seg_words = ""
#             for x in i.words:
#                 seg_words += "_"
#                 seg_words += x
#                 print(seg_words)
#         # s.sentiments 查询最终的情感分析的得分
#             fw.write(line + "\t" + seg_words + "\t" + str(i.sentiments) + "\n")
#     fw.close()
#     f.close()

# read_and_analysis("fb_text.txt", "fb_text_sentiment_analysis.txt")


def read_and_analysis(input_file, output_file):
    avg_index = 0
    number = 0
    f = open(input_file, "r", encoding="utf-8")
    fw = open(output_file, "w", encoding="utf-8")
    while True:
        line = f.readline()
        print(line)
        if not line:
            break
        line = line.strip()
        print(line)
        s = SnowNLP(line)

        # s.words 查询分词结果
        seg_words = ""
        for x in .words:
            seg_words += "_"
            seg_words += x
            print(seg_words)
        # s.sentiments 查询最终的情感分析的得分
        fw.write(line + "\t" + seg_words + "\t" + str(i.sentiments) + "\n")
    fw.close()
    f.close()

read_and_analysis("fb_text.txt", "fb_text_sentiment_analysis.txt")


