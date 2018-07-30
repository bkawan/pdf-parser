import datetime
import re

from .pdf_parser import PdfParser


def clean_king_county_pdf_file(file_path, pages=None):
    cols = ['DEF01', 'DEF02', 'PLA01', 'PLA02', 'DEC01', 'PET01', 'RSP01', 'ATY01']
    data = {
        'case_status_date':'',
        'case_list':[]
    }
    parser = PdfParser(file_path=file_path)
    raw_text = parser.convert_pdf_to_text(pages=pages)
    all_rows = re.split(r'((?:18|19|20)-[\d-]+)', raw_text)
    case_status_date_row = re.findall(r'\d{1,2}\.\d{1,2}\.\d{4}', all_rows[0])
    if not case_status_date_row:
        case_status_date_row = re.findall(r'\d{1,2}\.\d{1,2}', all_rows[0])
        if case_status_date_row:
            case_status_date_row = case_status_date_row[0] + "." + str(datetime.date.today().year)
            case_status_date_row = [case_status_date_row]
    if case_status_date_row:
        data['case_status_date'] = case_status_date_row[0]
    else:
        data['case_status_date'] = datetime.date.today().strftime('%m.%d.%Y')
    all_rows = all_rows[1:]
    keys = []
    values = []
    for index, row in enumerate(all_rows):
        value = {}
        if (index + 1) % 2 == 0:  # Even
            group = re.findall(r'(.*)(\d\d/\d\d/\d\d\d\d)(.*)', row)
            if group:
                if len(group[0]) == 3:
                    file_date = group[0][1]
                    value.update({'file_date':file_date})
                    remaining_data = group[0][2]
                    remaining_data = remaining_data.replace("   ", '$three$').replace('  ', '$two$')
                    case_type = remaining_data.split("$two$")[0].strip("$three$").strip()
                    case_type_strip_page = re.findall(r'(.*)(Page(.*))', case_type)
                    case_type_strip_scomis = re.findall(r'(.*)(SCOMIS(.*))', case_type)
                    if case_type_strip_page:
                        case_type = case_type_strip_page[0][0]
                    if case_type_strip_scomis:
                        case_type = case_type_strip_scomis[0][0]
                    value.update({'case_type':case_type})
                    for col in cols:
                        pattern = f'\$two\$({col})(.*)\$two\$'
                        regx = re.compile(pattern)
                        group = re.findall(regx, remaining_data)
                        col_value = ''
                        if group:
                            col_value = group[0][1].split('$two$')[0].strip("$three$")
                            col_value_strip_page = re.findall(r'(.*)(Page(.*))', col_value)
                            col_value_strip_scomis = re.findall(r'(.*)(SCOMIS(.*))', col_value)
                            if col_value_strip_page:
                                col_value = col_value_strip_page[0][0]
                            if col_value_strip_scomis:
                                col_value = col_value_strip_scomis[0][0]
                            col_value = col_value.replace("$three$", " ")
                        value.update({col:col_value})
            values.append(value)
        else:
            keys.append(row)

    for k, v in zip(keys, values):
        if v:
            v.update({'case_number':k})
            data['case_list'].append(v)

    return data
