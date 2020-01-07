# 將各種不同的溶液成分的單位全都轉成ml，再依此求出酒精濃度與總容量
import csv
import re

csvfile = open("pre_processing.csv", "r")
abvss = open("liquor_table.csv", "r")
abvs = abvss.readlines()
abv_involved = open("abv_involved.csv", "w")
writer = csv.writer(abv_involved)

acdict = {"dash":0.92,
		  "teaspoon":4.93,
		  "splash":5.91,
		  "bottle":750,
		  "cup":36.58,
		  "bar spoon":2.5,
		  "shot":44.36,
		  "tablespoon":14.79,
		  "can":227.30,
		  "drizzle":0.92}

writer.writerow(["cocktail_name", "alcohol_concentration(%)", "total_volume(ml)"])

warehouse = csv.DictReader(csvfile)  # 把調酒資料庫存成warehouse
for cocktail in warehouse:  # 打開調酒資料庫
	total_alcohol = 0  # 預設酒精含量為 0
	total_volume = 1  # 總容量為 1，避免等等總容量為 0 無法相除
	cocktail_name = cocktail["cocktails_name"]  # 調酒名稱
	# print(cocktail_name)
	for i in range(1, 13):
		volume = 0
		clnm = "ingredient_" + str(i) # 從第一個成分開始看到第十二個
		# print(cocktail[clnm])
		if (cocktail[clnm] == None) or (":" not in cocktail[clnm]):  # 若裡面是空白(None) 或是沒有冒號(代表沒有被我分類過)
			continue  # 就跳過不理
		else:  # 不然的話 
			cocktail_inf = cocktail[clnm].split(":")  # 用冒號分離出成分名稱與對應的容量
			# print(cocktail_inf)
			for key in acdict:
				unit = "(" + key + ")"
				# print(unit)
				if unit in cocktail_inf[1]:
					convert_to_ml = cocktail_inf[1].strip(unit)
					try:
						volume = float(convert_to_ml) * acdict[key]  # 單位轉成ml
						total_volume += volume
						# print(cocktail_inf[0], cocktail_inf[1], volume)
					except ValueError:
						pass
					break

			else:  # ml
				volume = float(cocktail_inf[1])
				total_volume += volume
				# print(cocktail_inf[0], cocktail_inf[1], volume)

			for abv in abvs:  # 打開酒精含量表，確認成分是否含酒精
				abv = abv.split(",")  # 因為是用readlines讀取，因此用冒號先分出相對應的酒種與其酒精濃度
				if abv[0] == cocktail_inf[0]:  # 如果酒精含量表的酒種名等於成分酒種名
					alcohol = volume * float(abv[1])
					total_alcohol += alcohol
					break
					# print(abv[0], alcohol)
			else:  # 不含酒精
				pass
	# total_volume -= 1
	alcohol_concentration = round(total_alcohol / total_volume, 1)

	print("name:", cocktail_name, ",", alcohol_concentration, "total_volume:", round(total_volume - 1))
	writer.writerow([cocktail_name, alcohol_concentration, round(total_volume - 1)])
	# print("total_volume is :", total_volume)
	# print("alcohol is :", alcohol)
csvfile.close()
abvss.close()
abv_involved.close()
# ===========================================================================================