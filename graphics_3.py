import csv
from matplotlib import pyplot as plt
import numpy as np

SPAM_FILE = 'output/spam.csv'
HAM_FILE = 'output/ham.csv'
WORD = 'word'
TIMES = 'times'
SPAM = 'spam'
HAM = 'ham'


def main():
    draw_chart(SPAM_FILE, SPAM)
    draw_chart(HAM_FILE, HAM)


def draw_chart(f_name, msg_type):
    with open(f_name) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        words = []
        frequency = []
        for row in csv_reader:
            words.append(row[WORD])
            frequency.append(row[TIMES])
        plt.style.use('seaborn-dark')
        plt.title('Top 20 {} words'.format(msg_type))
        words = words[0:20]
        words.reverse()
        frequency = frequency[:20]
        frequency.reverse()
        x_indexes = np.arange(len(words))
        plt.xticks(x_indexes, words)
        plt.bar(x_indexes, frequency, color='#FF2014', label='Most frequent {} words'.format(msg_type))
        plt.xlabel("Words")
        plt.ylabel("Frequency")
        plt.gca().invert_xaxis()
        plt.show()


if __name__ == '__main__':
    main()
