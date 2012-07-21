"""
Work in progress. Will eventually use daemonize, store
preferences in a config file, etc.
"""

import readers
import scrape
import logging
import getpass
import daemonize
import time

module_logger = logging.getLogger('as2000')
#in seconds
SLEEP_TIME = 60*60

def get_a_number(prompt):
    while 1:
        maybe_num = raw_input(prompt)
        try:
            num = int(maybe_num)
            return num
        except:
            print "Sorry, I didn't understand."

def run_daemon(scrapers, pocket_user, pocket_pw):

    module_logger.info("Starting loop")
    while 1:
        for scraper in scrapers:
            urls = scraper[0](*scraper[1:])
            readers.send_to_pocket(urls, pocket_user, pocket_pw)
        module_logger.info("Sleeping for {0}".format(SLEEP_TIME))
        time.sleep(SLEEP_TIME)

def main():

    scrapers = []
    print "Let's configure Article Saver 2000!"
    for attr in dir(scrape):
        if not attr.startswith("scrape_"):
            continue
        scraper = getattr(scrape, attr)
        
        to_scrape = raw_input(
            "Would you like to include {0} [y/n]? ".format(attr))
        if to_scrape.strip().lower() == 'y':
            print "Ok, I'll check {0}. ".format(attr),
            upvotes = get_a_number("Enter the minimum number of upvotes: ")
            scrapers.append((scraper, upvotes))

    pocket_user = raw_input("What is your Pocket username? ")
    pocket_pw = getpass.getpass("What is your Pocket password? ")
    run_daemon(scrapers, pocket_user, pocket_pw)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
