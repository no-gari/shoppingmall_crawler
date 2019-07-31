import re
from . import question_normalizer


# 취소 매뉴얼
def cancelation_method(mention):
    if '상품명' in mention:
        mention = str(re.findall(r'상품명.+?\*', mention))
        mention = mention.replace("[\'상품명 :", "")
        mention = mention.replace("*']", "")
    else:
        pass
    ment = '주문하신 상품' + mention + ' 바로 취소처리 해 드리겠습니다. 불편 드려서 죄송합니다. '
    return ment


# 배송 매뉴얼
def shipping_method(mention):
    try:
        ordered_number = re.search(r'\d{8}-\d{7}', mention)  # 주문 번호가 있는 경우
    except:
        ordered_number = 0  # 주문 번호가 없는 경우
    if ordered_number == 0:
        text = '현재 주문번호가 글에 적혀 있지 않아 확인이 어렵습니다. 다시 글 작성해 주시면 확인해 드리도록 하겠습니다. '
    else:
        text = '현재 송장등록되어 검수 후 이상없을경우 영업일기준 1~2일이내 출고 가능할 것으로 예상되며 검수시 이상있거나 물류량이 많을경우 출고일은 조금 지연될수 있습니다. 출고후 주문자분 휴대폰번호로 알림문자 발송 드릴 예정으로 해당 알림문자 확인 부탁드리겠습니다~'
    return text


# 상품 변경
def product_change(mention):
    ordered_product = '변경하실 상품'
    changed_product = '변경 원하시는 상품'
    if '변경하실 상품명 ' in mention:
        try:
            message = re.sub(r'변경.+?:', '', mention)
            order = message.split('*')
            ordered_product = order[2]
            changed_product = order[3]
        except:
            ordered_product = '변경하실 상품'
            changed_product = '변경 원하시는 상품'
    text = "{}에서 {}로 변경 완료했습니다. 차액금 환불기간은 영업일기준 1-3일 소요 된다는 점 안내해 드리겠습니다 ".format(ordered_product, changed_product)
    return text


# 사이즈 문의
def size_inquire():
    message = '착용하시는 체형에 따라 사이즈가 달라지고 있어 해당 부분 정확한 안내 어려운 점 양해 부탁 드립니다 '
    return message


# 재입고 문의
def restock_inquire(mention, product_num):
    from .models import Product

    product_code = int(product_num)
    try:
        product = Product.objects.get(code=product_code)
        product_name = product.name
        message = '{}은 ~까지 입고 예정이며 어쩌구 저저구 입니다. '.format(product_name)
    except:
        message = '상품을 정확히 기재해 주셔야 재고 날짜를 알려드릴 수 있습니다 '

    return message


# 쿠폰 문의
def coupon_inquire():
    message = '쿠폰, 적립금 관련 멘트는 쇼핑몰 마다 상이하므로 어쩌구 저쩌구 '
    return message
