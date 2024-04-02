import os
from typing import List


def files_in(folder_or_glob: str) -> List[str]:
    return [os.path.join(folder_or_glob, filename) for filename in os.listdir(folder_or_glob)]


def ensure_path_exists(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def output_filename_for(input_path: str, destination: str, volume: float) -> str:
    filename = os.path.basename(input_path)
    return os.path.join(destination, add_volume_suffix_to_filename(filename, volume))


def add_volume_suffix_to_filename(filename: str, volume: float) -> str:
    base_name, extension = os.path.splitext(filename)
    float_suffix = f"_x{str(volume).replace('.', '_')}"
    return base_name + float_suffix + extension

def find_missing_input(inputs: List[str]):
    return list(filter(lambda x: not os.path.exists(x), inputs))