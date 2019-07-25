import requests
from bs4 import BeautifulSoup
import re
from emoji import UNICODE_EMOJI

PARSER = 'html.parser'

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Referer': 'https://www.ggsing.com/board/product/list.html?board_no=6&page=1000'
}

### 이곳은 상품 크롤링 입니다
# def product_url_parser(url):
#     result = requests.get(url, headers= headers) #헤더 정보를 담습니다
#
#     result_text = result.text   #텍스트만 가져 옵니다
#     soup = BeautifulSoup(result_text, PARSER)   #파싱을 해줍니다
#     page_list = str(soup.findAll('div', {'class': 'xans-product-normalpaging'}))
#     soup = BeautifulSoup(page_list, PARSER)
#     page_list = str(soup.findAll('ol'))
#     list = re.findall(r'page=\d', page_list)
#
#     return list

#
# def product_html_parser(url):
#     result = requests.get(url, headers= headers) #헤더 정보를 담습니다
#     result_text = result.text   #텍스트만 가져 옵니다
#     soup = BeautifulSoup(result_text, PARSER)   #파싱을 해줍니다
#     url_group = soup.findAll('div', {'class': 'xans-product-listnormal'})
#     product_nums = re.findall('[anchorBoxId_]\d\d\d\d\d', url_group)
#     for elements i

### 이곳은 질문 크롤링 입니다
def url_parser(url):
    result = requests.get(url, headers= headers) #헤더 정보를 담습니다

    result_text = result.text   #텍스트만 가져 옵니다
    soup = BeautifulSoup(result_text, PARSER)   #파싱을 해줍니다
    url_group = str(soup.select('tbody >tr > td'))
    url_number = re.findall('[no=]\d\d\d\d\d\d\d', url_group)   #페이지의 항목 별 url 번호를 가져옵니다
    if '=2491125' in url_number:
        url_number.remove('=2491125')
    if '=1087230' in url_number:
        url_number.remove('=1087230')
    if '=1351599' in url_number:
        url_number.remove('=1351599')
    return url_number


def html_parser(url):
    result = requests.get(url, headers=headers)  # 헤더 정보를 담습니다

    result_text = result.text  # 텍스트만 가져 옵니다
    soup = BeautifulSoup(result_text, PARSER)  # 파싱을 해줍니다

    category = str(soup.select('div > div > table > tbody > tr > td'))  # 카테고리를 뽑아옵니다
    category = category.split(",")
    category_return = category.pop(0)
    if category_return == None:
        category_return = '카테고리가 없습니다'
    category_return = re.sub('<.+?>', '', category_return).strip()
    for emoji in UNICODE_EMOJI:
        category_return = category_return.replace(emoji, '')
    category_return = category_return.replace("[", "")

    message_raw = str(soup)
    text = "자주하는 질문 게시판"
    text2 = '</div></td></tr></tbody></table></div></div></form></div></div></div></div></body></html>'
    text3 = '<tr class="attach displaynone">'
    text4 = '<tr class="attach">'

    if text in message_raw:
        message_raw = message_raw.replace(text2, "")
        message_raw = message_raw.replace(text3, "</div>")
        message_raw = message_raw.replace(text4, "</div>")

    message_soup = BeautifulSoup(message_raw, PARSER)

    message = str(message_soup.findAll('div', {'class': 'detail'}))
    message = re.sub('<.+?>', '', message).strip()
    message = message.replace('\r', '')
    message = message.replace('\n', '')
    if '*' in message:
        message = re.sub(r'^\[.+?\*', '[*', message)
    for emoji in UNICODE_EMOJI:
        message = message.replace(emoji, '')
    message = message.replace("[", "")
    message = message.replace("]", "")


    dttm_area = str(soup.findAll('li', {'class': 'date'}))
    registered_dttm = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', dttm_area)

    if registered_dttm:
        registered_dttm = registered_dttm.group()
    else:
        registered_dttm = '1111-11-11 11:11'

    reply = str(soup.find('li', {'class': 'first xans-record-'}))  # 답변 섹션 파싱 -> 문제 없음
    reply_dttm = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', reply)
    if reply_dttm:
        reply_dttm = reply_dttm.group()
    else:
        reply_dttm = '1111-11-11 11:11'  # 답변 날짜 뽑아오기
    reply_article = str(soup.find('p', {'class': 'comment'}))  # 답변 내용 파싱 -> 문제 없음
    if reply_article == 'None':
        reply_article = "답변이 없습니다"
    else:
        reply_article = re.sub('<.+?>', '', reply_article).strip()  # 답변 내용 뽑아오기 -> 문제 없음

    return category_return, message, registered_dttm, reply_dttm, reply_article