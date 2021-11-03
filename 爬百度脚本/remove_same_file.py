import hashlib
import glob
import os
from threading import Thread
import threading

def remove_duplicated():
    md5_sums = []
    for f in glob.glob("*/*.jpg"):
        if '***文件夹2' in f:
            continue
        with open(f, 'rb') as fs:
            data = fs.read()
            file_md5= hashlib.md5(data).hexdigest()
            if file_md5 not in md5_sums:
                md5_sums.append(file_md5)
            else:
                os.remove(f)
                print(f)

def rename():
    dirs = os.listdir('.')
    for d in dirs:
        if '文件' in d:

            print(d.split('文件'))
            os.rename(d, d.split('文件')[0])


def generate_names(name):
    
    dirs = os.listdir(name)
    with open(f'name-{name}.txt', 'w', encoding='utf-8') as f:
        for d in dirs:
            f.write(f'{d}院士\n')
        

t1 = Thread(target=generate_names, args=('CAE',))
t1.setDaemon(True)
t1.start()
t2 = Thread(target=generate_names, args=('CAS',))
t2.setDaemon(True)
t2.start()
t1.join()
t2.join()
# generate_names('CAE')
# generate_names('CAS')
