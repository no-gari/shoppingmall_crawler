from .methods import *


def people_ordered(statement, product_num):
    shipping = ['배송', '발송', '출고', '주문']
    coupons = ['쿠폰발급', '할인쿠폰', '쿠폰할인', '쿠폰지급', '보상제도', '쿠폰', '적립금']
    return_statement = '안녕하세요 고객님 ^^ '
    return_closing_statement = '감사합니다 ^^'
    list2 = ['변경', '교환']

    # 취소 관련
    if '취소' in statement:
        mention = cancelation_method(statement)
        return_statement += mention

    #배송, 입고 관련
    for i in range(0, len(shipping)):
        if shipping[i] in statement:
            mention = shipping_method(statement)
            return_statement += mention
            break

    #변경 관련
    for i in range(0, len(list2)):
        if list2[i] in statement:
            mention = product_change(statement)
            return_statement += mention
            break

    # 사이즈 관련
    if '사이즈' in statement:
        mention = size_inquire()
        return_statement += mention

    # 재입고 문의
    if '재입고' in statement:
        mention = restock_inquire(statement, product_num)
        return_statement += mention

    # 쿠폰 문의
    for i in range(0, len(coupons)):
        if coupons[i] in statement:
            mention = coupon_inquire()
            return_statement += mention
            break

    return return_statement + return_closing_statement

def people_not_ordered(statement, product_num):
    coupons = ['쿠폰발급', '할인쿠폰', '쿠폰할인', '쿠폰지급', '보상제도', '쿠폰', '적립금']
    return_statement = '안녕하세요 고객님 ^^ '
    return_closing_statement = '감사합니다 ^^'

    # 사이즈 관련
    if '사이즈' in statement:
        mention = size_inquire()
        return_statement += mention

    # 재입고 문의
    if '재입고' in statement:
        mention = restock_inquire(statement, product_num)
        return_statement += mention

    # 쿠폰 문의
    for i in range(0, len(coupons)):
        if coupons[i] in statement:
            mention = coupon_inquire()
            return_statement += mention
            break

    return return_statement + return_closing_statement
