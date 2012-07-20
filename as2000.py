import readers
import scrape
import logging
import getpass
import daemonize

def get_a_number(prompt):
    while 1:
        maybe_num = raw_input(prompt)
        try:
            num = int(maybe_num)
            return num
        except:
            print "Sorry, I didn't understand."

def main():
    print "Let's configure Article Saver 2000!"
    hn = raw_input("Would you like to include Hacker News [y/n]? ")
    if hn.strip().lower() == 'y':
        print "Ok, I'll check Hacker News. ",
        upvotes = get_a_number("Enter the minimum number of upvotes: ")

    reddit = raw_input("Would you like to include Reddit [y/n]? ")
    if reddit.strip().lower() == 'y':
        print "Ok, I'll check reddit.", 
        upvotes = get_a_number("Enter the minimum number of upvotes: ")

    pocket_user = raw_input("What is your Pocket username? ")
    pocket_pw = getpass.getpass("What is your Pocket password? ")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
