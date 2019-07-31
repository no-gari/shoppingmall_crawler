from django.contrib import admin
from .models import Category, Question, Autoreply
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['article', 'date']

class ReplyAdmin(admin.ModelAdmin):
    list_display = ['url_address', 'auto_reply', 'question']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Autoreply, ReplyAdmin)