from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
import os
import random
import string

# Загрузка кириллического шрифта
pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))

# Создаем новый PDF-документ
pdf = canvas.Canvas('C.pdf')

# Устанавливаем кириллический шрифт для текста
pdf.setFont("Arial", 12)

# Добавляем текст на первую страницу
pdf.drawString(100, 700, "Привет, это содержимое файла C.pdf!")

# Сохраняем и закрываем PDF-документ
pdf.save()


def set_password(input_file, output_file, password):
    # Чтение входного файла
    pdf_reader = PdfReader(input_file)
    
    # Создание объекта для записи выходного файла
    pdf_writer = PdfWriter()
    
    # Установка пароля на каждую страницу файла
    for page in pdf_reader.pages:
        pdf_writer.add_page(page)
        pdf_writer.encrypt(user_password=password, owner_password=None, 
                           use_128bit=True)
    
    # Сохранение выходного файла с паролем
    with open(output_file, 'wb') as file:
        pdf_writer.write(file)


# # Пример использования
# input_file = 'sample.pdf'  # Исходный PDF-файл
# output_file = 'encrypted_sample.pdf'  # Выходной PDF-файл с паролем
# password = '123'  # Пароль для установки

# set_password(input_file, output_file, password)

# Открытие зашифрованного PDF-файла
with open('encrypted_sample.pdf', 'rb') as file:
    pdf_reader = PdfReader(file)
    # Проверка, зашифрован ли документ паролем
    if pdf_reader.is_encrypted:
        # Ввод пароля для дешифровки
        password = input('Введите пароль: ')

        # Попытка дешифровки с использованием пароля
        if pdf_reader.decrypt('123') == 2:
            # Создание нового объекта PdfFileWriter для сохранения дешифрованного документа
            pdf_writer = PdfWriter()

            # Копирование содержимого из зашифрованного файла в новый документ
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                pdf_writer.add_page(page)

            # Сохранение дешифрованного документа в новый файл
            with open('decrypted_sample.pdf', 'wb') as output_file:
                pdf_writer.write(output_file)

            print('Документ успешно дешифрован.')
        else:
            print('Неверный пароль или дешифровка не удалась.')
    else:
        print('Документ не зашифрован.')

# Укажите путь к файлу sample.pdf
file_path = 'decrypted_sample.pdf'

# Открываем файл PDF для чтения
with open(file_path, 'rb') as file:
    # Создаем объект PdfReader и загружаем файл
    pdf_reader = PdfReader(file)

    # Получаем количество страниц в документе
    num_pages = len(pdf_reader.pages)

    # Извлекаем текст со всех страниц
    extracted_text = ''
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        extracted_text += page.extract_text()

    # Выводим извлеченный текст
    print(extracted_text)


def generate_random_text(length):
    """Генерирует произвольный рандомный текст заданной длины."""
    letters = string.ascii_letters + string.digits + string.punctuation + " "
    return ''.join(random.choice(letters) for _ in range(length))


# Создаем новую директорию
new_directory = 'Pdf_files'

# Проверяем, существует ли уже директория с таким именем
if not os.path.exists(new_directory):
    # Создаем новую директорию
    os.mkdir(new_directory)
    print(f"Создана новая директория: {new_directory}")
else:
    print(f"Директория {new_directory} уже существует.")

# Запросить количество файлов для создания
num_files = int(input("Введите количество файлов для создания: "))

directory = new_directory

# Создать указанное количество файлов формата PDF
for i in range(num_files):
    # Генерировать произвольное имя файла
    file_name = f"file{i+1}.pdf"
    file_path = os.path.join(directory, file_name)
    
    # Создать новый PDF-документ
    pdf = canvas.Canvas(file_path)
    
    # Заполнить документ произвольным текстом
    random_text = generate_random_text(1000)  # Измените длину текста по своему усмотрению
    pdf.setFont("Helvetica", 12)
    pdf._leading = 20
    
    # Координаты начала текста
    x = 100
    y = 700

    # Максимальная ширина блока текста
    max_width = 400

    # Перебираем слова и добавляем их в PDF
    for letter in random_text:
        # Проверяем, если добавление текущего слова выходит за пределы блока текста
        if pdf.stringWidth(pdf._escape(letter)) + x > max_width:
            # Переносим на новую строку
            y -= pdf._leading
            x = 100

        # Добавляем слово на текущую позицию
        pdf.drawString(x, y, letter)

        # Увеличиваем x на ширину добавленного слова
        x += pdf.stringWidth(pdf._escape(letter))
    
    # Сохранить и закрыть PDF-документ
    pdf.save()
    
    print(f"Создан файл {file_name} в директории {directory}")

print("Все файлы созданы.")


def merge_pdfs_in_directory(directory, output_path):
    merger = PdfMerger()

    # Получаем список файлов PDF в директории
    file_list = [file for file in os.listdir(directory) if file.endswith('.pdf')]

    # Сортируем список файлов по алфавиту
    file_list.sort()

    # Объединяем файлы
    for file_name in file_list:
        file_path = os.path.join(directory, file_name)
        merger.append(file_path)

    # Сохраняем объединенный файл PDF
    merger.write(output_path)
    merger.close()


# Пример использования функции
output_file = 'merged.pdf'

merge_pdfs_in_directory(directory, output_file)

input()
