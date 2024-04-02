import os
from ffmepg import generate_file_with_volume
from files import files_in, ensure_path_exists, output_filename_for, find_missing_input
from cli import parse_args


def adjust_volume_for_file(input_file: str, destination: str, volume: float):
    output = output_filename_for(input_file, destination, volume)
    generate_file_with_volume(input_file, output, volume)

def adjust_volume_for_folder(input_path: str, destination: str, volume: float):
    files = files_in(input_path)

    for input_file in files:
        adjust_volume_for_file(input_file, destination, volume)


def adjust_volume_main(args):
    inputs = args.inputs
    destination = args.destination

    invalid_inputs = find_missing_input(inputs)
    if invalid_inputs:
        invalid_inputs_as_string = "\n".join(invalid_inputs)
        print(f'Cannot find the following inputs:\n{invalid_inputs_as_string}')
        return


    for input in inputs:
        if os.path.isdir(input):
            adjust_volume_for_folder(input, destination, args.volume)
        else:
            adjust_volume_for_file(input, destination, args.volume)


if __name__ == "__main__":
    adjust_volume_main(parse_args())
