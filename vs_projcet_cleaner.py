import os
import shutil


def vs_clean_files(dir_path):
    for root, dirs, files in os.walk(dir_path):
        for dir in dirs:
            if dir=="Debug" or dir=="Release":
                shutil.rmtree(os.path.join(root,dir))


if __name__ == '__main__':
    vs_clean_files(r"G:\my\code\C++")