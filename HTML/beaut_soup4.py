import requests
from bs4 import BeautifulSoup


url = "https://en.wikipedia.org/wiki/Main_Page"
r = requests.get(url)
soup = BeautifulSoup(r.content)
# print(soup.prettify)
# print(soup.find_all("a"))

links = soup.find_all("a")
# for link in links:
	# print (link.get("href"))
	# print(link.text)
	# print("<a href='%s'> %s </a>" %(link.get("href"),link.text
	# try:
	# 	print("hello")
	# except:
	# 	pass


g_data = soup.find_all("div",{"class":"info"})
for item in g_data:
	print(item.contents[0].find_all("a",{"calss":"business"})[0].text.replace(",", " ")  #tag and dict