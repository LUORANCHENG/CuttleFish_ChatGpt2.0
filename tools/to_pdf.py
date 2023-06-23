import os
from win32com import client
from docx2pdf import convert
import pythoncom
import threading


def to_pdf(file):
    pythoncom.CoInitialize()
    pdf_path = f'{file.strip(".docx")}.pdf'
    convert(file, pdf_path)
    pythoncom.CoUninitialize()
    pass

# def docx2pdf(file):
#     pythoncom.CoInitialize()
#     pdf_path = f'{file.strip(".docx")}.pdf'
#     word = client.Dispatch("Word.Application")
#     doc = word.Documents.Open(file)
#     doc.SaveAs(pdf_path, 17)
#     doc.Close()
#     word.Quit()
#     pythoncom.CoUninitialize()


# def main(file):
#     to_pdf(file)

pdf_gen_lock_ = threading.Lock()
def docx2pdf(file):
    with pdf_gen_lock_:
        pythoncom.CoInitialize()
        pdf_path = f'{file.strip(".docx")}.pdf'
        print(pdf_path)
        word = client.Dispatch("Word.Application")
        doc = word.Documents.Open(file)
        doc.SaveAs(pdf_path, 17)
        doc.Close()
        word.Quit()
        pythoncom.CoUninitialize()

def main(file):
    threads = []
    t = threading.Thread(target=docx2pdf, args=(file,))
    threads.append(t)
    t.start()
    for t in threads:
        t.join()

if __name__ == '__main__':
    main('D:/python_project/test1/1.docx')