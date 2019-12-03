from bs4 import BeautifulSoup
import requests

resp = requests.get('')
soup = BeautifulSoup(resp.text, 'html.parser')
#stories = soup.find_all('a', class_='story-title')
#for s in stories:
#    print("title: " + s.text)

print(soup.prettify())

