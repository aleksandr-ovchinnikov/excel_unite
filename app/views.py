import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

def home(request):
    if request.method == 'POST':
        files = request.FILES.getlist('excel_files')

        if len(files) != 4:
            return render(request, 'app/index.html', context={'message': f'All fields should be filled!'})
        merged_file = Workbook() 

        for index, file in enumerate(files, start=1):
            df = pd.read_excel(file)
            sheet_name = f'Sheet {index}'

            sheet = merged_file.create_sheet(sheet_name)
            for row in dataframe_to_rows(df, index=False, header=True):
                sheet.append(row)

        merged_file.remove(merged_file.active)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=merged_file.xlsx'
        merged_file.save(response)

        return response

    return render(request, 'app/index.html')

