from django.db import models
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=32, verbose_name='카테고리 이름')

    class Meta:
        verbose_name = '카테고리'
        verbose_name_plural = '카테고리'

class Product(models.Model):
    name = models.CharField(max_length=64, verbose_name='상품 이름', default='상품 이름')
    code = models.IntegerField(verbose_name='상품 코드')

    class Meta:
        verbose_name = '상품'
        verbose_name_plural = '상품'

class Question(models.Model):
    product_code = models.IntegerField(verbose_name='상품 코드', default=0)
    article = models.TextField(verbose_name='질문 제목')
    date = models.DateTimeField(verbose_name='등록 시간')
    category = models.ForeignKey(Category, verbose_name='카테고리', on_delete=models.CASCADE)
    class Meta:
        verbose_name = '질문'
        verbose_name_plural = '질문'

class Autoreply(models.Model):
    url_address = models.TextField(verbose_name='url 주소', default='www.gogosing.com')
    auto_reply = models.TextField(verbose_name='자동 답변', default='답변 불가능한 항목입니다')
    question = models.ForeignKey(Question, verbose_name='질문', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '자동답변'
        verbose_name_plural = '자동답변'