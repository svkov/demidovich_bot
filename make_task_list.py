import os
import re

from bot import get_data

def get_page_number_from_filename(filename):
    return int(filename.replace('.txt', '').split('-')[1])


def get_numbers_from_page(page, number_page):
    if number_page >= 478:
        return 'Ответы'
    all_numbers = list(filter(lambda x: 100 < x < 4500, map(int, re.findall(r'[0-9]+', page))))
    print(all_numbers)
    if len(all_numbers) == 0:
        return 'Нет номеров'
    end = max(all_numbers)
    return end


def main():
    path = 'res/pages_txt/'
    file_out = 'res/numbers/smth.txt'
    s = 0
    for file in os.listdir(path):
        with open(path + file, 'r') as page, open(file_out, 'a+') as out:
            text = page.read()
            number = get_page_number_from_filename(file)
            end = get_numbers_from_page(text, number)
            if end == 'Нет номеров':
                s += 1
            out.write(str(number) + ' ' + str(end) + '\n')
    print(s)


if __name__ == '__main__':
    # main()
    pass
