import csv
import io
import os

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage


pdf_pathes=[]
for f in os.scandir('pdfs'):
    if f.is_file() and f.path.split('.')[-1].lower() == 'pdf':
        pdf_pathes.append(f.path)


def extract_text_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()

    if text:
        return text


if __name__ == '__main__':
    with open('Результат.csv', 'w', newline='', encoding='utf-8-sig') as file:
        writer=csv.writer(file, delimiter=';')
        writer.writerow(['Имя', 'Фамилия', 'Отчество', 'Дата рождения', 'Документ'])
    for pdf_path in pdf_pathes:
        try:
            try:
                last_name=extract_text_from_pdf(pdf_path).split('Фамилияобязательно')[1].split('Имяобязательно')[0]
            except:
                last_name=extract_text_from_pdf(pdf_path).split('Фамилия')[1].split('Имя')[0]
            try:
                name=extract_text_from_pdf(pdf_path).split('Имяобязательно')[1].split('Отчествопри наличии')[0]
            except:
                name=extract_text_from_pdf(pdf_path).split('Имя')[1].split('Отчество')[0]
            try:
                father_name= extract_text_from_pdf(pdf_path).split('Отчествопри наличии')[1].split('Фамилия(латинскимибуквами)')[0]
            except:
                father_name = extract_text_from_pdf(pdf_path).split('Отчество')[1].split('Фамилия')[0]
            try:
                birthday=extract_text_from_pdf(pdf_path).split('Дата рожденияобязательно')[1].split('Документ, удостоверяющий')[0]
            except:
                birthday = extract_text_from_pdf(pdf_path).split('Дата рождения')[1].split('Документ')[0]
            try:
                document=extract_text_from_pdf(pdf_path).split('Паспорт гражданина РФ,')[1].split('Адрес фактическогоместа')[0]
            except:
                document=''
            # text=extract_text_from_pdf(pdf_path)
            # print(text)
            if document=='':
                try:
                    document=extract_text_from_pdf(pdf_path).split('гражданина Российской ФедерацииСерия (приналичии) и номеробязательно')[1].split('Адрес фактического места')[0]
                except:
                    document=extract_text_from_pdf(pdf_path).split('Паспорт гражданина РФСерия (приналичии) и номеробязательно')[1].split('Адрес фактического места жительства')[0]
            else:
                print()
            if document!='-':
                document=f"'{document}'"
        except:
            print(pdf_path + ' пропущен')
            continue
        with open('Результат.csv', 'a', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([name,last_name,father_name, birthday, document])
        print(pdf_path+' обработан')