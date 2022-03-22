import os
import shutil

if __name__ == '__main__':
    if not os.path.isdir('.\\ida_files'):
        os.mkdir('.\\ida_files')
    for root, dirs, files in os.walk('.\\firmware'):
        for f in files:
            if f.split('.')[-1] == 'ida':
                shutil.copy(root + "\\" + f, '.\\ida_files\\' + f)
