import os
from typing import List

from speech_generator import load_model
from output_formatting import filename_for
from config import config

def ensure_output_path_exists():
    if not os.path.exists(config.output_folder):
        os.makedirs(config.output_folder)

def speeches_to_generate_from(input: List[str]):
    sentences_to_generate = []
    for sentence_or_file in input:
        if os.path.isfile(sentence_or_file):
            with open(sentence_or_file, "r") as file:
                sentences_to_generate.extend([line.strip() for line in file.readlines()])
        else:
            sentences_to_generate.append(sentence_or_file)

    return sentences_to_generate


def generate_speech():
    ensure_output_path_exists()

    speeches_to_generate = speeches_to_generate_from(config.input)
    speech_generator = load_model(config)

    for speech in speeches_to_generate:
        print(f'Generating speech for "{speech}"')

        for iteration in range(10):
            output_file_path = f'{config.output_folder}/{filename_for(speech, iteration)}'
            speech_generator.generate(speech, output_file_path, temperature=0.8, speed=1)


if __name__ == "__main__":
    generate_speech()
