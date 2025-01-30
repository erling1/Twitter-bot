import requests
from bs4 import BeautifulSoup

url = 'https://www.vg.no/'




result = requests.get(url)
doc = BeautifulSoup(result.text) 



tag = doc.h2 
  
headlines = doc.find_all('h2', class_='headline')
links = doc.find_all('a', itemprop='url')

for link in doc.find_all('a'):
    print(link.get('href'))

data = {}
count = 1


"""for headline in headlines:
    print('\n')
    print(f'headline {count}', headline)

    count +=1

    if count ==2:
        break"""
