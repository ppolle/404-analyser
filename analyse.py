import requests
from bs4 import BeautifulSoup

class Crawl:
    def crawl(self):
        self.base_url = 'http://devhubafrika.org/'
        self.links = [self.base_url]
        self.broken_links = []
        self.visited_links = []

        for link in self.links:
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
        print('Analysing link:' + link)
        response = requests.get(link)
        if response.status_code == 200:
            self.update_visited_links(link)
            self.get_links(response.content)
        else:
            self.update_visited_links(link)
            self.update_broken_links(link)      

    def complete(self):
        print('Operation completed. {} urls analysed.{} broken links found as outlined below:'.format(len(self.visited_links), len(self.broken_links)))
        for link in self.broken_links:
            print(link)

run = Crawl()
run.crawl()
run.complete()  
