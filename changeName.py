import os
import sys
import sqlite3

def list_all_files(rootdir):
    _files = []
    list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
    for i in range(0,len(list)):
           path = os.path.join(rootdir,list[i])
           if os.path.isdir(path):
              _files.extend(list_all_files(path))
           if os.path.isfile(path):
              _files.append(path)
    return _files


def main():
    path = "/media/yijian/data/VShare/git/emark/emark"
    for filename in iter(list_all_files(path)):
        part = os.path.split(filename)
        if (part[0].find("/Assets.xcassets") != -1 or
            part[1].find(".plist") != -1 or
            part[1].find(".strings") != -1 or
            part[1].find("main.m") != -1 or
            part[1].find("AppDelegate.m") != -1 or
            part[1].find("AppDelegate.m") != -1 or
            part[1].find(".pch") != -1 or
            part[1].find(".storyboard") != -1) :
            pass
        else:
            print(part[1])


if __name__ == "__main__":
    main()