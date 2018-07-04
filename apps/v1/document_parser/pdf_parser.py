from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


class PdfParser(object):
    def __init__(self, file_path):
        self.input_file = file_path

    def get_total_page(self):
        # Create a PDF parser object associated with the file object.
        input_file = open(self.input_file, 'rb')
        parser = PDFParser(input_file)
        # Create a PDF document object that stores the document structure.
        # Supply the password for initialization.
        document = PDFDocument(parser, password='')
        total_pages = document.catalog['Pages'].resolve()['Count']
        return total_pages

    def convert_pdf_to_text(self, file_path=None, pages=None):
        if not file_path:
            file_path = self.input_file
        if not pages:
            pagenums = set()
        else:
            pagenums = set(pages)

        output = StringIO()
        manager = PDFResourceManager()
        converter = TextConverter(manager, output, laparams=LAParams())
        interpreter = PDFPageInterpreter(manager, converter)
        infile = open(file_path, 'rb')
        for page in PDFPage.get_pages(infile, pagenums):
            interpreter.process_page(page)
        infile.close()
        converter.close()
        text = output.getvalue()
        output.close()
        return text


if __name__ == '__main__':
    file_path = 'sample-data/pdf-samples/1_NewCaseList.pdf'
    obj = PdfParser(file_path=file_path)
    pages = obj.get_total_page()
    print(obj.convert_pdf_to_text())
    print(pages)
    # for i in range(pages):
    #     print(obj.convert_pdf_to_text(pages=[i]))
