import requests

import re

# 複製網址，分兩次只是為了比較好看而已
url = "https://www.socialandcocktail.co.uk/cocktail-recipes/"
url += "?sort_by=title&sort_name=Name&custom_sort=0&sort=ASC"  
r = requests.get(url)  # 用 requests.get() 取得網址資料

if r.status_code == requests.codes.ok:
	print("OK!")  # 確認網址運作正常（給爬）
# print(r.text)


from bs4 import BeautifulSoup
soup = BeautifulSoup(r.text, "html.parser")  # 準備用bs4爬蟲
# print(soup.prettify())

title_tag = soup.title  # 沒啥用，看一下title而已，可忽略～
# print(title_tag)
# print(title_tag.string)


# 收集調酒的名字 ex:「long island iced tea」
# 每頁應該要有 30 種調酒，共有 36 頁，不過最後一頁只有 22 種調酒
# 所以共計有 30 * 35 + 22 * 1 = 1072 種調酒～
names_tags = soup.find_all("h3")  # 剛剛好調酒名都藏在 <h3> 的 tag 下～
names = []

for name in names_tags:
	n = name.get_text().strip()
	# print(n)
	# print("=======")
	names.append(n)  # 創造一個裝有調酒名稱的 list

names = names[:-1]  # 因為 tag 的原因，每頁最後一個被抓到的名稱都會是
# print(names)		# "You Bring The Party. We Bring The Cocktails.Glasgow | Edinburgh | Aberdeen | Dundee"
					# 但不是我們要的，所以把他去掉～


# 接下來要抓每種調酒用的食材
# 這個比較容易，食材都藏在 <p style="font-size:0.7em;padding-bottom:10px"> 這個 tag 下
attr = {"style": "font-size:0.7em;padding-bottom:10px"}
ingredient_tags = soup.find_all("p", attrs=attr)
ingredient_lists = []

for ingredient_list in ingredient_tags:
	i = ingredient_list.get_text(",").strip().split(",")  # 注意這裡是用get_text(",")
	# print(i)											  # 而不是get_text()，不懂者可問谷歌大神
	# print("==========")
	ingredient_lists.append(i) # 將每種調酒的食材列成一個 list
# print(ingredient_lists)


def split_ingredient_by_plural(unit, base):
	base = base.split(unit)
	amount_str = base[0].strip().split(" ")

	amount = 0
	if len(amount_str) == 1:
		try:
			amount = float(amount_str[0])
		except ValueError:
			if "/" in amount_str[0]:
				num = int(amount_str[0].split("/")[0])
				den = int(amount_str[0].split("/")[0])
				amount = float(num / den)
			else:
				amount = "several"
	elif len(amount_str) == 2:
		amount = float(amount_str[0]) + 0.5
	
	if "of " in base[1].strip():
		liquid_name = base[1].strip()
		liquid_name = liquid_name[3: ]
	else:
		liquid_name = base[1].strip()
	
	liquid_name_and_amount = [liquid_name, str(amount)]

	return liquid_name_and_amount


def split_ingredient_by_single(unit,base):
	
	base = base.split(unit)
	amount = 1.0

	if "of " in base[1].strip():
		liquid_name = base[1].strip()
		liquid_name = liquid_name[3: ]
	else:
		liquid_name = base[1].strip()
	
	liquid_name_and_amount = [liquid_name, str(amount) + "(" + unit + ")"]

	return liquid_name_and_amount	


# 準備結構化資料
adjusted_ingredient_lists = []
for ingredient_list in ingredient_lists:  # 調酒

	base_list = []
	for base in ingredient_list:  # i 調酒的原料列表
		
		# match = re.match("([0-9]+) ([^0-9]+)", base, re.I)
		# print(match)

		if "ml" in base:  # 用 ml split，沒有 ml 的無法分割
			base = base.split("ml")
			amount_str = base[0].strip().split(" ")  # 因為容量都放在 ml 前面，所以取第一項，
													 # 並用空白分割  
			
			if len(amount_str) == 1:  # 如果沒有被空白分割（沒有 1/2）
				amount = float(amount_str[0])
			elif len(amount_str) == 2:  # 如果有，加 0.5ml（這裡是用觀察法）
				amount = float(amount_str[0]) + 0.5
			
			liquid_name = base[1].strip()  # 取得原料名稱
			liquid_name_and_amount = [liquid_name, amount] # 原料名稱、其容量

		elif "dashes" in base:
			unit = "dashes"
			liquid_name_and_amount = split_ingredient_by_plural(unit, base)
			liquid_name_and_amount[1] += "(dash)"

		elif "dash" in base:
			unit = "dash"
			liquid_name_and_amount = split_ingredient_by_single(unit, base)
		
		elif "teaspoons" in base:
			unit = "teaspoons"
			liquid_name_and_amount = split_ingredient_by_plural(unit, base)
			liquid_name_and_amount[1] += "(teaspoon)"

		elif "teaspoon" in base:
			unit = "teaspoon"
			liquid_name_and_amount = split_ingredient_by_single(unit, base)
		
		elif "cups" in base:
			unit = "cups"
			liquid_name_and_amount = split_ingredient_by_plural(unit, base)
			liquid_name_and_amount[1] += "(cup)"

		elif "cup" in base:
			unit = "cup"
			liquid_name_and_amount = split_ingredient_by_plural(unit, base)
			liquid_name_and_amount[1] += "(cup)"				

		elif "bottles" in base:
			unit = "bottles"
			liquid_name_and_amount = split_ingredient_by_plural(unit, base)
			liquid_name_and_amount[1] += "(bottle)"

		elif "bottle" in base:
			unit = "bottle"
			liquid_name_and_amount = split_ingredient_by_plural(unit, base)
			liquid_name_and_amount[1] += "(bottle)"

		# elif match != None:
  #  			items = match.groups()
  #  			liquid_name = items[1].strip()
  #  			amount_str = items[0].strip()
  #  			liquid_name_and_amount = [liquid_name, amount_str]

		else:
			liquid_name_and_amount = base  # 沒有 ml 則先給過，之後再處理

		base_list.append(liquid_name_and_amount)

	adjusted_ingredient_lists.append(base_list)  # 將整理好的原料列表計入新列表
