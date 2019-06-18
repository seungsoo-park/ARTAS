from selenium import webdriver
from bs4 import BeautifulSoup
from math import ceil
import os


def crawler():
    i = 1
    driver.implicitly_wait(10)
    driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[2]/div').click()

    if len(driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[1]/div/div/div/div[1]/div').text.split(' ')) == 2:
        max_page_num = ceil(float(driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[1]/div/div/div/div[1]/div').text.split(' ')[0]) / 10)
    else:
        max_page_num = ceil(float(driver.find_element_by_xpath('//*[@id="app"]/div/div/div[2]/div[1]/div/div/div/div[1]/div').text.split(' ')[1].replace(',', '')) / 10)

    print('{} total pages : {}'.format(flag, max_page_num))
    for page_num in range(1, max_page_num + 1):
        if page_num % 10 == 0:
            print('- Remain pages : {}'.format(max_page_num - page_num))
        driver.get(url + '&page=' + str(page_num))

        button_list = driver.find_elements_by_css_selector('.search-result-abstract .less, .search-result-abstract .more')
        for val in button_list:
            val.click()

        soup = BeautifulSoup(driver.page_source, 'lxml')
        for val in soup.find_all(class_='search-result'):
            if val.find(class_='search-result-abstract') is None:
                continue
            title = val.find(class_='search-result-title').text.strip()
            abstract = val.find(class_='search-result-abstract').text.replace('(Less)', '').strip()
            year = val.find().text.strip()[-4:]
            if not os.path.exists('../paper_data/{}/{}/'.format(flag, year)):
                os.makedirs('../paper_data/{}/{}/'.format(flag, year))
            with open('../paper_data/{}/{}/{}.txt'.format(flag, year, i), 'w', encoding='utf-8') as fp:
                fp.write('{}\n{}'.format(title, abstract))
            i += 1


if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome('./chromedriver_win32/chromedriver', options=options)

    """NDSS"""
    flag = 'NDSS'
    url = 'https://www.semanticscholar.org/search?year%5B0%5D=2009&year%5B1%5D=2018&venue%5B0%5D=NDSS&publicationType%5B0%5D=JournalArticle&q=NDSS&sort=year'
    driver.get(url)
    crawler()
    """ACM"""
    flag = 'ACM'
    url = 'https://www.semanticscholar.org/search?year%5B0%5D=2009&year%5B1%5D=2018&venue%5B0%5D=ACM%20Conference%20on%20Computer%20and%20Communications%20Security&publicationType%5B0%5D=JournalArticle&q=ACM%20CCS&sort=year'
    driver.get(url)
    crawler()
    """USENIX"""
    flag = 'USENIX'
    url = 'https://www.semanticscholar.org/search?year%5B0%5D=2009&year%5B1%5D=2018&venue%5B0%5D=USENIX%20Security%20Symposium&publicationType%5B0%5D=JournalArticle&q=USENIX%20Security&sort=year'
    driver.get(url)
    crawler()
    """IEEE"""
    flag = 'IEEE'
    url = 'https://www.semanticscholar.org/search?year%5B0%5D=2009&year%5B1%5D=2018&venue%5B0%5D=IEEE%20Security%20%26%20Privacy&publicationType%5B0%5D=JournalArticle&q=IEEE%20Security&sort=year'
    driver.get(url)
    crawler()

    driver.quit()
