from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .forms import *
from . import models
from django.contrib.auth import login as auth_login, authenticate as auth


def index(request):
    return render(request, 'core/user/index.html')


def login(request):
    if request.user.is_anonymous != True:
        return redirect('home')

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = auth(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
    else:
        login_form = LoginForm()
    return render(request, 'core/user/login.html', {'login_form': login_form})


def signup(request):
    signup_form = SignUpForm(data=request.POST or None)

    text = ''
    if request.method == 'POST':
        if signup_form.is_valid():
            new_user = User.objects.create_user(**signup_form.cleaned_data)
            new_user.save()
            text = '가입 성공'
        else:
            text = '가입 실패'

    return render(request, 'core/user/signup.html',{
        'signup_form': signup_form,
        'text': text
    })


def start2():
    from . import product_normalizer as p

    category_list = [31, 46, 47, 26, 297, 7, 28, 27, 29, 1771]
    for i in range(0, len(category_list)):
        product_url_base = 'https://www.ggsing.com/product/list.html?cate_no='
        product_url = product_url_base+ str(category_list[i])
        page_list = p.product_url_parser(product_url)
        for j in range(0, len(page_list)):
            product_url_page = product_url_base+ str(category_list[i]) +'&' + page_list[j]
            product_name_list, product_code_list = p.product_html_parser(product_url_page)
            for k in range(0, len(product_code_list)):
                gogosing_product = models.Product.objects.create(code=product_code_list[k], name=product_name_list[k])
                gogosing_product.save()


def start():
    from . import question_normalizer

    for j in range(1, 2000):
        url_base = "https://www.ggsing.com/board/product/list.html?board_no=6&page="
        url_page = url_base + str(j)  # 페이지를 띄우는 url 입니다
        page_list = question_normalizer.url_parser(url_page)  # question_normalizer에서 리스트 목록을 가져옵니다
        page_len = len(page_list)  # 페이지 리스트 개수를 가져옵니다.

        for i in range(0, page_len):
            url_list = "https://www.ggsing.com/board/product/read.html?no" + page_list[i] + "&board_no=6&page=" + str(j)

            res1, res2, res3, res4, res5 = question_normalizer.html_parser(url_list)

            if res2 == '[]':
                continue

            # 카테고리 저장 하는 부분
            gogosing_category = models.Category.objects.filter(name=res1)
            if gogosing_category.count() > 0:
                gogosing_category = gogosing_category.first()
            else:
                gogosing_category = models.Category.objects.create(name=res1)
                gogosing_category.save()

            # 질문 저장하는 부분
            gogosing_question = models.Question.objects.create(article=res2, date=res3, product_code=res5,
                                                               category=gogosing_category)
            gogosing_question.save()

            # 자동 답변 저장하는 부분
            gogosing_autoreply = models.Autoreply.objects.create(url_address=url_list, auto_reply=res4, question=gogosing_question)
            gogosing_autoreply.save()

            if i == page_len:
                break


def home(request):
    import math

    if request.user.is_anonymous == True:
        return redirect('/')

    category = models.Category.objects.all().order_by('id')
    questions = models.Question.objects.all().order_by('category_id')
    total_counts = questions.count()
    current_page = request.GET.get('page', 1) # 현재 페이지
    page_now = int(current_page) # 현재 페이지 사용하기 위해서
    lists_per_page = 10  # 한 페이지당 게시물 수
    page_total = math.ceil(total_counts / lists_per_page)
    start_list = (page_now - 1) * lists_per_page  # 페이지마다 시작하는 게시물
    end_list = start_list + lists_per_page  # 페이지마다 끝나는 게시물
    questions = questions[int(start_list): int(end_list)]
    first_page = math.floor(page_now *0.1) * lists_per_page + 1 #페이지네이션 10개씩 끊기 //
    last_page = first_page + lists_per_page #페이지네이션 10개씩 끊기


    if page_now % 10 == 0:
        first_page = first_page - 10
        last_page = last_page - 10
    if last_page > page_total:
        last_page = page_total + 1

    next= {}
    next[0] = 0
    if math.floor(page_total/10) == math.floor(first_page/10):
        next[0] = 1

    prev_page = first_page - 10
    after_page = last_page

    if first_page == 1:
        prev_page = 1

    pages = {}
    pages[0] = prev_page
    pages[1] = after_page
    page_control = {}
    page_control[0] = first_page
    page_control[1] = last_page

    dic_page_total = {}
    for i in range(first_page, last_page):
        dic_page_total[i] = i

    return render(request, 'core/user/home.html', {'questions': questions, 'dic_page_total': dic_page_total, 'pages': pages,
                                                   'page_control' : page_control, 'next': next, 'category' : category})


@api_view(['POST'])
def crawling(request):
    if request.method == 'POST':
        send_data = request.POST['send_data']
        if send_data == 'start':
            start()
        elif send_data == 'delete':
            auto_reply = models.Autoreply.objects.all()
            auto_reply.delete()
            questions = models.Question.objects.all()
            questions.delete()
            category = models.Category.objects.all()
            category.delete()
        elif send_data == 'product_start':
            start2()
        elif send_data == 'product_delete':
            product = models.Product.objects.all()
            product.delete()
        return Response({'message': '크롤링이 실행되었습니다.', 'data': send_data})
