import requests
from bs4 import BeautifulSoup

url = 'https://www.vg.no/'




result = requests.get(url)
doc = BeautifulSoup(result.text) 



tag = doc.h2 
  
headlines = doc.find_all('h2', class_='headline')
links = doc.find_all('a', itemprop='url')

links_list = []

for link in links:
    href = link.get('href')  # Use .get() to avoid KeyError
    if href and 'https://www.vg.no/nyheter' in href:  # Ensure href is not None

        headline = href[35:].split('?')

        print(headline)

        links_list.append(headline[0].replace("-", " "))
          # Print only matching links

for i in links_list:
    print(i)


"""for headline in headlines:
    print('\n')
    print(f'headline {count}', headline)

    count +=1

    if count ==2:
        break"""
