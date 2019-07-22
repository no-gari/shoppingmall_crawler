from django.db import models
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=32, verbose_name='카테고리 이름')

    class Meta:
        verbose_name = '카테고리'
        verbose_name_plural = '카테고리'


class Question(models.Model):

    article = models.CharField(max_length=2000, verbose_name='질문 제목')
    date = models.DateTimeField(verbose_name='등록 시간')
    category = models.ForeignKey(Category, verbose_name='카테고리', on_delete='CASCADE')

    class Meta:
        verbose_name = '질문'
        verbose_name_plural = '질문'


class Comment(models.Model):
    text = models.CharField(max_length=2000, verbose_name='답변 내용')
    date = models.DateTimeField(verbose_name='등록 시간')
    title = models.ForeignKey(Question, verbose_name='질문', on_delete='CASCADE')

    class Meta:
        verbose_name = '답변'
        verbose_name_plural = '답변'