# print(adjusted_ingredient_lists)
# print(len(names))


# 輸出成csv檔案（這只是第一頁喔！）
with open("cocktails.csv", "w", encoding="utf-8") as fh1:

	fh1.write("cocktails_name,ingredient_1,ingredient_2,ingredient_3,ingredient_4,ingredient_5,ingredient_6,ingredient_7,ingredient_8,ingredient_9,ingredient_10,ingredient_11,ingredient_12\n")

	for i in range(len(names)):

		ingredient_str = ""
		# print(adjusted_ingredient_lists[i])
		for j in adjusted_ingredient_lists[i]:
			if isinstance(j, list):
				ingredient_str += "," + j[0] + ":" + str(j[1])
			else:
				ingredient_str += "," + j
		print(ingredient_str)
		fh1.write(names[i] + ingredient_str + "\n")
	fh1.close()



# 還有後面的另外35頁，用 for 迴圈包住，然後做跟第一頁一樣的事～最後append在原檔上
for page in range(2, 37):
	url = "https://www.socialandcocktail.co.uk/cocktail-recipes/page/"
	url += str(page)
	url += "/?sort_by=title&sort_name=Name&custom_sort=0&sort=ASC"
	# print(url)
	
	r = requests.get(url)
	
	soup = BeautifulSoup(r.text, "html.parser")
	
	names_tags = soup.find_all("h3")
	names = []

	for name in names_tags:
		n = name.get_text().strip()
		names.append(n)
	names = names[:-1]

	attr = {"style": "font-size:0.7em;padding-bottom:10px"}
	ingredient_tags = soup.find_all("p", attrs=attr)
	ingredient_lists = []

	for ingredient_list in ingredient_tags:
		i = ingredient_list.get_text(",").strip().split(",")
		ingredient_lists.append(i)

	adjusted_ingredient_lists = []
	for ingredient_list in ingredient_lists:

		base_list = []
		for base in ingredient_list:
			
			# match = re.match("([0-9]+) ([^0-9]+)", base, re.I)
			# print(match)
			
			if "ml" in base:
				base = base.split("ml")
				amount_str = base[0].strip().split(" ")
			
				if len(amount_str) == 1:
					amount = float(amount_str[0])
				elif len(amount_str) == 2:
					amount = float(amount_str[0]) + 0.5
			
				liquid_name = base[1].strip()

				liquid_name_and_amount = [liquid_name, amount]
			
			elif "dashes" in base:
				unit = "dashes"
				liquid_name_and_amount = split_ingredient_by_plural(unit, base)
				liquid_name_and_amount[1] += "(dash)"

			elif "dash" in base:
				unit = "dash"
				liquid_name_and_amount = split_ingredient_by_single(unit, base)
			
			elif "teaspoons" in base:
				unit = "teaspoons"
				liquid_name_and_amount = split_ingredient_by_plural(unit, base)
				liquid_name_and_amount[1] += "(teaspoon)"

			elif "teaspoon" in base:
				unit = "teaspoon"
				liquid_name_and_amount = split_ingredient_by_single(unit, base)
		
			elif "cups" in base:
				unit = "cups"
				liquid_name_and_amount = split_ingredient_by_plural(unit, base)
				liquid_name_and_amount[1] += "(cup)"

			elif "cup" in base:
				unit = "cup"
				liquid_name_and_amount = split_ingredient_by_plural(unit, base)
				liquid_name_and_amount[1] += "(cup)"				

			elif "bottles" in base:
				unit = "bottles"
				liquid_name_and_amount = split_ingredient_by_plural(unit, base)
				liquid_name_and_amount[1] += "(bottle)"

			elif "bottle" in base:
				unit = "bottle"
				liquid_name_and_amount = split_ingredient_by_plural(unit, base)
				liquid_name_and_amount[1] += "(bottle)"

			# elif match != None:
   # 				items = match.groups()
   # 				liquid_name = items[1].strip()
   # 				amount_str = items[0].strip()
   # 				liquid_name_and_amount = [liquid_name, amount_str]
			
			else:
				liquid_name_and_amount = base

			base_list.append(liquid_name_and_amount)

		adjusted_ingredient_lists.append(base_list)

	with open("cocktails.csv", "a", encoding="utf-8") as fh1:
		for i in range(len(names)):

			ingredient_str = ""
			print(adjusted_ingredient_lists[i])
			for j in adjusted_ingredient_lists[i]:
				if isinstance(j, list):
					ingredient_str += "," + j[0] + ":" + str(j[1])
				else:
					ingredient_str += "," + j
			print(ingredient_str)
			fh1.write(names[i] + ingredient_str + "\n")
		fh1.close()

