import subprocess


def generate_file_with_volume(input_file: str, output_file: str, volume: float):
    ffmpeg_command_parts = [
        'ffmpeg',
        '-y',  # overwrite if exists
        f'-i {input_file}', # input file
        f'-af volume={volume}',  # set the given volume
        output_file
    ]
    ffmpeg_command = " ".join(ffmpeg_command_parts)
    result = subprocess.run(ffmpeg_command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        print("Command failed with an error:")
        print(ffmpeg_command)
        print(result.stderr)
