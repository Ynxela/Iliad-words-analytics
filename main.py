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


# Проверяет, подходит ли паттерн. Критерий - символы в паттерне должны быть строго из множества mask
def pattern_is_valid(pattern):
    if len(pattern) > 1 and '\n' in pattern:
        return False
    for i in pattern:
        if i not in mask:
            return False
    return True


# Функция добавляет паттерн в словарь, на входе - длина паттерна, мин индекс строки, сама строка и словарь-контейнер
def add_pattern(p_len, last_index, line, root):
    for index in range(first_index, last_index - p_len + 2):
        pattern = line[index: index + p_len]
        # Добавляет паттерн в массив, если его там нет, проверяя, соответствует ли критериям
        if pattern not in root and '\n' not in pattern and pattern_is_valid(pattern):
            root[pattern] = {}


# Функция заполняет словарь символами, идущими следом за паттерном
def add_pattern_post_patterns(pattern, value, line, last_index):
    p_len = len(pattern)
    for index in range(first_index, last_index - p_len + 2):
        if line[index:index + p_len] == pattern:  # Соответствует ли срез паттерну? Если нет - пропускаем.
            # Находим максимальную длину пост-паттерна
            max_post_pattern_len = last_index - index - p_len + 1
            num_of_post_patterns = post_pattern_len
            if max_post_pattern_len < post_pattern_len:
                num_of_post_patterns = max_post_pattern_len
            # Находим все пост-паттерны
            for i in range(1, num_of_post_patterns + 1):
                post_pattern = line[index + p_len: index + p_len + i]
                if pattern_is_valid(post_pattern):
                    if post_pattern in value['post_pattern']:
                        value['post_pattern'][post_pattern] += 1
                    else:
                        value['post_pattern'][post_pattern] = 1


def safe_data(data, file):
    with open(file, "w") as write_file:
        json.dump(data, write_file, ensure_ascii=False, indent=4)


def get_post_pattern(base_pattern, data):
    post_patterns = data[base_pattern]['post_pattern']
    next_s = random.choices(list(post_patterns.keys()), list(post_patterns.values()))[0]
    return next_s


def write_text(count_symbols):
    with open(data_base, "r") as write_file:
        root_structure = json.loads(write_file.read())
    text = ''
    base_pattern = random.choice(mask)
    for i in range(count_symbols):
        if len(text) > 6:
            base_pattern = text[-5:]
        try:
            letter = get_post_pattern(base_pattern, root_structure)
        except:
            try:
                base_pattern = text[-4:]
                letter = get_post_pattern(base_pattern, root_structure)
            except:
                try:
                    base_pattern = text[-3:]
                    letter = get_post_pattern(base_pattern, root_structure)
                except:
                    try:
                        base_pattern = text[-2:]
                        letter = get_post_pattern(base_pattern, root_structure)
                    except:
                        try:
                            base_pattern = text[-1:]
                            letter = get_post_pattern(base_pattern, root_structure)
                        except:
                            base_pattern = random.choice(mask)
                            letter = get_post_pattern(base_pattern, root_structure)
        text += letter
        base_pattern = letter

    with open(output_text, 'ta', encoding='utf-8') as out_text:
        out_text.write(
            '{0} | '.format(time.ctime()) + 'длина паттерна - {0} | '.format(
                pattern_len) + 'длина пост-паттерна - {0}'.format(post_pattern_len) + '\n' + text + '\n\n')


def fill_db(flag):
    with open(data_base, "r") as write_file:
        root_structure = json.loads(write_file.read())
        if len(root_structure) == 0 or flag == 1:
            root_structure = {}

            # Количество каждого символа и пары в тексте
            with open(file_name, 'r') as text:
                for line in text:  # Для каждой линии в тексте
                    line = line.lower()
                    last_index = len(line) - 1  # Последний индекс в строке
                    # Добавляем паттерны всех длин
                    for p_len in range(1, pattern_len + 1):
                        add_pattern(p_len, last_index, line, root_structure)

            # Количество встреч каждого символа после искомого символа (key):
            for key, value in root_structure.items():
                value['post_pattern'] = {}  # Добавили символ для анализа
                # Здесь начинаем прогонять символы и забивать данные в словарь, который создан под данную букву
                with open(file_name, 'r') as text:
                    for line in text:
                        line = line.lower()
                        last_index = len(line) - 1
                        if key in line:
                            add_pattern_post_patterns(key, value, line, last_index)

            # # Если пара или тройка ни разу не встретилась в тексте, то удалить
            # keys_to_delete = []
            # for key, value in root_structure.items():
            #     if len(value['post_pattern']) == 0:
            #         keys_to_delete.append(key)
            # for key in keys_to_delete:
            #     del root_structure[key]

            # del root_structure[' ']['post_pattern'][' ']
            # for i in range(2, pattern_len + 1):
            #     keys_to_delete = '{}'.format(' ' * i)
            #     del root_structure[keys_to_delete]

            safe_data(root_structure, data_base)


def check_existing_db():
    if not os.path.exists(data_base):
        f = open(data_base, 'tw', encoding='utf-8')
        f.close()
        safe_data({}, data_base)


check_existing_db()
fill_db(1)
write_text(300)
