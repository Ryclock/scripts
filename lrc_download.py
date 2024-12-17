import requests
from config_loader import read_config_byconfigparser
import os

filename = os.path.basename(__file__)
base_url = read_config_byconfigparser(filename, 'lrc_server')
music_directory = read_config_byconfigparser(filename,'music_directory')
lrc_directory = read_config_byconfigparser(filename, 'lrc_directory')

def get_best_lyric(title:str, parent:str, filename:str):
    path = os.path.join(parent, filename)
    if not os.path.exists(path):
        raise Exception(f"filepath[{path}] not exists")

    url = '/lyrics'
    params = {
        'title': title,
        'path': path
    }
    response = requests.get(base_url+url, params=params)
    if not response:
        raise Exception(f"response is None")
    if response.status_code != 200:
        raise Exception(f"response status code is {response.status_code}")

    return response.text

def write_lyric_tofile(data:str, parent:str, filename:str):
    if not os.path.exists(parent):
        os.makedirs(parent)
    path = os.path.join(parent, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(data)


if __name__ == '__main__':
    import os
    for filename in os.listdir(music_directory):
        if not os.path.isfile(os.path.join(music_directory, filename)):
            continue

        file_basename, file_extension = os.path.splitext(filename)
        if file_extension not in ['.flac', '.mp3']:
            print(f"unsupported file[{file_basename}] type[{file_extension}]")
            continue

        print(f"start operate file[{file_basename}]")
        try:
            title = file_basename.split("-")[0]
            best_lyric = get_best_lyric(title, music_directory,filename)
            write_lyric_tofile(best_lyric, lrc_directory, file_basename+".lrc")
        except Exception as e:
            print(f"error in operate file[{file_basename}]: {e}")
