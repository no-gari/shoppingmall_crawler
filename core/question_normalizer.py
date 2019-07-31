import requests
from bs4 import BeautifulSoup
from .methods import *


def get_beautifulsoup_obj(url):
    PARSER = 'html.parser'

    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'Referer': 'https://www.ggsing.com/board/product/list.html?board_no=6&page=1000'
    }
    result = requests.get(url, headers=headers)  # 헤더 정보를 담습니다

    result_text = result.text  # 텍스트만 가져 옵니다
    soup = BeautifulSoup(result_text, PARSER)  # 파싱을 해줍니다

    return soup


### 이곳은 질문 크롤링 입니다
def url_parser(url):
    soup = get_beautifulsoup_obj(url)
    url_group = str(soup.select('tbody >tr > td'))
    url_number = re.findall('[no=]\d\d\d\d\d\d\d', url_group)  # 페이지의 항목 별 url 번호를 가져옵니다
    if '=2491125' in url_number:
        url_number.remove('=2491125')
    if '=1087230' in url_number:
        url_number.remove('=1087230')
    if '=1351599' in url_number:
        url_number.remove('=1351599')
    return url_number


def html_parser(url):
    from .auto_reply import people_ordered, people_not_ordered

    soup = get_beautifulsoup_obj(url)

    category = str(soup.select('div > div > table > tbody > tr > td'))  # 카테고리를 뽑아옵니다
    category = category.split(",")
    category_return = category.pop(0)
    if category_return == None:
        category_return = '카테고리가 없습니다'
    category_return = re.sub('<.+?>', '', category_return).strip()
    category_return = category_return.replace("[", "")

    message_raw = str(soup)
    text = "자주하는 질문 게시판"
    text2 = '</div></td></tr></tbody></table></div></div></form></div></div></div></div></body></html>'
    text3 = '<tr class="attach displaynone">'
    text4 = '<tr class="attach">'

    # 질문에서 상품 코드를 뽑아옴
    try:
        product_codes = str(soup.findAll('div', {'class': 'prdInfo'}))
        product_code = re.findall(r'\d\d\d\d\d', product_codes)
        product_num = str(product_code[0])
    except:
        product_num = 0

    if text in message_raw:
        message_raw = message_raw.replace(text2, "")
        message_raw = message_raw.replace(text3, "</div>")
        message_raw = message_raw.replace(text4, "</div>")

    message_soup = BeautifulSoup(message_raw, 'html.parser')

    message = str(message_soup.findAll('div', {'class': 'detail'}))
    message = re.sub('<.+?>', '', message).strip()
    message = message.replace('\r', '')
    message = message.replace('\n', '')
    if '*' in message:
        message = re.sub(r'^\[.+?\*', '[*', message)
    message = message.replace("[", "")
    message = message.replace("]", "")

    dttm_area = str(soup.findAll('li', {'class': 'date'}))
    registered_dttm = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', dttm_area)

    if registered_dttm:
        registered_dttm = registered_dttm.group()
    else:
        registered_dttm = '1111-11-11 11:11'

    try:
        ordered_number = re.search(r'\d{8}-\d{7}', message)  # 주문 번호가 있는 경우
    except:
        ordered_number = 0  # 주문 번호가 없는 경우

    if ordered_number != 0:
        auto_reply = people_ordered(message, product_num)  # 주문 번호가 있는 경우 자동 답변
    else:
        auto_reply = people_not_ordered(message, product_num)  # 주문 번호가 없는 경우의 자동 답변

    return category_return, message, registered_dttm, auto_reply, product_num
