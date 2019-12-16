import requests

url = "https://search.books.com.tw/"
url += "search/query/cat/all/key/python/sort/1/page/2/v/0/"
print(url)

r = requests.get(url)

print(r.status_code)

if r.status_code == requests.codes.ok:
	print("OK!")

# print(r.text)


from bs4 import BeautifulSoup
soup = BeautifulSoup(r.text, "html.parser")
# print(soup.prettify())

title_tag = soup.title
# print(title_tag)
# print(title_tag.string)

attr = {"class": "price"}
price_tags = soup.find_all("span", attrs=attr)
prices = []

for tag in price_tags:
	t = tag.get_text().strip()
	index_comma = t.find(",")
	index_dollar = t.find("元")

	if index_comma >= 0:
		price_str = t[index_comma + 2 : index_dollar - 1]
	else:
		index_colon = t.find(":")
		price_str = t[index_colon + 2 : index_dollar - 1]

	prices.append(int(price_str))
prices = prices[0:20]
# avg_price = sum(prices) / len(prices)
# print(avg_price)

attr = {"rel": "mid_name"}
title_tags = soup.find_all("a", attrs=attr)

titles = []
links = []

for tag in title_tags:
	title_str = tag.get_text().strip()
	link_str = "http:" + tag["href"]
	titles.append(title_str)
	links.append(link_str)

# print(titles)
# print(links)

fn2 = "books.csv"
fh2 = open(fn2, "w", encoding="utf-8")
print(len(titles))
print(len(prices))
print(len(links))

for i in range(len(prices)):
	fh2.write(titles[i] + "," + str(prices[i]) + "," + links[i] + "\n")
fh2.close()
	















