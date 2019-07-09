# -*- encoding: utf-8 -*-
#该程序统计一个文件夹下所有的学生成绩文件
#文件格式为：一个班一个TXT文件，每个学生成绩占一行，
#           每题的分数用空格分隔。
import sys
import xlrd
import xlwt
import getopt
from os import walk
from os.path import join,isfile,exists,dirname

Workbook=xlwt.Workbook(encoding='utf-8')

def printUsage():
	help_info = '''
Something went wrong, check for valid command line parameters:

USEAGE: 
python ./sst.py [-h | -i <src>]

Where:
-h       : Show help information.

-i <src> : Specify the <src> folder or <src> file
           which contains the txt files for score caculation. 

Examples: 
	   -h
	   -i C:/Desktop/test
	   -i C:/Desktop/test/score_sample.txt

				'''
	print(help_info)
 
#检查文件路径是否合法，并判定该路径指向目录还是文件
def check_path(path):
	if isfile(path):
		print("1 File found.\n")
		check = "file"
	elif exists(path):
		print("1 Folder found.\n")
		check = "folder"
	else:
		print("No such file or directory found, please check!\n")
		check = False
	return check

#从命令行获取参数
def get_options():
	options = {"src":None,"src_type":None}
	collected_opt = []
	#print(sys.argv,len(sys.argv[1:]))
	if(len(sys.argv[1:])):
		try:
			opts, args = getopt.getopt(sys.argv[1:],"hi:")
		except getopt.GetoptError:
			printUsage()
			sys.exit(-1)
		for opt, arg in opts: collected_opt.append(opt)
		if("-h" in collected_opt):printUsage()
		if("-i" in collected_opt):
			options["src"] = opts[collected_opt.index("-i")][1]
			result = check_path(options["src"])
			if (result==False):
				sys.exit(-1)
			else:
				options["src_type"] = result	
	else:
		printUsage()
	return options

#将一个成绩TXT文件中的所有数据保存在一个二维列表中
def save_as_list(file_path):
	scores = []
	with open(file_path) as fp:
		while(1):
			record = fp.readline().strip()
			if(len(record)):
				temp = []
				#将每个学生的成绩保存为一个列表
				for score in record.split(" "):
					temp.append(int(score))
				scores.append(temp)
			else:
				break
	return scores

#计算每个学生的总分并将计算结果保存在Excel文件中
def caculate_and_save(scores,file_name,work_book=Workbook):
	start_row = 1
	new_sheet = work_book.add_sheet(file_name) #每个文件单独一个工作表
	#添加表头
	new_sheet.write(0,0,"学号")
	for index in range(len(scores[0])):
		label = "第%d大题"%(index+1)
		new_sheet.write(0,index+1,label)
	new_sheet.write(0,len(scores[0])+1,"总分")

	#计算每个学生的总分
	for score in scores:
		score.append(sum(score))
		new_sheet.write(start_row,0,start_row)
		for index,value in enumerate(score):
			new_sheet.write(start_row,index+1,value)
		start_row+=1

		
if __name__=='__main__':
	options = get_options()
	#遍历并过滤文件夹中的txt成绩文件，并将其绝对路径添加在列表中
	file_list=[]
	if (options["src_type"] == "file"):
		if(options["src_type"].endswith("txt")):
			file_list.append(options['src'])
		else:
			print("Error: Must be a txt file!")
			printUsage()
			exit(-1)
	if (options["src_type"] == "folder"):
		for root,dirs,files in walk(options["src"]):
			for f in files:
				if(f.startswith("~$") or not f.endswith(('.txt'))):
					pass  #忽略临时文件和其他文件
				else:
				    #保存所有文件绝对路径到一个列表中
					file_list.append(join(root,f)) 
		print("%d files found in the specified directory."%len(file_list))
    
    #遍历并计算所有原始成绩文件
	for file in file_list:
		s = save_as_list(file)
		file_name =  file.split("\\")[-1]
		caculate_and_save(s,file_name)

	#生成计算结果的存储路径	
	if(options["src_type"] == 'folder'):
		output_path = options['src']
	else:
		output_path = dirname(options['src'])[:]

	#保存计算结果并提示保存位置
	Workbook.save(output_path+"\\"+"results.xls")
	print("Caculation results has been saved in:\n%s"%output_path)
	
