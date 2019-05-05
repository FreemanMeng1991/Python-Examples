#批量重命名指定目录下的所有文件
#目录由变量src_dir指定
import os,re

src_dir = r"E:\教学资料\学生作业\物联网通信技术\第一次"
files = os.listdir(src_dir)

for f in files:
	split = os.path.splitext(f)
	filename = split[0]
	filetype = split[1]
    #匹配一个或多个数字
	student_id = re.findall("\d+",filename)
	#匹配一个或多个汉字
	student_name = re.findall("[\u4E00-\u9FA5]+",filename) 
	src = os.path.join(src_dir,f)
	new_name = student_id[0]+"_"+student_name[0]+"_第一次"+filetype
	dst = os.path.join(src_dir,new_name)
	os.rename(src,dst)
