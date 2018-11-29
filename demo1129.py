import os
# root_path = os.getcwd()
# offset = len(root_path.split("\\"))
# for root,dirs,files in os.walk(root_path):
# 	current_dir = root
# 	path_list = current_dir.split("\\")
# 	indent_level = len(path_list) - offset 
# 	for f in files:
# 		file_name = os.path.splitext(f)[0]
# 		file_path = os.path.join(root,f)
# 		print(file_path)

file_path = r'C:\Users\Administrator\Desktop\root\dir1\cp3_data_size.c'
# print(file_path)

def line_count(file_path):
	code_line,blank_line = 0,0
	with open(file_path,'r') as fp:
		while True:
			line = fp.readline()
			if not line:
				break
			code_line+=1
	print(code_line,"Lines")

line_count(file_path)
