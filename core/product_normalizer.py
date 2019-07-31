import requests
import re
from bs4 import BeautifulSoup

PARSER = 'html.parser'

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Referer': 'https://www.ggsing.com/board/product/list.html?board_no=6&page=1000'
}


### 이곳은 상품 크롤링 입니다
def product_url_parser(url):
    result = requests.get(url, headers=headers)  # 헤더 정보를 담습니다

    result_text = result.text  # 텍스트만 가져 옵니다
    soup = BeautifulSoup(result_text, PARSER)  # 파싱을 해줍니다
    page_list = str(soup.findAll('div', {'class': 'xans-product-normalpaging'}))
    soup = BeautifulSoup(page_list, PARSER)
    page_list = str(soup.findAll('ol'))
    product_list = re.findall(r'page=\d', page_list)

    return product_list


def product_html_parser(url):
    result = requests.get(url, headers=headers)  # 헤더 정보를 담습니다
    result_text = result.text  # 텍스트만 가져 옵니다
    soup = BeautifulSoup(result_text, PARSER)  # 파싱을 해줍니다
    url_group = str(soup.findAll('div', {'class': 'xans-product-listnormal'}))
    product_names = list(re.findall(r'a href="/product/.+?/', url_group))
    for i in range(0, len(product_names)):
        product_names[i] = product_names[i].replace('a href="/product/', '')
        product_names[i] = product_names[i].replace('무료배송', '')
        product_names[i] = product_names[i].replace('당일출고', '')
        product_names[i] = product_names[i].replace('/', '')

    product_nums = list(re.findall(r'anchorBoxId_\d\d\d\d\d', url_group))
    for i in range(0, len(product_nums)):
        product_nums[i] = product_nums[i].replace("anchorBoxId_", "")

    return product_names, product_nums
