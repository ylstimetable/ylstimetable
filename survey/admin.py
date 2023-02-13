from django.contrib import admin
from .models import Post, Question, Response, Answer


@admin.action(description='Export selected as csv')
def export_to_csv(self, request, queryset):
    pass

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1

class PostAdmin(admin.ModelAdmin):
  
    fieldsets = [
        (None,               {'fields': ['subject', 'content']}),
        ('Date information', {'fields': ['end_month', 'end_day', 'visible']}),
    ]
    inlines = [QuestionInline]
    actions = [export_to_csv]

admin.site.register(Post, PostAdmin)
admin.site.register(Response)
