import os
import sys
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
    path = "/media/yijian/data/VShare/git/emark"
    for filename in iter(list_all_files(path)):
        print(filename)


if __name__ == "__main__":
    main()