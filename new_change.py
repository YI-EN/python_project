# url = "https://www.socialandcocktail.co.uk/cocktails/"
# url += "tequila-sunrise-margarita" + "/"

wine = ["'asdf'  'asd fasfd'  'asdfgaf'"]
url_list = []
for i in wine:
	urll_list = []
	i = i.split("  ")
	# print(i)
	for j in i:
		j = j.strip("'")
		# print(j)
		url = "https://www.socialandcocktail.co.uk/cocktails/"
		j = j.split(" ")
		if len(j) > 1:
			y = "-".join(j)
			url += y + "/"
			urll_list.append(url)
			# print(url)
		else:
			url += j[0] + "/"
			urll_list.append(url)
			# print(url)
	url_list.append(urll_list)
print(url_list)