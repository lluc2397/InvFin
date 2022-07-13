from django.contrib import admin

from .models import Answer, AnswerComment, QuesitonComment, Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'author'
        ]
    
    list_editable = [
        'author'
    ]

    search_fields = ['author_username']


@admin.register(QuesitonComment)
class QuesitonCommentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'author',
        'created_at']
    
    search_fields = ['author_username']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'author'
        ]
    
    list_editable = [
        'author'
    ]
    search_fields = ['author_username']


@admin.register(AnswerComment)
class AnswerCommentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'author',
        'created_at']
    
    search_fields = ['author_username']
