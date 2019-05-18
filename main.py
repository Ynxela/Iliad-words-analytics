import random
import json
import os.path
import time

mask = 'абвгдежзийклмнопрстуфхцчшщъыьэюя ,.-!?\n'
file_name = 'my.txt'
just_name = file_name.split('.')[0]
data_base = '{0}_db.json'.format(just_name)
output_text = '{0}_out.txt'.format(just_name)
pattern_len = 5
post_pattern_len = 5
first_index = 0


# Проверяет, подходит ли паттерн
def pattern_is_valid(pattern):
    if '\n' in pattern and len(pattern) > 1:
        return False
    for i in pattern:
        if i not in mask:
            return False
    return True


# Функция добавляет паттерн в словарь, на входе - длина паттерна, мин индекс строки, сама строка и словарь-контейнер
def add_pattern(p_len, last_index, line, root):
    for index in range(first_index, last_index - p_len + 2):
        pattern = line[index: index + p_len]
        if pattern not in root and '\n' not in pattern and pattern_is_valid(pattern):  # Добавляет паттерн в массив
            root[pattern] = {}
            root[pattern] = {}
        if pattern in root:
            max_post_pattern_len = last_index - index - p_len + 1  # Максимальная длина пост-паттерна
            num_of_post_patterns = post_pattern_len
            if max_post_pattern_len < post_pattern_len:
                num_of_post_patterns = max_post_pattern_len
            for i in range(1, num_of_post_patterns + 1):  # Находим все пост-паттерны
                post_pattern = line[index + p_len: index + p_len + i]
                if pattern_is_valid(post_pattern):
                    if post_pattern in root[pattern]:
                        root[pattern][post_pattern] += 1
                    else:
                        root[pattern][post_pattern] = 1


def safe_data(data, file):
    with open(file, "w") as write_file:
        json.dump(data, write_file, ensure_ascii=False, indent=4)


def get_post_pattern(base_pattern, data):
    post_patterns = data[base_pattern]
    next_s = random.choices(list(post_patterns.keys()), list(post_patterns.values()))[0]
    return next_s


def fill_db(flag):
    with open(data_base, "r") as write_file:
        root_structure = json.loads(write_file.read())
        if len(root_structure) == 0 or flag == 1:
            root_structure = {}
            with open(file_name, 'r') as text:  # Количество каждого символа и пары в тексте
                for line in text:  # Для каждой линии в тексте
                    line = line.lower()
                    last_index = len(line) - 1  # Последний индекс в строке
                    for p_len in range(1, pattern_len + 1):  # Добавляем паттерны всех длин
                        add_pattern(p_len, last_index, line, root_structure)
            safe_data(root_structure, data_base)


def write_text(count_symbols):
    text = ''
    with open(data_base, "r") as write_file:
        root_structure = json.loads(write_file.read())
    for i in range(count_symbols):
        post_pattern = None
        for pat in range(pattern_len, -1, -1):
            base_pattern = text[-pat:]
            if base_pattern in root_structure:
                post_pattern = get_post_pattern(base_pattern, root_structure)
                break
            if pat == 0:
                post_pattern = random.choice(mask)
        text += post_pattern
    with open(output_text, 'ta', encoding='utf-8') as out_text:
        out_text.write(
            '{0} | '.format(time.ctime()) + 'длина паттерна - {0} | '.format(
                pattern_len) + 'длина пост-паттерна - {0}'.format(post_pattern_len) + '\n' + text + '\n\n')


def check_existing_db():
    if not os.path.exists(data_base):
        f = open(data_base, 'tw', encoding='utf-8')
        f.close()
        safe_data({}, data_base)


check_existing_db()
fill_db(1)
write_text(300)
