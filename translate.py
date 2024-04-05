import os
import sys
from googletrans import Translator

SRC_LANG = 'zh-cn'
DEST_LANG = 'en'


def read_file(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        return f.readlines()


def write_file(output_file, lines):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines("\r\n".join(lines))


def build_output_filepath(input_file):
    root, ext = os.path.splitext(input_file)
    return f"{root}_{DEST_LANG}{ext}"


def try_translate(content):
    translator = Translator(
        service_urls=['translate.google.com',
                      'translate.google.co.kr'],
    )
    res = []
    for idx, line in enumerate(content):
        if line in ['\n', '\r\n'] or line.strip() == "":
            res.append(line)
            continue

        try:
            trans = translator.translate(
                line, src=SRC_LANG, dest=DEST_LANG).text
        except Exception as e:
            print(f"Error occurred during translate {idx}: {e}")
            res.append(line)
        else:
            res.append(trans)
    return res


if __name__ == "__main__":
    n_param = len(sys.argv)
    if n_param < 2 or n_param > 4:
        print(
            f"Usage: python {sys.argv[0]} <file_path> [<src_lang>] [<dest_lang>]")
        sys.exit(1)

    input_file_path = sys.argv[1]
    if n_param >= 3:
        SRC_LANG = sys.argv[2]
    if n_param >= 4:
        SRC_LANG = sys.argv[3]
    output_file_path = build_output_filepath(input_file_path)

    content = read_file(input_file_path)
    translated_content = try_translate(content)
    if isinstance(translated_content, list)\
            and len(translated_content) == len(content):
        write_file(output_file_path, translated_content)
        print(
            f"Translation completed. The result has been saved to: {output_file_path}")
