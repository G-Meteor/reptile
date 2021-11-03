# encoding: utf-8
# Author: Huaping Qi
import face_recognition
import glob
import os
import sys
from queue import Queue
import threading
import time

THREAD_NUM = 10


def remove_file(f):
    try:
        os.remove(f)
        print(f'remove {f}')
    except:
        print(f'remove {f} failed')


def face_search_and_remove(ref_path, targe_dir=None):
    #print(44444444444444)
    print(ref_path)

    try:
        ref_pic = face_recognition.load_image_file(ref_path)
        #print(222222222222222222)
        #print(ref_pic)
        ref_pic_encoding = face_recognition.face_encodings(ref_pic)[0]
        print(3333333333333333333)
    except:
        print(f"################ {ref_path}")
        return

    patten = os.path.join(os.path.dirname(ref_path), "*.jpg")
    if targe_dir:
        patten = os.path.join(targe_dir, '*.jpg')
        print(targe_dir)

    for f in glob.glob(patten):
        if os.path.basename(ref_path) in f:
            continue
        try:
            unknown_picture = face_recognition.load_image_file(f)
            unknown_face_encodings = face_recognition.face_encodings(unknown_picture)

            if not unknown_face_encodings:
                remove_file(f)
                continue
            need_remove = True
            for unknown_face_encoding in unknown_face_encodings:
                results = face_recognition.compare_faces([ref_pic_encoding], unknown_face_encoding, tolerance=0.52)
                print(results)
                if True in results:
                    print(results, f)
                    need_remove = False
                    break
            if need_remove:
                remove_file(f)
        except:
            print(f'exception on picture {f}')
            remove_file(f)


def consumer(qu):
    while not qu.empty():

        name, pic = qu.get(False)
        print(name+" \n"+pic)

        try:
           # print(1111111111111111111)
            time.sleep(50)
            abspath=os.path.abspath("..\\1.baidu\\"+ os.path.join(name, pic))
            #print(abspath)
            #print(os.path.isabs(abspath))
            face_search_and_remove(abspath)

            #print(2222222222222222222 )
        except:
            print(f'failed to handle {os.path.join(name, pic)}')

def compare_in_same_dir():
    # 从文件见选择一个图片作为从参考图，如果人脸不同则删除
    # face_search_and_remove(sys.argv[1])
    name_file = 'name-ref2.txt'
    if len(sys.argv) == 2:
        name_file = sys.argv[1]
    with open(name_file, encoding='utf-8') as f:
        lines = f.readlines()
        q = Queue()
        for line in lines:
            if not line:
                continue
            if line.startswith("#"):
                continue
            name = ' '.join(line.split()[:-1]) if len(line.split()[:-1]) >= 1 else line.split()[0]
            pic = line.split()[-1]
            # 队列
            q.put((name, pic), False)

        tasks = []
        for i in range(THREAD_NUM):
            t = threading.Thread(target=consumer, args=(q,))
            t.setDaemon(True)
            t.start()
            tasks.append(t)

        for t in tasks:
            t.join()
        print('当前搜索结束，感谢使用')

        # try:
        #     face_search_and_remove(os.path.join(name, pic))
        # except:
        #     print(f'failed to handle {os.path.join(name, pic)}')


def compare_in_diff_dir(name):
    """参考图来自不同的文件夹"""
    refs = os.listdir(name)
    # refs = refs[::-1]
    # print(refs)
    targets = os.listdir('.')
    # print(targets)
    for ref in refs:
        jpgs = glob.glob(os.path.join(name, ref) + os.sep + "*.jpg")
        if jpgs:
            ref_pic = jpgs[0]
        # print(ref)
        for target in targets:
            if ref not in target:
                continue
            face_search_and_remove(ref_pic, targe_dir=target)


if __name__ == '__main__':
    # compare_in_diff_dir(sys.argv[1])
    compare_in_same_dir()
