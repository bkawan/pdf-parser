from .pdf_parser import PdfParser


def clean_king_count_pdf_file(file_path):
    cleaned_data = ''
    raw_data = PdfParser(file_path=file_path)

    return cleaned_data
