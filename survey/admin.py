from django.contrib import admin
from .models import Post, Question, Response, Answer



class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1

class PostAdmin(admin.ModelAdmin):
  
    fieldsets = [
        (None,               {'fields': ['subject', 'content']}),
        ('Date information', {'fields': ['create_date', 'end_date', 'visible']}),
    ]
    inlines = [QuestionInline]

    
admin.site.register(Post, PostAdmin)
