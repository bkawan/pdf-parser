from .pdf_parser import PdfParser


def clean_king_county_pdf_file(file_path):
    cleaned_data = ''
    raw_data = PdfParser(file_path=file_path)

    cleaned_data = raw_data.convert_pdf_to_text()

    return cleaned_data
