# 404 Analyser
## By Peter Polle

## Description
404 Analyser is a CLI app that finds broken links on a website by crawling through it and and writting the resulting broken links into an aptly named CSV file.

## How It Works
404 Analyser works by crawling through a website finding all links on a page and testing if they are broken or not. It will in turn parse through all the links to find other links on the website and test those too. This process continues untill all links on the website have been tested. If a links doesnt have a status 200, it is registered as a broken link. Only links with the same top level domains as the base url will have their 404 status tested. 

### Usage
You can run the script directly from the terminal via Python 3.

Valid arguments are: 
- ```base_url``` required, URL at which the crawler should start

Example: 
``` 
python analyse.py https://example.com
```

### CSV Files
If any broken links will be found, a csv file will be saved in a 'Broken Links' directory. The file will take the top level domain name of the website that was just crawled.

Example:
For https://example.com the name of the csv file will be ```example.csv```

### Requirements 
- Python 3
- Beautiful Soup
- requests
- argparse
- csv
- tldextract
- logging

# License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details