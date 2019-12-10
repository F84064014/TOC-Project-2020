from bs4 import BeautifulSoup
import requests
import random

resp = requests.get('https://tw.yahoo.com/')
soup = BeautifulSoup(resp.text, 'html.parser')
stories = soup.find_all('a', class_='story-title')
#for s in stories:
#    print("title: " + s.text)

#print(soup.prettify())
#print(stories)
for s in stories:
    print(s.text)
a = list()
for s in stories:
    a.append(s.text)
print(a[random.randint(0,10)])

#https://must-be-lower-case.herokuapp.com/webhook



https://tw.news.search.yahoo.com/search;_ylt=AwrtXWm9l.9d8hUALRFw1gt.;_ylu=X3oDMTEwOG1tc2p0BGNvbG8DBHBvcwMxBHZ0aWQDBHNlYwNwYWdpbmF0aW9u?p=%E9%9F%93%E5%9C%8B%E7%91%9C&pz=10&b=1&pz=10&xargs=0
https://tw.news.search.yahoo.com/search;_ylt=AwrtXWlkle9dcTsA3wNw1gt.;_ylu=X3oDMTEwOG1tc2p0BGNvbG8DBHBvcwMxBHZ0aWQDBHNlYwNwYWdpbmF0aW9u?p=%E9%9F%93%E5%9C%8B%E7%91%9C&b=11&pz=10&xargs=0
https://tw.news.search.yahoo.com/search;_ylt=AwrtXWrMl.9dkgwAdRRw1gt.;_ylu=X3oDMTEwOG1tc2p0BGNvbG8DBHBvcwMxBHZ0aWQDBHNlYwNwYWdpbmF0aW9u?p=%E9%9F%93%E5%9C%8B%E7%91%9C&pz=10&b=21&pz=10&xargs=0
https://tw.news.search.yahoo.com/search;_ylt=AwrtXW4cmO9dR3QAyyBw1gt.;_ylu=X3oDMTEwOG1tc2p0BGNvbG8DBHBvcwMxBHZ0aWQDBHNlYwNwYWdpbmF0aW9u?p=%E9%9F%93%E5%9C%8B%E7%91%9C&pz=10&b=31&pz=10&xargs=0