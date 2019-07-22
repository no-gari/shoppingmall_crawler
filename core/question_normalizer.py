import requests
from bs4 import BeautifulSoup
import re

PARSER = 'html.parser'

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Referer': 'https://www.ggsing.com/board/product/list.html?board_no=6&page=1000'
}

def url_parser(url):
    result = requests.get(url, headers= headers) #헤더 정보를 담습니다

    result_text = result.text   #텍스트만 가져 옵니다
    soup = BeautifulSoup(result_text, PARSER)   #파싱을 해줍니다
    url_group = str(soup.select('tbody >tr > td'))
    url_number = re.findall('[no=]\d\d\d\d\d\d\d', url_group)   #페이지의 항목 별 url 번호를 가져옵니다
    return url_number


def html_parser(url):
    result = requests.get(url, headers=headers)  # 헤더 정보를 담습니다

    result_text = result.text  # 텍스트만 가져 옵니다
    soup = BeautifulSoup(result_text, PARSER)  # 파싱을 해줍니다

    category = str(soup.select('div > div > table > tbody > tr > td'))  # 카테고리를 뽑아옵니다
    if category == None:
        category = '카테고리가 없습니다'
    category = re.sub('<.+?>', '', category).strip()

    text = '<b>글 남겨주시기 전 <b><font color="red">자주하는 질문 게시판</font></b></b></div></td></tr></tbody></table></div></div></form></div></div></div></div></body></html>에서 다시한번 확인해주시길 바랍니다<br/>'
    text2 = '</div></td></tr></tbody></table></div></div></form></div></div></div></div></body></html>'
    text3 = '<tr class="attach displaynone">'
    message_raw = str(soup)
    trash_raw = str(soup.findAll('b'))
    if "</b></font>" in trash_raw:
        trash_raw = trash_raw.replace("</b></font>", "")
        trash_raw = BeautifulSoup(trash_raw, PARSER)
        trash = str(trash_raw.findAll('b'))
        if "</b>," in trash:
            trash = trash.replace("</b>,", "")
    elif "</font></b>" in trash_raw:
        trash_raw = trash_raw.replace("</font></b>", "")
        trash_raw = BeautifulSoup(trash_raw, PARSER)
        trash = str(trash_raw.findAll('b'))
        if "</b>," in trash:
            trash = trash.replace("</b>,", "")
    else:
        trash = trash_raw

    if "</b>, " in trash:
        trash = trash.replace("</b>, ", "")


    if trash:
        trash = re.sub('<.+?>', '', trash).strip()
        trash = trash.replace("[0,  ", "")
        trash = trash.replace("[0,", "")
        trash = trash.replace("[0", "")
        trash = trash.replace("]", "")

    message_raw = message_raw.replace(text, "")
    message_raw = message_raw.replace(text3, text2)
    message_raw = BeautifulSoup(message_raw, PARSER)
    message = str(message_raw.findAll('div', {'class': 'detail'}))
    if message:
        message = re.sub('<.+?>', '', message).strip()
        message = message.replace(trash, "")

        # if message == '[]':
        #     message = "질문이 없습니다"

    text4 = "ㅁ 일반상품은 주문후 2~3일이내 출고됩니다.\r\nㅁ 예약판매상품 또는 입고지연상품을 함께 구매하셨을경우, 출고가 늦어질 수 있습니다.\r\nㅁ 입고지연안내 게시판을 참고해주세요!\r\nㅁ사진첨부를 원하시는 경우에는 비밀게시판을 이용해주시면 가능하세요"
    text4_ = "ㅁ 일반상품은 주문후 2~3일이내 출고됩니다.ㅁ 예약판매상품 또는 입고지연상품을 함께 구매하셨을경우, 출고가 늦어질 수 있습니다.ㅁ 입고지연안내 게시판을 참고해주세요!ㅁ사진첨부를 원하시는 경우에는 비밀게시판을 이용해주시면 가능하세요"
    text5 = "글 남겨주시기 전 자주하는 질문 게시판에서 다시한번 확인해주시길 바랍니다"
    text6 = "ㅁ 이미 출고된 상품은 주소지변경이 되지 않습니다.\r\nㅁ 송장입력된 후, 주소지변경을 요청해주시면 상품출고가 지연될 수 있습니다.\r\n주소지 변경을 원하시는 경우 개인 정보로 인해 비밀게시판에 글 남겨주시면 주소지 변경 처리 도와드리겠습니다."
    if text4 in message:
        message = message.replace(text4, "")
    if text4_ in message:
        message = message.replace(text4, "")
    if text5 in message:
        message = message.replace(text5, "")
    if text6 in message:
        message = message.replace(text6, "")


    dttm_area = str(soup.findAll('li', {'class': 'date'}))
    registered_dttm = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', dttm_area)

    if registered_dttm:
        registered_dttm = registered_dttm.group()
    else:
        registered_dttm = '1111-11-11 11:11'

    reply = str(soup.find('li', {'class': 'first xans-record-'}))  # 답변 섹션 파싱
    reply_dttm = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', reply)
    if reply_dttm:
        reply_dttm = reply_dttm.group()
    else:
        reply_dttm = '1111-11-11 11:11'  # 답변 날짜 뽑아오기
    reply_article = str(soup.find('p', {'class': 'comment'}))  # 답변 내용 파싱
    if reply_article == 'None':
        reply_article = "답변이 없습니다"
    else:
        reply_article = re.sub('<.+?>', '', reply_article).strip()  # 답변 내용 뽑아오기

    return category, message, registered_dttm, reply_dttm, reply_article