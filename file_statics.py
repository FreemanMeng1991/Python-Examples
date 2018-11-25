"""
将此脚本放置在某一文件夹下并运行，此脚本将以
当前文件夹为根目录，遍历所有文件夹及其子文件夹
以及其中包含的文件，给出各文件的文件名、类型、
行数（包括空行）、大小、文件路径、编码格式、并
统计出文件和文件夹（包含子文件夹）的个数。
"""
import os.path
import sys
import chardet

def get_file_info(file_path):
    blank_lines,total_lines = 0,0
    with open(file_path,'rb') as fp:
        encode = chardet.detect(fp.read())['encoding']
        print("Encoding: ",encode)

    with open(file_path, 'r',encoding=encode) as fp:

        while True:
            line = fp.readline() 
            if not line:
                break
            if not (len(line.strip())): #先去掉首尾的空白,再判断是否空行，若使用len(line)-1
                blank_lines+=1                #则可能会受到开头为非打印字符的干扰如制表位、空格
            total_lines+=1
        print(total_lines,"lines in toals","(",blank_lines,"blank lines)")
        count['lines']+=total_lines
        count['blanks']+=blank_lines
        blank_lines, total_lines = 0, 0

if __name__ == '__main__':

    file_path = os.getcwd()
    print(file_path)
    print(os.path.dirname(file_path),"\n")
    count={'file':0,'folder':-1,'lines':0,'blanks':0} #根目录不统计在内，故为-1

    for root,dirs,files in os.walk(file_path):
       
        #直接将root传递给isfile会使得root字符串中包含的
        #反斜杠被误认为转义字符，如\t \f 因此使用eval和
        #原生字符串的组合来解决这个问题
        if not os.path.isfile(eval("r'"+root+"'")):
             count['folder']+=1

        for file in files:
            abspath = os.path.join(root,file)
            if os.path.isfile(eval("r'"+abspath+"'")):
                 count['file']+=1
            # else:
            #     count['folder']+=1
            print("--"*20)
            print("Filename: ",os.path.splitext(file)[0])
            print("Type    : ",os.path.splitext(file)[1],"file")
            print("Size    : ",os.path.getsize(abspath),"bytes")
            print("Location: ",root)
            get_file_info(abspath)

    print("\n","*"*40)
    print(count['file'],"Files,",count['folder'],"Folders")
    print(count['lines'],"Lines(",count['blanks'],"blank lines)")

