#根据期末成绩反推5次平时成绩，都是5的倍数
import sys
import xlrd
import xlwt
import getopt
from os import walk
from random import randint
from xlutils.copy import copy
from itertools import permutations,combinations
from os.path import join,isfile,exists,dirname

def printUsage():
	help_info = '''
Something went wrong, check for valid command line parameters:

USEAGE: 
python ./scrvar.py [-h | -i <src>]

Where:
-h		: Show help information.

-i <src> : Specify the <src> folder or <src> file
			which contains the excel files for score balance. 

Examples: 
		-h
		-i C:/Desktop/test
		-i C:/Desktop/test/sample.xls

				'''
	print(help_info)

#检查文件路径是否合法，并判定该路径指向目录还是文件
def check_path(path):
	if isfile(path):
		print("1 File found.")
		check = "file"
	elif exists(path):
		print("1 Folder found.")
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

def create_variance():	
	#根据不同的分数尾数，生成不同的分数调整序列，使其为5的倍数
	balance_set = set()
	balance_dict = {}
	keys = ["bal_0_5","bal_1_6","bal_2_7","bal_3_8","bal_4_9"]
	base_bal = [[-5,5,-5,5,0],[-1,-1,-1,-1,4],
				[-2,-2,-2,3,3],[2,2,2,-3,-3],
				[1,1,1,1,-4]
				]
	for n, bal in enumerate(base_bal):
		#算出base_bal中每个列表的全排列并保存至字典中
		for p in permutations(bal): 
			balance_set.add(p) #去除permutations产生的重复元素
		balance_dict[keys[n]] = list(balance_set)
		balance_set.clear() #清空，为下一个列表的全排列做准备

	return balance_dict

def str_to_int(string):
	score = string
	if type(string)==str:
		score = int(string)
	return score

def set_style(font_name="SimSun",font_size=10,
	          align_H = xlwt.Alignment.HORZ_CENTER,
	          align_V = xlwt.Alignment.VERT_CENTER,
	          border_style = xlwt.Borders.THIN):
	#创建单元格样式对象，存储样式信息
	style = xlwt.XFStyle() 
	#设置样式信息
	font = xlwt.Font() #参见formatting.py中的Font类
	font.name = font_name
	font.height = font_size*20

	borders = xlwt.Borders()#参见formatting.py中的Borders类
	borders.left   = border_style
	borders.right  = border_style
	borders.up     = border_style
	borders.bottom = border_style

	alignment = xlwt.Alignment()
	alignment.horz = align_H
	alignment.vert = align_V

	#写入样式信息
	style.borders   = borders
	style.font      = font
	style.alignment = alignment

	return style


def set_scores(file,balance_dict):
	data	    = xlrd.open_workbook(file)
	sheets	    = data.sheet_names()
	start_row   = 4 #从start_row行开始读取学生分数
	#拷贝一份带有格式的工作表供写入结算结果
	new_excel   = copy(xlrd.open_workbook(file,formatting_info=True))
	write_sheet = new_excel.get_sheet(0)
	for sheet in sheets:
		table = data.sheet_by_name(sheet)
		cols  = table.ncols #工作表列数
		rows  = table.nrows #工作表行数
		col_data  = table.col_values
		#将所有分数转为数字
		scores = list(map(str_to_int,col_data(cols-1,4,rows-2)))
		for score in scores: #调整分数
			mod = score%10
			base   = [score]*5 #向量化平均成绩，共5次
			if(mod == 0 or mod == 5):
				#0和100保持不变
				if(score == 100 or score == 0):
					offset = base
				else:
					offset = list(map(lambda x,y:x+y,
						 base,balance_dict["bal_0_5"][randint(0,len(balance_dict["bal_0_5"])-1)]))
			if(mod == 1 or mod == 6):
				offset = list(map(lambda x,y:x+y,
						 base,balance_dict["bal_1_6"][randint(0,len(balance_dict["bal_1_6"])-1)]))
			if(mod == 2 or mod == 7):
				offset = list(map(lambda x,y:x+y,
						 base,balance_dict["bal_2_7"][randint(0,len(balance_dict["bal_2_7"])-1)]))
			if(mod == 3 or mod == 8):
				offset = list(map(lambda x,y:x+y,
						 base,balance_dict["bal_3_8"][randint(0,len(balance_dict["bal_3_8"])-1)]))
			if(mod == 4 or mod == 9):
				offset = list(map(lambda x,y:x+y,
						 base,balance_dict["bal_4_9"][randint(0,len(balance_dict["bal_4_9"])-1)]))

			for index,value in enumerate(offset):
				write_sheet.write(start_row,index+3,value,set_style())
			start_row+=1

	new_excel.save(file)


if __name__ == '__main__':
	options  = get_options()
	balance_dict = create_variance()
	
	#遍历并过滤文件夹中的xls成绩文件，并将其绝对路径添加在列表中
	file_list=[]
	if (options["src_type"] == "file"):
		if(options["src_type"].endswith(("xls","xlsx"))):
			file_list.append(options['src'])
		else:
			print("Error: Must be a txt file!")
			printUsage()
			exit(-1)
	if (options["src_type"] == "folder"):
		for root,dirs,files in walk(options["src"]):
			for f in files:
				if(f.startswith("~$") or not f.endswith(("xls","xlsx"))):
					pass  #忽略临时文件和其他文件
				else:
					#保存所有文件绝对路径到一个列表中
					file_list.append(join(root,f)) 
		print("%d Excel files found in the specified directory."%len(file_list))
	
 	#遍历并计算所有原始成绩文件
	for file in file_list:
		set_scores(file,balance_dict)
	print("\nDone! %d Excel files has been processed!"%len(file_list))