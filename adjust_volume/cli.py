import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Adjust volume of audio files")
    parser.add_argument("inputs",  metavar="file", type=str, nargs="+", help="Path to input file or folder")
    parser.add_argument("-d", "--destination", help="Path to destination folder")
    parser.add_argument("-v", "--volume", type=float, default=1.0, help="Volume adjustment factor")
    return parser.parse_args()
