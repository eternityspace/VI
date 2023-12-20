"""Home Work Module VI"""

import re
import shutil
import sys
from pathlib import Path
from pprint import pprint

FILE_TYPES_AND_EXTENSIONS = {
    'archives': ['ZIP', 'GZ', 'TAR', 'RAR'],
    'audio': ['MP3', 'OGG', 'WAV', 'AMR'],
    'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', "XLS", 'PPTX', 'FB2', 'EPUB', 'DJVU'],
    'images': ['JPEG', 'PNG', 'JPG', 'SVG', 'HEIC', 'GIF'],
    'video': ['AVI', 'MP4', 'MOV', 'MKV', 'WEBM'],
}

types_and_extensions_folder_result = {}


def normalize(name: str):
    '''normalize'''

    normalized_name = name
    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                   "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

    TRANS = {}

    for a, b in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(a)] = b
        TRANS[ord(a.upper())] = b.upper()

    normalized_name = normalized_name.translate(TRANS)

    normalized_name = re.sub(r'\W', '_', normalized_name)

    return ''.join(normalized_name)


def print_to_terminal(result):

    for key, value in result.items():
        print(f'{key}: ')
        for item in sorted(value.items(), key=lambda kv: kv[1], reverse=True):
            print(' ' * 10, item)
    # pprint(result, width=1)


def sorting_files(root_path, path):
    '''sorting files and folder'''

    if path.exists():
        for item in path.iterdir():

            try:
                if item.name in FILE_TYPES_AND_EXTENSIONS:
                    continue

                if item.is_file():

                    file_name = normalize(item.stem)
                    file_extension = item.suffix
                    file_type = type_checker(file_extension[1:].upper())

                    new_dir_path = root_path / file_type
                    new_file_path = new_dir_path / (file_name + file_extension)

                    if file_type == 'archives':

                        try:

                            shutil.unpack_archive(str(item.resolve()), str(new_dir_path / file_name))
                            item.unlink()

                        except shutil.ReadError:
                            item.unlink()

                        except WindowsError:
                            item.unlink()

                    elif file_type != 'others':

                        if not new_dir_path.exists():
                            new_dir_path.mkdir()

                        item.replace(new_file_path)

                    else:

                        if not new_dir_path.exists():
                            new_dir_path.mkdir()

                        new_dir_path = root_path / ('others')
                        new_file_path = new_dir_path / (file_name + file_extension)

                        item.replace(new_file_path)

                if item.is_dir():
                    sorting_files(root_path, item)

                try:

                    item.rmdir()

                except:
                    pass

            except Exception as e:
                print(f'{e}!')

    else:
        print(f'The path that you tried to reach does not exist... {path}')


def type_checker(extension: str):
    '''checking type of file'''

    for file_type, list_of_extensions in FILE_TYPES_AND_EXTENSIONS.items():

        if extension in list_of_extensions:

            if file_type in types_and_extensions_folder_result:

                if extension in types_and_extensions_folder_result[file_type]:

                    types_and_extensions_folder_result[file_type][extension] += 1
                    return file_type

                types_and_extensions_folder_result[file_type].update({extension: 1})
                return file_type

            types_and_extensions_folder_result[file_type] = {extension: 1}
            return file_type

    others = 'others'

    if others in types_and_extensions_folder_result:

        if extension in types_and_extensions_folder_result[others]:

            types_and_extensions_folder_result[others][extension] += 1
            return others

        types_and_extensions_folder_result[others].update({extension: 1})
        return others

    types_and_extensions_folder_result[others] = {extension: 1}
    return others


def main():

    try:

        path = Path(sys.argv[1])
        sorting_files(path, path)

    except IndexError:
        print('Directory name is needed!')

    print_to_terminal(types_and_extensions_folder_result)


if __name__ == '__main__':
    main()
