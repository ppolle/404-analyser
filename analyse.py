import logging
import requests
import tldextract
from bs4 import BeautifulSoup

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class Crawl:
    def __init__(self, base_url):
        self.base_url = base_url
        self.links = [self.base_url]
        self.broken_links = []
        self.visited_links = []

    def crawl(self):
        '''
        Starts the crawl process
        '''

        for link in self.links:
            if link not in self.visited_links:
                self.analysis(link)

    def get_links(self, content, link):
        '''
        Gets all links from a particular web page
        '''
        try:
            logger.info('Parsing:' + link + ', for more links')
            soup = BeautifulSoup(content, 'html.parser')
            links = soup.find_all('a')

            logger.info('... {} links found at {}'.format(len(links), link))

            for link in links:
                if link.has_attr('href'):
                    link = self.sanitize_links(link.get('href'))
                    if link not in self.links and self.check_tld(link):
                        self.links.append(link)
        except Exception as e:
            logger.error(e)

    def sanitize_links(self, link):
        '''
        Sanitizes the link
        '''
        if link == '/':
            link = self.base_url

        if link == '#':
            link = self.base_url

        # if link.startwith('')not self.check_tlf(link)

        # if link.startswith('/'):
        #     link = self.base_url + link[1:]

       

        # if base_tld not in link:
        #     link = self.base_url + link

        return link

    def check_tld(self, link):
        '''
        Checks if a links is of the same top level domain as the base url
        '''
        base_tld = tldextract.extract(self.base_url).registered_domain
        link_tld = tldextract.extract(link).registered_domain

        if link.startswith('https://') or link.startswith('http://'):
            if base_tld == link_tld:
                return True
            else:
                return False
        else:
            return False

    def update_visited_links(self, link):
        '''
        Update the visited links list
        '''
        if link not in self.visited_links:
            self.visited_links.append(link)

    def update_broken_links(self, link):
        '''
        Update the broken links list
        '''
        if link not in self.broken_links:
            self.broken_links.append(link)

    def analysis(self, link):
        '''
        Checks whether a link will return a status 200 and appropriately update the links visited and broken links lists
        '''
        try:
            logger.info('Analysing link:' + link)
            response = requests.get(link)
            if response.status_code == 200:
                self.update_visited_links(link)
                self.get_links(response.content, link)
            else:
                self.update_visited_links(link)
                self.update_broken_links(link)
        except Exception as e:
            logger.error(e)

    def complete(self):
        '''
        Saves all broken links into a csv file and saves the file in the 'Broken Links' folder
        '''
        import os
        import csv

        print('')
        logger.info('Operation completed. {} urls analysed.{} broken links found as outlined in the csv file'.format(
            len(self.visited_links), len(self.broken_links)))

        try:
            if len(self.broken_links) > 0:
                # Create target Directory to save broken links csv file's if don't exist
                if not os.path.exists('Broken Links'):
                    os.mkdir('Broken Links')

                #Create csv file    
                with open('Broken Links/{}.csv'.format(tldextract.extract(self.base_url).domain), "w") as csvfile:
                    writer = csv.writer(
                        csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    writer.writerow(["Broken Links"])
                    for link in self.broken_links:
                        writer.writerow([link])
        except Exception as e:
            logger.error(e)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description="Finds broken links on a website.")
    parser.add_argument('base_url', type=str,
                        help='The base url where the crawler should start')

    arguments = parser.parse_args()
    address = arguments.base_url

    run = Crawl(address)
    run.crawl()
    run.complete()
