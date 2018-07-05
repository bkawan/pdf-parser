import re

from .pdf_parser import PdfParser


def clean_king_county_pdf_file(file_path, pages=None):
    parser = PdfParser(file_path=file_path)
    splitter = "------------------------------------------------------------------------------"
    raw_data = parser.convert_pdf_to_text(pages=pages)
    rows = re.split(splitter, raw_data)
    rows.pop()  ## last one is just page number
    data = {
        'case_status_date':'',
        'case_list':[]
    }
    for i, x in enumerate(rows):
        if i == 0:
            group = re.search(r'New\s+Case\s+List(.*)PAGE[\s]+\d', x.strip())
            case_status_data = group.group().split(' ')[3]
            data['case_status_date'] = case_status_data.strip()
            each_row = x.strip().replace(group.group(), '').strip().split(" ")
        else:
            group = re.search(r'SCOMIS(.*)PAGE[\s]+\d', x.strip())
            if group:
                each_row = x.strip().replace(group.group(), '').strip().split(" ")
            else:
                each_row = x.strip().split(" ")

        try:
            case_number = each_row[0]
        except IndexError:
            case_number = 'Error'

        try:
            case_type = each_row[6]
        except IndexError:
            case_type = 'Error'

        try:
            file_date = each_row[3]
        except IndexError:
            file_date = 'Error'
        data['case_list'].append({
            'case_number':case_number,
            'case_type':case_type,
            'file_date':file_date,
        })

    return data
