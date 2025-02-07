from scrape import ScrapAndFilter
import requests
from bs4 import BeautifulSoup
import json
import itertools

norwegian_news_sites = [
    "https://www.nrk.no",
    "https://www.tv2.no",
    "https://www.dagbladet.no",
    "https://www.aftenposten.no"
]

def get_clean_nrk_headlines(url):
    # Get webpage content
    result = requests.get(url)
    doc = BeautifulSoup(result.text, 'html.parser')
    links = doc.find_all('a')
    
    cleaned_headlines = set()
    
    for link in links:
        href = link.get('href', '')
        
        
        if not href or 'www.nrk.no' not in href:
            continue
            
        
        headline = href.split('/')[-1]
        
        
        if not headline or headline in ['nyheter', 'logginn', 'nrk-forklarer', 'langlesing']:
            continue
            
        
        if '-' in headline and any(char.isdigit() for char in headline):
            # Split by the article ID
            parts = headline.split('-1.')
            if len(parts) > 1:
                # Clean up the headline
                clean_headline = parts[0]
                clean_headline = clean_headline.replace('-', ' ')
                clean_headline = clean_headline.strip('_ ')
                
                if clean_headline:  # Only add non-empty headlines
                    cleaned_headlines.add(clean_headline)
    
    return list(cleaned_headlines)



def get_clean_tv2_headlines(url):
    # Get webpage content
    result = requests.get(url)
    doc = BeautifulSoup(result.text, 'html.parser')
    links = doc.find_all('a')
    
    # Store unique headlines
    cleaned_headlines = set()
    
    for link in links:
        href = link.get('href', '')
        
        # Skip if empty or if it's not a news article
        if not href or not any(char.isdigit() for char in href):
            continue
            
        # Split by '/' and get relevant parts
        parts = href.split('/')
        
        # The TV2 format we want has a number at the end like '/17434344/'
        if len(parts) >= 2:
            # Look for the part that ends with numeric ID
            for i, part in enumerate(parts):
                if part.isdigit() and i > 0:  # If we find a numeric part
                    headline = parts[i-1]  # Take the part before the number
                    
                    # Clean up the headline
                    headline = headline.replace('-', ' ')
                    headline = headline.strip('_ ')
                    
                    # Only add if it's not a system page and is long enough
                    if (headline and 
                        len(headline) > 3 and  # Avoid very short strings
                        not headline.startswith(('video', 'asset', 'sport', 'kategori', 'alle')) and
                        not headline.endswith(('jpg', 'png', 'mp4'))):
                        
                        cleaned_headlines.add(headline)
                    break  # Stop looking after finding first numeric part
    
    return list(cleaned_headlines)


def get_clean_dagbladet_headlines(url):
    # Get webpage content
    result = requests.get(url)
    doc = BeautifulSoup(result.text, 'html.parser')
    links = doc.find_all('a')
    
    # Store unique headlines
    cleaned_headlines = set()
    
    for link in links:
        href = link.get('href', '')
        
        # Skip if empty or if it's not a news article 
        if not href or 'dagbladet.no' not in href:
            continue
            
        # Split by '/' to get parts
        parts = href.split('/')
        
        # Look for parts that start with '8' (Dagbladet article IDs)
        for i, part in enumerate(parts):
            if part.isdigit() and part.startswith('8') and len(part) == 8:
                # Get the headline part (comes before the ID)
                if i > 0:
                    headline = parts[i-1]
                    
                    # Clean up the headline
                    headline = headline.replace('-', ' ')
                    headline = headline.strip('_ ')
                    
                    # Filter out non-article pages
                    if (headline and 
                        len(headline) > 3 and
                        not headline.startswith(('video', 'asset', 'kategori', 'alle', 'info')) and
                        not headline.endswith(('jpg', 'png', 'mp4'))):
                        
                        cleaned_headlines.add(headline)
                break
    
    return list(cleaned_headlines)


def get_clean_aftenposten_headlines(url):
    result = requests.get(url)
    doc = BeautifulSoup(result.text, 'html.parser')
    links = doc.find_all('a')
    
    cleaned_headlines = set()
    
    # Keywords that suggest political content
    political_keywords = {
        'trump', 'politikk', 'stortinget', 'regjering', 'parti', 'minister', 
        'høyre', 'frp', 'ap', 'arbeiderpartiet', 'sp', 'sv', 'valg', 
        'demokrat', 'republikaner', 'nato', 'eu', 'stoltenberg', 'støre',
        'folkevalgt', 'vedtak', 'storting', 'statsråd', 'israel', 'putin',
        'biden', 'militær', 'krig'
    }
    
    for link in links:
        href = link.get('href', '')
        
        # Only process Aftenposten articles
        if not href or 'aftenposten.no' not in href:
            continue
            
        # Skip certain sections we don't want
        if any(x in href for x in ['/video/', '/stories/', '/fordel/', '/spill/', '/tag/', '/kultur/']):
            continue
            
        # Split URL into parts
        parts = href.split('/')
        if len(parts) < 5:  # Need at least domain/section/i/id/headline
            continue
            
        # Find the part that contains the actual headline
        headline = None
        for i, part in enumerate(parts):
            if part == 'i' and i+2 < len(parts):
                headline = parts[i+2].split('?')[0]  # Remove URL parameters
                break
        
        if headline:
            # Clean up the headline
            headline = headline.replace('-', ' ')
            headline = headline.strip('_ ')
            
            # Check if it's political content
            if (any(keyword in headline.lower() for keyword in political_keywords) and
                len(headline) > 5):  # Avoid very short strings
                cleaned_headlines.add(headline)
    
    return list(cleaned_headlines)



news_scrapers = [
    get_clean_nrk_headlines,
    get_clean_tv2_headlines,
    get_clean_dagbladet_headlines,
    get_clean_aftenposten_headlines
]

json_file = 'headlines.json'
with open(json_file, 'w', encoding='utf-8') as f:    # Need file object 'f', utf 8 to handle norwegian
    full_list = []
    for scraper, url in zip(news_scrapers, norwegian_news_sites):
        headlines = scraper(url)
        full_list.append(headlines)

    vg_headlines = ScrapAndFilter()
    full_list.append(vg_headlines.filter_news())

    json.dump(list(itertools.chain.from_iterable(full_list)), f)


    
