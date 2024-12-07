import argparse
import os
from collections import Counter


def read_file(file_name):

    with open(file_name, 'r', encoding='utf-8') as file:
        return file.read()


def clean_text(text):
    
    allowed_chars = set("йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ0123456789-")
    words = text.split()
    clean_words = ["".join(char for char in word if char in allowed_chars) for word in words]
    return [word for word in clean_words if word]


def count_words(text_list):

    return dict(Counter(text_list))


def save_word_counts(file_name, word_counts):

    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    with open(file_name, 'w', encoding='utf-8') as file:
        for word, count in sorted_words:
            file.write(f"{word}: {count}\n")


def calculate_statistics(text, word_counts):
    
    punctuation = ['.', ',', ';', '?', '!', '"', '...']
    stats = {punct: text.count(punct) for punct in punctuation}

    # Длина слова
    for length in range(1, 21):
        stats[length] = sum(count for word, count in word_counts.items() if len(word) == length)

    stats['unique_words'] = len(word_counts)
    return stats


def save_statistics(file_name, stats):
    
    with open(file_name, 'w', encoding='utf-8') as file:
        for key, value in stats.items():
            file.write(f"{key}: {value}\n")


def main():
    parser = argparse.ArgumentParser(description="Text statistics generator")
    parser.add_argument('input_file', help="Path to the input text file")
    args = parser.parse_args()

    input_file = args.input_file
    output_dir = "result"
    os.makedirs(output_dir, exist_ok=True)

    text = read_file(input_file).lower()
    words = clean_text(text)

    word_counts = count_words(words)
    words_output_file = os.path.join(output_dir, os.path.basename(input_file).replace('.txt', '_words.txt'))
    save_word_counts(words_output_file, word_counts)

    stats = calculate_statistics(text, word_counts)
    stats_output_file = os.path.join(output_dir, os.path.basename(input_file).replace('.txt', '_stat.txt'))
    save_statistics(stats_output_file, stats)


if __name__ == "__main__":
    main()
