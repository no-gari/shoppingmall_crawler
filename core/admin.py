from django.contrib import admin
from .models import Category, Question, Comment
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['article', 'date']

class CommentAdmin(admin.ModelAdmin):
    list_display = ['text', 'title', 'date']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Comment, CommentAdmin)