import os.path
import json
import csv

mask = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
root_structure = {}
input_text = 'my.txt'
output_json = 'out_json_{0}.json'.format(input_text)
output_csv = 'out_csv_{0}.csv'.format(input_text)


def write_json(data, out_file):
    with open(out_file, "w") as write_file:
        json.dump(data, write_file, ensure_ascii=False, indent=4)

def write_csv(data, out_file):
    with open(out_file, 'w', newline="") as write_file:
        writer = csv.writer(write_file)
        writer.writerows(data.items())


def count_words(file_name):
    with open(file_name, 'r') as text:
        for line in text:
            line = line.lower()
            max_index = len(line) - 1
            min_index = 0
            word = ''
            for idx in range(min_index, max_index):
                if line[idx] in mask:
                    word += line[idx]
                else:
                    if word == '':
                        continue
                    if word in root_structure:
                        root_structure[word] += 1
                    else:
                        root_structure[word] = 1
                    word = ''
        write_json(root_structure, output_json)
        write_csv(root_structure, output_csv)

count_words(input_text)