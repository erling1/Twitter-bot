import requests
from bs4 import BeautifulSoup




class ScrapAndFilter:

    def __init__(self, url : str = 'https://www.vg.no/'):
        self.url = url

        self.headlines = self.scrape(url)
        self.norwegian_news_words = frozenset([
    # Crime and Law Enforcement
    "politiet",
    "drapet",
    "dømt",
    "drap",
    "siktede",
    "mistenkte",
    "fengslet",
    "doemt",
    "knivstikking",
    "arrestert",
    
    # Politics and Government
    "justisministeren",
    "regjeringen",
    "politiker",
    "opposisjons",
    "stortinget",
    
    # Political Figures
    "erna solberg",
    "støre",
    "vedum",
    "trump",
    
    # Action Words
    "sier",
    "mener",
    "advarer",
    "avsløres",
    "hevder",
    "raser",
    "anker",
    "henlegger",
    
    # Incident Related
    "ulykken",
    "skytingen",
    "døde",
    "drepte",
    "skadede",
    "hendelsen",
    
    # Location Identifiers
    "norske",
    "norge",
    "svensk",
    "israel",
    "gaza",
    
    # Organizations
    "nrk",
    "vg",
    "aftenposten",
    "politiet",
    "usaid",
    
    # Status Words
    "saken",
    "dommen",
    "ordre",
    "rapport"
])
    
    def scrape(self,url):


        result = requests.get(url)
        doc = BeautifulSoup(result.text) 

        links = doc.find_all('a', itemprop='url')

        links_list = []

        for link in links:
            href = link.get('href') 
            if href and 'https://www.vg.no/nyheter' in href:  

                headline = href[35:].split('?')

                

                links_list.append(headline[0].replace("-", " "))
                # Print only matching links

        
        return links_list

    def filter_news(self ):

        filter_words = self.norwegian_news_words

        news_headlines = []
        

        for headline in self.headlines:

            

        

            title_words = set(headline.lower().split())
            if bool(title_words & filter_words):  # True if any word from title is in filter_words

                news_headlines.append(headline)
        

        
        return news_headlines
    

    
    