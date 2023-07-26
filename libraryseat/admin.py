from django.contrib import admin
from .models import Result, Receipt, Reserve, Receipt_Student

import codecs
import csv
import xlwt
from django.http import HttpResponse

admin.site.register(Result)
admin.site.register(Receipt)
admin.site.register(Reserve)
admin.site.register(Receipt_Student)


class ReceiptStudentAdmin(admin.ModelAdmin):
    actions = ['xls_export']

    @admin.action(description='xls로 저장')
    def xls_export(self, request, receiptset):
        response = HttpResponse(content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = 'attachment;filename*=UTF-8\'\'yttexported.xls'
        wb = xlwt.Workbook(encoding='ansi') #encoding은 ansi로 해준다.
        ws = wb.add_sheet('응답') #시트 추가
        for i, resp in enumerate(receiptset):
            if i == 0:
                ws.write(0, 0, "이름")
                ws.write(0, 1, "학번")
                ws.write(0, 2, "학년")
                ws.write(0, 3, "흡연여부")
            ws.write(i+1, 0, resp.author.student_name)
            ws.write(i+1, 1, resp.author.student_number)
            ws.write(i+1, 2, resp.floor)
            ws.write(i+1, 3, resp.smoke)
        wb.save(response)
        return response

admin.site.register(Receipt_Student, ReceiptStudentAdmin)
