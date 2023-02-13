from django.contrib import admin
from .models import Post, Question, Response, Answer

import codecs
import csv
import xlwt
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
    actions = ['export_to_csv', 'xls_export']
    
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
        
    
    @admin.action(description='xls로 저장')
    def xls_export(self, request, queryset):
        response = HttpResponse(content_type="application/vnd.ms-excel")
        
        
        for i, post in enumerate(queryset):
            if i == 0:
                response["Content-Disposition"] = 'attachment;filename*=UTF-8\'\'{}.xls'.format(str(post))
                wb = xlwt.Workbook(encoding='ansi') #encoding은 ansi로 해준다.
                
                ws = wb.add_sheet('답변') #시트 추가
                
                ws.write(0, 0, "user")
                for i, question in enumerate(post.question_set.all()):
                    ws.write(0, i+1, question.subject)
                    
        return reponse
    '''
    
    #데이터 베이스에서 유저 정보를 불러온다.
    rows = User.objects.all().values_list('name', 'email') 
    
    #유저정보를 한줄씩 작성한다.
    for row in rows:
    	row_num +=1
        for col_num, attr in enumerate(row):
        	ws.write(row_num, col_num, attr)
            
    wb.save(response)
    '''
    


admin.site.register(Post, PostAdmin)
admin.site.register(Response)
