# -*- coding: utf-8 -*-
import sys

sys.path.append('../')
from PIL import Image as Img
import os, threading, platform


class Compress():
    file_list = []
    rlock = threading.RLock()

    def __init__(self, file_dir, th_num=10):
        self.file_dir = file_dir
        self.new_dir = file_dir+"/compress"
        self.th_num = th_num

    sysstr = platform.system()
    if sysstr == "Windows":
        p = "\\"
    else:
        p = "/"

    def get_file_name(self):
        for files in os.walk(self.file_dir):
            for name in files[2]:
                file = files[0] + self.p + name
                self.file_list.append(file)

    def pl_compress_new(self, file_path):
        path = file_path.split(self.p)
        name = path[-1]
        image = Img.open(file_path)
        if image.size[0] > 5000:
            width = image.size[0] * 0.15
            height = image.size[1] * 0.15
        elif image.size[0] > 4000:
            width = image.size[0] * 0.2
            height = image.size[1] * 0.2
        elif image.size[0] > 3000:
            width = image.size[0] * 0.25
            height = image.size[1] * 0.25
        elif image.size[0] > 2000:
            width = image.size[0] * 0.4
            height = image.size[1] * 0.4
        elif image.size[0] > 1000:
            width = image.size[0] * 0.7
            height = image.size[1] * 0.7
        else:
            width = image.size[0]  # 获取宽度
            height = image.size[1]  # 获取高度
        new_name = self.new_dir + self.p + "/".join(path[-2:-1]) + self.p
        is_ex = os.path.exists(new_name)
        if not is_ex:
            os.makedirs(new_name)
        image.thumbnail((width, height))
        image.save(new_name + name, quality=85)
        print("压缩完成：" + file_path)

    def do_work(self):
        while True:
            Compress.rlock.acquire()
            if len(Compress.file_list) == 0:
                Compress.rlock.release()
                break
            else:
                file_path = Compress.file_list.pop()
                Compress.rlock.release()
                try:
                    self.pl_compress_new(file_path)
                except Exception as e:
                    pass

    def run(self):
        for i in range(self.th_num):
            download_t = threading.Thread(target=self.do_work)
            download_t.start()


if __name__ == "__main__":
    print("输入源图片所在路径")
    dir_name = input("")
    compress = Compress(dir_name, 10)
    compress.get_file_name()
    compress.run()
