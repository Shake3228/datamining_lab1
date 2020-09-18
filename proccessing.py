import csv
import re
from collections import Counter
import os
import nltk
import logging
from nltk.corpus import stopwords

nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

SYMBOLS_REGEX = 'amp;|gt;|lt;|[=!,*)@#%(&$_?.^:;/\\\\"\'\\-]'
DIGITS_REGEX = "[0-9]"
MESSAGE_TYPE = "v1"
MESSAGE_KEY = "v2"
SPAM = "spam"
HAM = "ham"
OUTPUT_DIRECTORY = 'output'
FILE = 'resources/sms-spam-corpus.csv'
SPAM_OUTPUT_FILE = 'spam.csv'
HAM_OUTPUT_FILE = 'ham.csv'

porter = PorterStemmer()
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def csv_dict_reader(file_obj):
    return csv.DictReader(file_obj, delimiter=',')


def processor_line(line):
    line = remove_digits(line)
    line = remove_symbols(line)
    line = line.lower()
    line = remove_stop_words(line)
    return str(line)


def remove_digits(line):
    return re.sub(DIGITS_REGEX, '', line)


def remove_symbols(line):
    return re.sub(SYMBOLS_REGEX, '', line)


def remove_stop_words(line):
    return [word for word in word_tokenize(line) if len(word) > 2 and not word in stopwords.words()]


def stemming(line):
    token_words = word_tokenize(line)
    for word in token_words:
        porter.stem(word)


def write_to_file(list, file_name):
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)
    with open(OUTPUT_DIRECTORY + '/' + file_name, 'w', newline='') as file:
        fieldnames = ['word', 'times']
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        for key, value in list:
            csv_writer.writerow({'word': key, 'times': value})


def main():
    with open(FILE) as file:
        reader = csv_dict_reader(file)
        spam_counter = Counter()
        ham_counter = Counter()
        for line in reader:
            tokenized_msg = word_tokenize(processor_line(line[MESSAGE_KEY]))
            if line[MESSAGE_TYPE] == SPAM:
                spam_counter.update(tokenized_msg)
            else:
                ham_counter.update(tokenized_msg)

        write_to_file(spam_counter.most_common(), SPAM_OUTPUT_FILE)
        write_to_file(ham_counter.most_common(), HAM_OUTPUT_FILE)


if __name__ == '__main__':
    main()
