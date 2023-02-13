from django.contrib import admin
from .models import Post, Question, Response, Answer



class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1

class PostAdmin(admin.ModelAdmin):
  
    fieldsets = [
        (None,               {'fields': ['subject', 'content']}),
        ('Date information', {'fields': ['end_month', 'end_day', 'visible']}),
    ]
    inlines = [QuestionInline]

    def export_to_csv(self, request, queryset):
        pass
    
    export_to_csv.short_description = "Export Selected to csv"
        
    
admin.site.register(Post, PostAdmin)
admin.site.register(Response)
