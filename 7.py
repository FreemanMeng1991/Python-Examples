import os.path,sys
def mainKeywords(dirPath):
    blank, codelines = 0, 0
    count = 0
    f_list = os.listdir(dirPath)
    print("Directory: ",dirPath)
    print("Files: ",f_list)
    for i in f_list:
        print(os.path.splitext(i))#分离文件名与扩展名
        print(dirPath+"\\"+i)
        """
        with open(dirPath+"\\"+i, 'r') as fp:  #相当于fp=open(...)
            while True:
                line = fp.readline() 
                count+=1
                if not line:
                    break
                if not (len(line.strip())): #先去掉首尾的空白,再判断是否空行，若使用len(line)-1
                    blank+=1                #则可能会受到开头为非打印字符的干扰如制表位、空格
                codelines+=1
            print('the nuber of codelines is : ' + str(codelines))
            print('the nuber of blanklines is : ' + str(blank))
            blank, codelines = 0, 0
"""
file_path = os.getcwd()
print(file_path)
print(os.path.dirname(file_path),"\n")

for root,dirs,files in os.walk(file_path):
    print("Root    : ",root)
    print("DirName : ",os.path.dirname(root).split("\\")[-1])
    print("SubDirs    : ",dirs)
    for file in files:
        abspath = os.path.join(root,file)
        
        #print("Abspath : ",abspath)
        print("Filename: ",os.path.splitext(file)[0])
        print("Type    : ",os.path.splitext(file)[1])
        print("Size    : ",os.path.getsize(abspath),"\n")
#mainKeywords(r'C:\Users\FREEMAN\Desktop\utmp')