import bs4
import lxml
import re
import requests


class Scraper:
    """
    Gets author and their quotes in a dictionary from a a page
    Also finds out if the page has a next one
    If it does have a next page it gets the href
    """

    def __init__(self, url):
        self._url = url
        self._hasnext = True
        self._next = ""

    def scrape(self):
        
        r = requests.get(self._url)
        if r.status_code != requests.codes.ok:
            return None

        page_text = r.text # .encode('ascii', 'ignore')
        soup = bs4.BeautifulSoup(page_text, 'lxml')
        try:
            self._next = soup.find_all("li", {"class": "next"})[0].find_all("a")[0].attrs['href']
        except:
            self._hasnext = False
            
        page_data = {}

        for items in soup.find_all("div",  {"class": "quote"}):
            quote = items.find_all("span",  {"class": "text"})[0].get_text()
            author = items.find_all("small",  {"class": "author"})[0].get_text()

            if author in page_data:
                page_data[author].append(quote)
            else:
                page_data[author] = [quote]

        return  page_data

    def hasnext(self):
        return self._hasnext

    def nexturl(self):
        return self._next

class Crawler:
    """
    Calls Scraper for every page
    Uses Scraper methods to get the next page
    """

    def __init__(self):
        self._data = {}
        self.base_url = "http://quotes.toscrape.com"

    def crawl(self):
        curr_url = ""
        current_page = Scraper(self.base_url)
        self._data.update(current_page.scrape())

        while(current_page.hasnext()):
            curr_url = current_page.nexturl()
            current_page = Scraper(self.base_url + curr_url)
            self._data.update(current_page.scrape())
        return self._data


print(Crawler().crawl())
