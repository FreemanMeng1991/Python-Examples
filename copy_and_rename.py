# -*- coding: utf-8 -*-
#!/usr/bin/python
#批量将一个目录下的文件复制或移动到另一目录
#复制或移动的过程中，可以对文件进行重命名操作
#src_dir为源目录 dst_dir为目标目录

import os,shutil
from random import randint

root_path = os.getcwd() #获取当前根目录的路径

src_dir = r"E:\Examples_in_Python\Docs"
dst_dir = r"E:\Examples_in_Python\Copytest"
files = os.listdir(src_dir)

def move_file(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        shutil.move(srcfile,dstfile)          #移动文件
        print("Move %s \nTo: %s"%(srcfile,dstfile))

def copy_file(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        shutil.copyfile(srcfile,dstfile)      #复制文件
        print("copy %s -> %s"%( srcfile,dstfile))

with open(r"E:\Examples_in_Python\统计年级段各班级人数和学生信息\计专1701班.txt","r") as fp:
        while(True):
            header = fp.readline().strip().replace("\t","+")
            print(header)
            if(header):
                filename = header+"+第二次.doc"
                index = randint(0,len(files)-1)
                srcfile = os.path.join(src_dir,files[index])
                dstfile = os.path.join(dst_dir,filename)
                copy_file(srcfile,dstfile)
            else:
                break