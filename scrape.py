"""
Module to scrape top-urls from various websites
"""

import requests
import bs4
import logging
import re

module_logger = logging.getLogger('scrape')

def _scrape_reddit(subreddit, min_votes):
    resp = requests.get('http://reddit.com/r/{0}'.format(subreddit))
    if resp.status_code != 200:
        module_logger.error("Unable to reach reddit subreddit {0}".format(
            subreddit))
        return []

    urls = []
    soup = bs4.BeautifulSoup(resp.text)
    for div_tag in soup.findAll('div', attrs={'class':'score unvoted'}):
        try:
            score = int(div_tag.text)
            if score < min_votes:
                continue
        except:
            continue
        link = div_tag.parent.parent.findAll('a', attrs={'class':'title'})[0]
        urls.append((link['href'], link.text))
    return urls

def scrape_reddit_programming(min_votes):
    return _scrape_reddit('programming', min_votes)

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

