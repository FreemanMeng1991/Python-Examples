"""
This is the final version.
"""
import os
root_path = os.getcwd() #获取当前根目录的路径
offset = len(root_path.split("\\")) #确定计算缩进级别的所用的基准量
print(root_path)

#修复Bug：使用列表代替字典
filename     = []
indent_level = []

for root,dirs,files in os.walk(root_path):
    current_dir = root.split("\\")
    level = len(current_dir)-offset
    indent_level.append(level)
    filename.append("\\"+current_dir[-1])
    for f in files:
    	indent_level.append(level+1)
    	filename.append(f)

for f,i in zip(filename,indent_level):
	print("\t"*i,f)
	