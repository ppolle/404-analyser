import os
import requests
import logging
from bs4 import BeautifulSoup

class Crawl:
    def __init__(self, base_url):
        self.base_url = base_url
        self.links = [self.base_url]
        self.broken_links = []
        self.visited_links = []

        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

        # Create target Directory if don't exist
        if not os.path.exists('Broken Links'):
            os.mkdir('Broken Links')

    def crawl(self):
        
        for link in self.links:
            if link not in self.visited_links:
                self.analysis(link)

    def get_links(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        links = soup.find_all('a')

        for link in links:
            if link.has_attr('href'):
                link = self.sanitize_links(link.get('href'))
                if link not in self.links and link.startswith(self.base_url) is True:
                    self.links.append(link)
                
    def sanitize_links(self, link):

        if link.startswith('/'):
            link = self.base_url + link[1:]

        if self.base_url not in link:
            link = self.base_url + link

        return link

    def update_visited_links(self, link):
        if link not in self.visited_links:
            self.visited_links.append(link)

    def update_broken_links(self, link):
        if link not in self.broken_links:
            self.broken_links.append(link)

    def analysis(self, link):
        logging.info('Analysing link:' + link)
        response = requests.get(link)
        if response.status_code == 200:
            self.update_visited_links(link)
            self.get_links(response.content)
        else:
            self.update_visited_links(link)
            self.update_broken_links(link)      

    def complete(self):
        import csv

        print('')
        logging.info('Operation completed. {} urls analysed.{} broken links found as outlined in the csv file'.format(len(self.visited_links), len(self.broken_links)))
        
        with open('broken_lins_csv/{}.csv'.format(self.base_url), "w") as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["Broken Links"])
            for link in self.broken_links:
                writer.writerow([link])

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Finds broken links on a website.")
    parser.add_argument('base_url', type=str,
                        help='The base url where the crawler should start')

    arguments = parser.parse_args()
    address = arguments.base_url 

    run = Crawl(address)
    run.crawl()
    run.complete()  
