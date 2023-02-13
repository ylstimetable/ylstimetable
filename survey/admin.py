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
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(str(self.model))
        print('attachment; filename={}.csv'.format(str(self.model)))
        writer = csv.writer(response)

        for obj in queryset:
            print(obj)
            #row = writer.writerow([getattr(obj, field) for field in field_names])

        return response


admin.site.register(Post, PostAdmin)
admin.site.register(Response)
