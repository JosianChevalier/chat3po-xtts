import re


def filename_for(sentence: str, iteration: int):
    words = tokenize(sentence)
    filtered_words = filter_out_special_chars(words)
    snake_case_words = first_words_to_snake_case(filtered_words)

    return f'{snake_case_words}-{iteration}.wav'


def tokenize(sentence):
    words = re.findall(r'\w+', sentence.lower())
    return words


def filter_out_special_chars(words):
    filtered_words = [word for word in words if word.isalnum()]
    return filtered_words


def first_words_to_snake_case(filtered_words):
    # Join the first 5 filtered words with dashes
    snake_case_words = '-'.join(filtered_words[:5])
    return snake_case_words
