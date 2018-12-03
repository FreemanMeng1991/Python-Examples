import os
root_path = os.getcwd()
offset = len(root_path.split("\\"))

for root,dirs,files in os.walk(root_path):
	current_dir = root.split("\\")
	indent = len(current_dir)-offset
	print("\t"*indent,current_dir[-1]
	      
**************************************************	      
from chardet import detect
count,blanks = 0,0
with open("a.txt",'rb') as fp:
	encode = detect(fp.read())['encoding']
	print(encode)
	fp.close()

with open("a.txt",'r',encoding=encode) as fp:
	while True:
		line = fp.readline()
		if not line: #判断文件是否结束
			break
		count+=1
		if not (len(line.strip())):
			blanks+=1
		
print(count,blanks)	      
