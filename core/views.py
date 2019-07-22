from django.shortcuts import render

def start():
    from . import models
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
            gogosing_category = models.Category.objects.create(name=res1)
            gogosing_category.save()

            # 답변 저장하는 부분
            gogosing_question = models.Question.objects.create(article=res2, date=res3,
                                                               category=gogosing_category)
            gogosing_question.save()

            # 댓글 저장하는 부분
            gogosing_replies = models.Comment.objects.create(title=gogosing_question, text=res5, date=res4)
            gogosing_replies.save()

            if i == page_len:
                break





def home(request):
    from . import models
    import math

    if request.method == "POST":
        submit_type = request.POST['submit_type']
        if submit_type == str(1):
            start()
        elif submit_type == str(2):
            comments = models.Comment.objects.all()
            comments.delete()
            questions = models.Question.objects.all()
            questions.delete()
            category = models.Category.objects.all()
            category.delete()

    questions = models.Question.objects.all().order_by('id')
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
                                                   'page_control' : page_control, 'next': next})
