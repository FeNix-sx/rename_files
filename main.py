import os
import re
import csv
import time


def read_molels_names()->dict:
    """
    Читает модели телефона возвращает словарь с ними:
    ключ - название (вместо "/" пробел)
    значение - код из 6 цифр
    :return: dict
    """
    try:
        name_code_dict = dict()
        with open("models.csv", encoding='utf-8') as r_file:
            # Создаем объект reader, указываем символ-разделитель ";"
            file_reader = csv.reader(r_file, delimiter=";")
            print("Файл с моделями загружен")
            # Счетчик для подсчета количества строк и вывода заголовков столбцов
            count = 0
            # Считывание данных из CSV файла
            for row in file_reader:
                if count > 0:
                    # запись в словарь имен из файла с моделями
                    name_code_dict[row[1].replace("/"," ")] = row[0]

                count += 1

            print(f'Найдено моделей телефонов: {count}.')

            return name_code_dict

    except Exception as ex:
        print(ex)
        print("Не удалось загрузить список смартфоном. Возможно отсутствует файл 'models.csv'")


def read_name_folder(name_code: dict) -> bool:
    try:
        folders = [folder for folder in os.listdir('.') if os.path.isdir(folder) and folder not in ('.git', '.idea','venv')]

        for name in folders:
            if name_code.get(name,False):
                print(f"{name}: код - {name_code[name]}")
            else:
                raise Exception(f"\nОшибка! На найден код для модели '{name}'")

        for folder in folders:
            print(f"Выполняю замену имен файлов в папке {folder} -> ", end=" ")
            if not rename_files(folder, name_code[folder]):
                return

        print("Программа успешно завершена")

    except Exception as ex:
        print(ex)


def rename_files(folder: str, code: str) -> bool:
    try:
        # Получаем список файлов из папки folder с расширением jpg
        files = [f for f in os.listdir(folder) if f.endswith('.jpg')]
        regex = r"\d+"
        for file in files:
            if "-d012#" in file:
                raise Exception(f"\n### Ошибка! Файл с нужным именем уже существует в папке {folder}: {file}")
            else:
                res = re.findall(regex, file)

                part = "" if len(res) == 1 or res[1] == "1" else f"_{res[1]}"

                new_name = f"{code}-d012#{str(res[0]).rjust(3,'0')}{part}.jpg"
                file_path = os.path.join(folder, file)

                try:
                    os.rename(file_path, os.path.join(folder, new_name))
                except Exception as ex:
                    print(ex)
                    return False

        print("Выполнено")
        return True

    except Exception as ex:
        print(ex)
        return False


def main():
    names_dict = read_molels_names()
    read_name_folder(names_dict)


if __name__ == '__main__':
    main()
    time.sleep(4)
