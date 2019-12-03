from bs4 import BeautifulSoup
import requests

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
print(a)

