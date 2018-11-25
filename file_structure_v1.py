import os
root_path = os.getcwd() #获取当前文件夹路径
print("Root path: ",root_path)
print("Parent: ",os.path.dirname(root_path)) #获取当前文件夹都上级文件夹路径
offset = len(root_path.split("\\"))
print("Offset: ",offset)

#自根目录遍历所有文件夹及其子文件夹以及其中包含的文件
for root,dirs,files in os.walk(root_path):
    print("-"*30)
    print("Current : ",root)  #当前文件夹
    print("SubDirs : ",dirs,"\n") #当前文件夹包含的子文件夹
    parent_dir = root.split("\\")

    for file in files:
        abspath = os.path.join(root,file)
        print("Filename: ",os.path.splitext(file)[0]) #当前文件名
        print("Type    : ",os.path.splitext(file)[1]) #当前文件类型
        print("Abspath : ",abspath)                   #当前文件绝对路径
        print("Size    : ",os.path.getsize(abspath),"\n") #文件大小


