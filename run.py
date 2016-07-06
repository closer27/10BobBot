import requests
from bs4 import BeautifulSoup

def crawl_page():
    url = 'http://supportportal.skplanet.com/Main/Main.aspx'
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'lxml')
    print(soup)

if __name__ == '__main__':
    crawl_page()