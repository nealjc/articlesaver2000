"""
Module to scrape top-urls from various websites
"""

import requests
import bs4
import logging
import re

module_logger = logging.getLogger('scrape')

def scrape_reddit(subreddit, min_votes):
    pass

def scrape_hackernews(min_votes):
    resp = requests.get('http://news.ycombinator.com')
    if resp.status_code != 200:
        module_logger.error("Unable to reach NH")
        return []

    urls = []
    soup = bs4.BeautifulSoup(resp.text)
    for span_tag in soup.findAll(id=re.compile("^score_*")):
        score = int(span_tag.text.split()[0])
        if score < min_votes:
            continue
        title_row_tr = span_tag.parent.parent.previousSibling
        title_td = title_row_tr.findAll('td', attrs={'class':'title'})[1]
        url, title = title_td.a['href'], title_td.a.text
        urls.append((url, title))
    return urls

if __name__ == '__main__':
    logging.basicConfig()
    print scrape_hackernews(100)
    
