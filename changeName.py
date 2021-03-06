import os
import sys
import sqlite3
import re
import string

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

def split_word(camel:str):
    _words = []
    first = 0
    for i in range(len(camel) - 1):
        if camel[i].isupper() and camel[i+1].islower():
            if i == 0:
                pass
            else:
                _words.append(camel[first: i])
                first = i
    _words.append(camel[first:])
    return _words

def cleanInput(content):
    content = content.lower()
    content = re.sub('[\n,.\'"-+!?-]', ' ', content)
    #print(content.split(' '));
    words = [word for word in content.split(' ') if len(word) > 4]
    return words
    #print(words)
    #return [cleanSentence(sentence) for sentence in content]

def createDictionary(keys:list, values:list):
    dict = {}
    if len(keys) <= len(values):
        for i, key in enumerate(keys):
            value = ""
            if re.search('[a-z]', key) == None:
                value = values[i][0:len(key)].upper()
            else:
                value = values[i].capitalize()
            dict[key] = value
    else:
        pass
    return dict

def get_candidate_words():
    with open('words.txt', 'r') as f:
        return cleanInput(f.read())

def adjustLine(filename):
    with open(filename, encoding="utf8", errors='ignore') as file:
        text = str()
        while True:
            line = file.readline()
            #print(line)
            if line == '':
                break
            if (len(line) != 0 and
                #(line[0:2] == '+(' or line[0:2] == '-(')):
                re.search(r'^ *[-+] *\(', line) != None and
                line.find('{') == -1):
                line = re.sub('\n', '', line)
            if (len(line) != 0 and
                line.find('{') != -1):
                line = re.sub('{', '{\n', line)
            text += line
        return text


def fileFunctions(filepath):
    with open(filepath, encoding="utf8", errors='ignore') as file:
        function = []
        templine = ""
        while True:
            line = file.readline()
            #print(line)
            if line == '':
                break
            line = re.sub('\n', ' ', line)
            if (len(line) != 0 and
                #(line[0:2] == '+(' or line[0:2] == '-(')):
                re.search(r'^ *[-+] *\(', line) != None):
                templine = line
            elif (len(templine) != 0):
                templine += line
            templineEnd = templine.find('{') 
            if templineEnd == -1:
                continue
            else:
                templine = templine[0: templineEnd]
                templine = templine.strip()
                templine = re.sub(' +', ' ', templine)
                if templine.find(':') != -1:
                    function.append(templine)
                templine = ""
        return function

def functionName(functionSign):
    stack = []
    lfunc = str()
    isBeginPara = False
    for i in range(len(functionSign) - 1):
        c = functionSign[i]
        if c == '(':
            stack.append(c)
            if i != 0 and functionSign[i-1] == ':':
                isBeginPara = True
        elif c == ')':
            stack.pop()
        else:
            if len(stack) == 0 and isBeginPara == False:
                lfunc += c
                if c == '-' or c == '+':
                    lfunc += ' '
            else:
                pass
            if len(stack) == 0 and c == ' ':
                isBeginPara = False
                lfunc += c
    ll = re.sub(r' +', ' ', lfunc)
    return ll

def outputFunctionsAndDictionary():
    path = "/media/yijian/data/VShare/git/emark/emark"
    functions = set()
    for filename in iter(list_all_files(path)):
        part = os.path.split(filename)
        if (part[0].find("/Assets.xcassets") != -1 or
            part[1].find(".plist") != -1 or
            part[1].find(".strings") != -1 or
            part[1].find("main.m") != -1 or
            part[1].find("AppDelegate.m") != -1 or
            part[1].find("AppDelegate.h") != -1 or
            part[1].find(".pch") != -1 or
            part[1].find("+") != -1 or
            part[1].find(".storyboard") != -1) :
            pass
        else:
            if filename[-1] == 'm':
                #words |= fileFunctionWordSet(filename)
                functions |= set(fileFunctions(filename))
                print(adjustLine(filename))
    with open('functions.out', 'w') as f:
        for funcSign in functions:
            f.write(functionName(funcSign))
            f.write('\n')


def main():
    #print(createDictionary(list(fileNameSet()),get_candidate_words()))
    #for word in enumerate(fileNameSet()):
    #    print(word)
    # print(fileNameSet())
    outputFunctionsAndDictionary()
    


if __name__ == "__main__":
    main()