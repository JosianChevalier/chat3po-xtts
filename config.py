import argparse
import os
from dataclasses import dataclass
from typing import List
from enum import Enum

class Model(Enum):
    CUSTOM_C3PO = "custom-c3po"
    XTTS_V2 = "xtts_v2"


@dataclass
class Chat3POSpeechConfig:
    input: List[str]
    model: Model
    speaker_reference: List[str]
    destination: str
    use_cuda: bool
    variations_count: int
    speed: float
    temperature: float


def parse_args() -> Chat3POSpeechConfig:
    parser = argparse.ArgumentParser(description="Configure TTS model")
    parser.add_argument(
        "--model",
        type=str,
        choices=[member.value for member in Model],
        default=Model.CUSTOM_C3PO,
        help="Choose the TTS model (custom-c3po or xtts_v2)"
    )
    parser.add_argument(
        "--speaker-reference",
        type=str,
        default='./reference',
        help="Path to speaker reference folder or file "
    )
    parser.add_argument(
        "-d", "--destination",
        type=str,
        default="./output",
        help="Destination folder"
    ),
    parser.add_argument(
        "--cuda",
        type=bool,
        default=False,
        help="Wether to use CUDA (should be true if the GPU is NVIDIA)"
    )
    parser.add_argument(
        "-n", "--variations-count",
        type=int,
        default=10,
        help="How many variations to generate for each speech."
    )
    parser.add_argument(
        "-s", "--speed",
        type=float,
        default=1,
        help="The speed of the speech."
    )
    parser.add_argument(
        "-t", "--temperature",
        type=float,
        default=0.7,
        help="Level of variance of the outputs. Lower is more stable."
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
        model=Model(args.model),
        speaker_reference=speaker_reference_files,
        destination=args.destination,
        use_cuda=args.cuda,
        variations_count=args.variations_count,
        speed=args.speed,
        temperature=args.temperature,
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
