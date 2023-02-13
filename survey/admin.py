from django.contrib import admin
from .models import Post, Question, Response, Answer

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
        
        for i, post in enumerate(queryset):
            if i == 0:
                response['Content-Disposition'] = 'attachment; filename={}.csv'.format(str(post))
                writer = csv.writer(response)
                header = ["user"]  
                for question in post.question_set.all():
                    header.append(question.subject)
                print(header)
            else:
                pass
                
       
        '''
        return header, question_order
            else:
                if settings.EXCEL_COMPATIBLE_CSV:
                    survey_as_csv = str(survey_as_csv).replace(f"{Survey2Csv.EXCEL_HACK}\n", "")
                if i != 0:
                    filename += f"-{survey.safe_name}"
                elif settings.EXCEL_COMPATIBLE_CSV:
                    # If we need to be compatible with excel and it's the first survey
                    response.write(f"{Survey2Csv.EXCEL_HACK}\n")
                response.write(f"{survey.name}\n")
                response.write(survey_as_csv)
                response.write("\n\n")
        response["Content-Disposition"] = f"attachment; filename={filename}.csv"
        '''
        return response
    


admin.site.register(Post, PostAdmin)
admin.site.register(Response)
