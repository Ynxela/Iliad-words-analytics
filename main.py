import random
import json
import os.path
import time

mask = 'абвгдежзийклмнопрстуфхцчшщъыьэюя ,.-!?'
file_name = 'my.txt'
data_base = '{0}.json'.format(file_name)
output_text = 'experiment_{0}.txt'.format(file_name)
root_structure = {}
pattern_len = 5
next_symbols_len = 1
min_id = 0


# Проверяет, подходит ли паттерн. Критерий - символы в паттерне должны быть строго из множества mask
def check_pattern(pattern):
    for i in pattern:
        if i not in mask:
            return False
    return True


# Функция добавляет паттерн в словарь, на входе - длина паттерна, мин индекс строки, сама строка и словарь-контейнер
def add_pattern(p_len, min_id, line, letters_data):
    max_id = len(str(line)) - 1
    for id in range(min_id, max_id - p_len):
        pattern = line[id:id + p_len]
        # Добавляет паттерн в массив, если его там нет, проверяя, соответствует ли критериям
        if pattern not in letters_data:
            if check_pattern(pattern):
                letters_data[pattern] = {}


def add_pattern_next_letters(pattern, value, line):
    min_id = line.index(pattern)
    p_len = len(pattern)
    max_id = len(str(line)) - p_len
    for id in range(min_id, max_id):
        # Соответствует ли срез паттерну? Если нет - пропускаем.
        if line[id:id + p_len] == pattern:
            # Если паттерн не последний, то символом берем следующий по индексу, если последний, то перенос строки
            if id == max_id:
                next_letter = '\n'
            else:
                next_letter = line[id + p_len]
            if next_letter != '\n' and next_letter not in set(mask):
                continue
            # Если следующего символа нет еще в списке, то добавляем
            if next_letter in value['next_letter']:
                value['next_letter'][next_letter] += 1
            else:
                value['next_letter'][next_letter] = 1
            if id < max_id - p_len:
                next_pattern = line[id + p_len: id + next_symbols_len + p_len + 1]
                if next_pattern == '  ':
                    continue
                if check_pattern(next_pattern):
                    if next_pattern in value['next_letter']:
                        value['next_letter'][next_pattern] += 1
                    else:
                        value['next_letter'][next_pattern] = 1
            if id < max_id - p_len - 1:
                next_pattern = line[id + p_len: id + next_symbols_len + p_len + 2]
                if next_pattern == '   ':
                    continue
                if check_pattern(next_pattern):
                    if next_pattern in value['next_letter']:
                        value['next_letter'][next_pattern] += 1
                    else:
                        value['next_letter'][next_pattern] = 1
            if id < max_id - p_len - 2:
                next_pattern = line[id + p_len: id + next_symbols_len + p_len + 3]
                if next_pattern == '   ':
                    continue
                if check_pattern(next_pattern):
                    if next_pattern in value['next_letter']:
                        value['next_letter'][next_pattern] += 1
                    else:
                        value['next_letter'][next_pattern] = 1


def safe_data(data, file):
    with open(file, "w") as write_file:
        json.dump(data, write_file, ensure_ascii=False, indent=4)


def next_symbol(base_symbol, data):
    next_letters = data['letters_data'][base_symbol]['next_letter']
    next_s = random.choices(list(next_letters.keys()), list(next_letters.values()))[0]
    return next_s


def write_text(count_symbols):
    with open(data_base, "r") as write_file:
        root_structure = json.loads(write_file.read())
    text = ''
    base_symbol = random.choice(mask)
    for i in range(count_symbols):
        if len(text) > 6:
            base_symbol = text[-5:]
        try:
            letter = next_symbol(base_symbol, root_structure)
        except:
            try:
                base_symbol = text[-4:]
                letter = next_symbol(base_symbol, root_structure)
            except:
                try:
                    base_symbol = text[-3:]
                    letter = next_symbol(base_symbol, root_structure)
                except:
                    try:
                        base_symbol = text[-2:]
                        letter = next_symbol(base_symbol, root_structure)
                    except:
                        try:
                            base_symbol = text[-1:]
                            letter = next_symbol(base_symbol, root_structure)
                        except:
                            base_symbol = random.choice(mask)
                            letter = next_symbol(base_symbol, root_structure)
        text += letter
        base_symbol = letter

    with open(output_text, 'ta', encoding='utf-8') as out_text:
        out_text.write('{0}'.format(time.ctime()) + '\n' + text + '\n\n')


if not os.path.exists(data_base):
    f = open(data_base, 'tw', encoding='utf-8')
    f.close()
    safe_data(root_structure, data_base)


def fill_data(min_id, flag):
    with open(data_base, "r") as write_file:
        root_structure = json.loads(write_file.read())
        if 'letters_data' not in root_structure or flag == 1:
            root_structure['letters_data'] = {}

            # Количество каждого символа и пары в тексте
            with open(file_name, 'r') as text:
                for line in text:
                    line = line.lower()
                    # Добавляем паттерны всех длин
                    for i in range(1, pattern_len + 1):
                        add_pattern(i, min_id, line, root_structure['letters_data'])

            # Количество встреч каждого символа после искомого символа (key):
            for key, value in root_structure['letters_data'].items():
                # print(key)
                # Добавили символ для анализа
                value['next_letter'] = {}
                # Здесь начинаем прогонять символы и забивать данные в словарь, который создан под данную букву
                with open(file_name, 'r') as text:
                    for line in text:
                        line = line.lower()
                        # Если символа нет в строке - берем следующую строку
                        if key not in line:
                            continue
                        # Здесь проверяем каждый символ и паттерн
                        add_pattern_next_letters(key, value, line)

            # # Если пара или тройка ни разу не встретилась в тексте, то удалить
            # keys_to_delete = []
            # for key, value in root_structure['letters_data'].items():
            #     if len(value['next_letter']) == 0:
            #         keys_to_delete.append(key)
            # for key in keys_to_delete:
            #     del root_structure['letters_data'][key]

            # del root_structure['letters_data'][' ']['next_letter'][' ']
            # for i in range(2, pattern_len + 1):
            #     keys_to_delete = '{}'.format(' ' * i)
            #     del root_structure['letters_data'][keys_to_delete]

            safe_data(root_structure, data_base)


fill_data(min_id, 1)
write_text(500)
