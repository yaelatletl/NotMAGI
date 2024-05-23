import io
import pdfminer
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter

def convert_pdf_to_text(path):
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    codec = 'utf-8'
    capacity = 16777216
    caching = True
    interpreter = PDFPageInterpreter(rsrcmgr, TextConverter(codec, laparams=laparams, capacity=capacity, caching=caching))

    fp = open(path, 'rb')
    document = PDFDocument(fp)

    output = io.StringIO()
    for page in document.get_pages():
        interpreter.process_page(page)
        text = interpreter.get_result()
        output.write(text)

    fp.close()
    document.close()
    output.close()

    return output.getvalue()