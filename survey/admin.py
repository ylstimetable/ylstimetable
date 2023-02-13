from django.contrib import admin
from .models import Post, Question, Response, Answer

import codecs
import csv
from django.http import HttpResponse



class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1

    
class PostAdmin(admin.ModelAdmin):
  
    fieldsets = [
        (None,               {'fields': ['subject', 'content']}),
        ('Date information', {'fields': ['end_month', 'end_day', 'visible']}),
    ]
    inlines = [QuestionInline]
    actions = ['export_to_csv']
    
    @admin.action(description='Export selected as csv')
    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response.write(codecs.BOM_UTF8)
        for i, post in enumerate(queryset):
            if i == 0:
                response['Content-Disposition'] = 'attachment; filename={}.csv'.format(str(post))
                writer = csv.writer(response)
                header = ["user"]  
                for question in post.question_set.all():
                    header.append(question.subject)
                writer.writerow(header)
                for r in post.response_set.all(): 
                    row = writer.writerow(r.get_clean_answers())
            else:
                pass
                
       
        return response
    


admin.site.register(Post, PostAdmin)
admin.site.register(Response)
