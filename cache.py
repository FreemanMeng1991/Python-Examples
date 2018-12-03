import os
root_path = os.getcwd()
offset = len(root_path.split("\\"))

for root,dirs,files in os.walk(root_path):
	current_dir = root.split("\\")
	indent = len(current_dir)-offset
	print("\t"*indent,current_dir[-1])
