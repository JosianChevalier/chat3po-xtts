import subprocess


def set_volume(file: str, volume: float):

    ffmpeg_command = [
        'ffmpeg',
        f'-i {file}',
        f'-af "volume={volume}"', # set file volume to given level
        '-y',  # overwrite if exists
        f'{file}.loud.wav'
    ]

    result = subprocess.run(' '.join(ffmpeg_command), shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        print('Changing volume failed with an error:')
        print(result.stderr)
