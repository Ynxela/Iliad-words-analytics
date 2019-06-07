import json
import os.path
import random
import time


class ArtificialIntelligenceText:

    def __init__(self, pattern=5, post_pattern=4, file_name='my.txt'):
        self.mask = 'абвгдежзийклмнопрстуфхцчшщъыьэюя ,.-!?\n'
        self.file_name = file_name
        self.just_name = self.file_name.split('.')[0]
        self.data_base = '{0}_db.json'.format(self.just_name)
        self.output_text = '{0}_out.txt'.format(self.just_name)
        self.pattern_len = pattern
        self.post_pattern_len = post_pattern
        self.first_index = 0
        self.data = {}
        self.check_existing_db()
        self.load_data()

    # Проверяет, подходит ли паттерн
    def pattern_is_valid(self, pattern):
        if '\n' in pattern and len(pattern) > 1:
            return False
        for i in pattern:
            if i not in self.mask:
                return False
        return True

    # Функция добавляет паттерн в словарь, на входе - длина паттерна, мин индекс строки, сама строка и словарь-контейнер
    def add_pattern(self, p_len, last_index, line):
        for index in range(self.first_index, last_index - p_len + 2):
            pattern = line[index: index + p_len]
            # Добавляет паттерн в массив
            if pattern not in self.data and '\n' not in pattern and self.pattern_is_valid(pattern):
                self.data[pattern] = {}
            if pattern in self.data:
                max_post_pattern_len = last_index - index - p_len + 1  # Максимальная длина пост-паттерна
                num_of_post_patterns = self.post_pattern_len
                if max_post_pattern_len < self.post_pattern_len:
                    num_of_post_patterns = max_post_pattern_len
                for i in range(1, num_of_post_patterns + 1):  # Находим все пост-паттерны
                    post_pattern = line[index + p_len: index + p_len + i]
                    if self.pattern_is_valid(post_pattern):
                        if post_pattern in self.data[pattern]:
                            self.data[pattern][post_pattern] += 1
                        else:
                            self.data[pattern][post_pattern] = 1

    def load_data(self):
        with open(self.data_base, "r") as source_db:
            self.data = json.loads(source_db.read())

    def safe_data(self, data, file):
        with open(file, "w") as source_db:
            json.dump(data, source_db, ensure_ascii=False, indent=4)

    def get_post_pattern(self, base_pattern, data):
        post_patterns = data[base_pattern]
        next_s = random.choices(list(post_patterns.keys()), list(post_patterns.values()))[0]
        return next_s

    def run(self, flag=1):
        if len(self.data) == 0 or flag == 1:
            self.data = {}
            with open(self.file_name, 'r') as text:  # Количество каждого символа и пары в тексте
                for line in text:  # Для каждой линии в тексте
                    line = line.lower()
                    last_index = len(line) - 1  # Последний индекс в строке
                    for p_len in range(1, self.pattern_len + 1):  # Добавляем паттерны всех длин
                        self.add_pattern(p_len, last_index, line)
            self.safe_data(self.data, self.data_base)

    def write_text(self, count_symbols):
        text = ''
        for i in range(count_symbols):
            post_pattern = None
            for pat in range(self.pattern_len, -1, -1):
                base_pattern = text[-pat:]
                if base_pattern in self.data:
                    post_pattern = self.get_post_pattern(base_pattern, self.data)
                    break
                if pat == 0:
                    post_pattern = random.choice(self.mask)
            text += post_pattern
        with open(self.output_text, 'ta', encoding='utf-8') as out_text:
            out_text.write(
                '{0} | '.format(time.ctime()) + 'длина паттерна - {0} | '.format(
                    self.pattern_len) + 'длина пост-паттерна - {0}'.format(
                    self.post_pattern_len) + '\n' + text + '\n\n\n')

    def check_existing_db(self):
        if not os.path.exists(self.data_base):
            self.safe_data({}, self.data_base)

    def __call__(self):
        self.run()


if __name__ == '__main__':
    ai = ArtificialIntelligenceText(5, 5)
    ai()  # Эквивалентно ai.run()
    ai.write_text(300)
