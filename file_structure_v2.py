import os
root_path = os.getcwd() #获取当前根目录的路径
offset = len(root_path.split("\\")) #确定计算缩进级别的所用的基准量
print(root_path)

#使用字典记录每个文件和文件夹的名称和缩进等级
#这里有个Bug：不同文件夹下的同名文件在字典中
#的键值对会被多次覆盖，导致只显示最后一次出现
#该文件或文件夹时的缩进等级
structure = {}

#自根目录遍历所有文件夹及其子文件夹以及其中包含的文件
for root,dirs,files in os.walk(root_path):
    #root为各文件夹的绝对路径
    #dirs为各文件夹下的子文件夹
    #files为各文件夹下的文件名
    current_dir = root.split("\\")
    level = len(current_dir)-offset
    structure[current_dir[-1]] = level
    for f in files:
    	structure[f] = level+1
   
#print(filename)
#print(indent_level)

#按缩进等级输出文件结构
for k,v in structure.items():
	print("\t"*v,k)


