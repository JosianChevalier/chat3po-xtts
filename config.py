import argparse
import os
from dataclasses import dataclass
from typing import List


@dataclass
class Chat3POSpeechConfig:
    input: List[str]
    xtts_config_path: str
    xtts_vocab_file: str
    xtts_model: str
    speaker_file_path: str
    speaker_reference: List[str]
    output_folder: str
    use_cuda: bool


def parse_args() -> Chat3POSpeechConfig:
    parser = argparse.ArgumentParser(description="Configure TTS model")
    parser.add_argument(
        "--xtts-config-path",
        type=str,
        default="./model/config.json",
        help="Path to xtts config file"
    )
    parser.add_argument(
        "--xtts-vocab-file",
        type=str,
        default="./model/vocab.json",
        help="Path to xtts vocab file"
    )
    parser.add_argument(
        "--xtts-model",
        type=str,
        default="./model/model.pth",
        help="Path to xtts model"
    )
    parser.add_argument(
        "--speaker-reference",
        type=str,
        default='./reference',
        help="Path to speaker reference folder or file "
    )
    parser.add_argument(
        "--output-folder",
        type=str,
        default="./output",
        help="Output folder"
    ),
    parser.add_argument(
        "--cuda",
        type=bool,
        default=False,
        help="Wether to use CUDA (should be true if the GPU is NVIDIA)"
    )
    parser.add_argument(
        "input",
        default=['chat3po_lines.txt'],
        type=str,
        nargs = "+",
        help="Sentences to generate, or files containing them."
    )

    args = parser.parse_args()

    speaker_reference_files = speaker_reference_files_int(args.speaker_reference)

    # Return the configuration dictionary
    return Chat3POSpeechConfig(
        input=args.input,
        xtts_config_path=args.xtts_config_path,
        xtts_vocab_file=args.xtts_vocab_file,
        xtts_model=args.xtts_model,
        speaker_file_path="recipes/ljspeech/xtts_v1/run/training/GPT_XTTS_LJSpeech_FT/speakers_xtts.pth",
        speaker_reference=speaker_reference_files,
        output_folder=args.output_folder,
        use_cuda=args.cuda,
    )


def speaker_reference_files_int(folder):
    # Calculate speaker reference files from the input folder
    speaker_reference_files = []
    if os.path.exists(folder) and os.path.isdir(folder):
        speaker_reference_files = [
            os.path.join(folder, f) for f in os.listdir(folder)
            if os.path.isfile(os.path.join(folder, f))
        ]

    return speaker_reference_files


config: Chat3POSpeechConfig = parse_args()
