# -*- encoding: utf-8 -*-
import sys
import uuid
import getopt
import pdfkit
from os import walk,remove
from os.path import join,isfile,exists,splitext
from PyPDF2 import PdfFileReader,PdfFileWriter,PdfFileMerger
from win32com.client import Dispatch

wdFormatPDF = 17
file_list   = [] 

pdf_maker = r'D:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe' #安装位置


def printUsage():
	help_info = '''
Something went wrong, check for valid command line parameters:

USEAGE: 
python ./ezp.py [-h | -i <src_folder> | -m | -b]

Where:
-h			   : Show help information.
-m			   : Merge all converted pdf files into one single file.

-b			   : Adjust for both-sides print, files of odd-numbered 
				   pages will be added one blank page in the end.
				   Usually used with "-m" option.

-i <src_folder>  : Specify the <src_folder> which contains the files 
				   to be coverted to pdf.

Examples: 
	   -i C:/Desktop/test -m
	   -i C:/Desktop/test -m -b
	   -i C:/Desktop/test/sample.doc 

No command line parameters will run in interactive mode.
				'''
	print(help_info)
 

#pip instatll win32com
def doc_to_pdf(doc_path,pdf_path):
	"""
	:word文件转pdf
	:param doc_path word文件路径
	:param pdf_path 转换后pdf文件路径
	"""
	word = Dispatch('Word.Application')
	doc = word.Documents.Open(doc_path)
	#doc_name.replace(".doc", ".pdf")
	doc.SaveAs(pdf_path, FileFormat=wdFormatPDF)
	doc.Close()
	word.Quit()
	print("Done!")


def add_blank_page(pdf_file):
	#创建pdf文件读写对象
	pdfFileReader = PdfFileReader(pdf_file) 
	pdfFileWriter = PdfFileWriter()
	#获取页数和页面尺寸
	numPages = pdfFileReader.getNumPages()
	pageObj = pdfFileReader.getPage(0)
	page_width = pageObj.mediaBox.upperRight[0]
	page_height  = pageObj.mediaBox.upperRight[1]
	#将现有页面拷贝到pdf生成器中
	for index in range(0, numPages):
		pageObj = pdfFileReader.getPage(index)
		pdfFileWriter.addPage(pageObj)  # 根据每页返回的 PageObject,写入到文件	
	#创建并向文档中添加空白页
	page = pageObj.createBlankPage(pdf_file,page_width,page_height)
	pdfFileWriter.insertPage(page,index=numPages)
	#另外两种添加空白页的方法
	#pdfFileWriter.addBlankPage()
	#pdfFileWriter.insertBlankPage(page_width,page_height,index=numPages)
	pdfFileWriter.write(open(pdf_file,'wb'))

def add_offset_page(pdf_file,offset_page):
	#创建pdf文件读写对象
	offset        = PdfFileReader(offset_page).getPage(0)
	pdfFileReader = PdfFileReader(pdf_file) 
	pdfFileWriter = PdfFileWriter()
	#获取当前pdf页数
	numPages = pdfFileReader.getNumPages()
	#将现有页面拷贝到pdf生成器中
	for index in range(0, numPages):
		pageObj = pdfFileReader.getPage(index)
		pdfFileWriter.addPage(pageObj)  # 根据每页返回的 PageObject,写入到文件	
	
	pdfFileWriter.insertPage(offset,index=numPages)
	pdfFileWriter.write(open(pdf_file,'wb'))

def merge_pdf_file(src_folder,both_sides=False,offset_file=None):
	"""
	:合并pdf文件
	:param src_folder   含有pdf文件的文件夹
	:param both_sides   若为True，则针对双面打印进行调整，
	:				    奇数页的pdf文件末尾自动加一页调整页
	:param offset_file  若both_sides为True，则此项必选，
	:				    该参数指向调整页文件的路径
	"""
	file_list = []
	pdfMaker = PdfFileMerger()
	#遍历文件夹找出所有pdf文件
	for root,dirs,files in walk(src_folder):
		for f in files:
			if(f.endswith(".pdf")):
				file_list.append(join(root,f)) 
			else:
				pass #忽略非pdf文件
	output_file = join(src_folder,"Bind.pdf")
	if exists(output_file):
		print("A file named \"Bind.pdf\" already in %s\n"%src_folder)
		while(1):
			option = input("Would you want to DELETE it and continue? (y/n)\n")
			if(option.lower()=='y'):
				remove(output_file)
				merge_pdf_file(src_folder,both_sides)
				break
			if(option.lower()=='n'):
				print("Program Terminated!\nRemove or rename the Bind.pdf file then continue.")
				break
			else:
				print("Key in y(Y) or n(N) only!\n")
		return
	#将所有pdf文件合并并写入文件
	#print(file_list)
	if(both_sides):
		for file in file_list:
			if(file == offset_file):
				print("pass")
				continue
			#创建pdf文件读写对象
			pdfFileReader = PdfFileReader(file) 
			#获取页数和页面尺寸
			numPages = pdfFileReader.getNumPages()
			if(numPages%2):
				add_offset_page(file,offset_file)
			pdf = pdfMaker.append(open(file,"rb"))
	else:
		for file in file_list:
			pdf = pdfMaker.append(open(file,"rb"))
	pdf = open(output_file,"wb")
	pdfMaker.write(pdf)
	print("All pdf files have been combined and saved in:\n%s"%output_file)

def create_offset_page(output_file,pdf_maker):
	"""
	Create pdf files from plain text or HTML text.
	output_file : File path to the offset pdf file for both-side printout
	pdf_maker   : Path to wkhtmltopdf.exe
	"""
	if (not exists(pdf_maker)):
		print("Invalid path to wkhtmltopdf.exe, please check")
		return
	print("Creating pages for both-sides printout adjustment ...")
	config   = pdfkit.configuration(wkhtmltopdf = pdf_maker)
	contents = """."""
	options  = {
				'page-size':'A4',
				'margin-top':'0.001',
				'margin-left':'0.001',
				'encoding':"UTF-8",
				}
	pdfkit.from_string(contents,output_file, configuration=config, options=options) 


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

def get_options():
	options = {"src_folder":None,"src_type":None,"merge":None,"both_sides":None}
	collected_opt = []
	#print(sys.argv,len(sys.argv[1:]))
	if(len(sys.argv[1:])):
		try:
			opts, args = getopt.getopt(sys.argv[1:],"hi:mb")
		except getopt.GetoptError:
			printUsage()
			sys.exit(-1)
		for opt, arg in opts: collected_opt.append(opt)

		if("-i" in collected_opt):
			options["src_folder"] = opts[collected_opt.index("-i")][1]
			result = check_path(options["src_folder"])
			if (result==False):
				sys.exit(-1)
			else:
				options["src_type"] = result
		else:
			options["src_folder"] = None

		if(options["src_type"]=="file"):return

		if("-m" in collected_opt):
			options["merge"] = 'y'
		else:
			options["merge"] = 'n'

		if("-b" in collected_opt):
			options["both_sides"] = 'y'
		else:
			options["both_sides"] = 'n'
	else:
		while (1):
			if(not options["src_folder"]):
				options["src_folder"] = input("Specify source file or directory:\n")
				options["src_type"] = check_path(options["src_folder"])
			if(check_path(options["src_folder"])):
				break
			else:
				options["src_folder"] = input("Specify source file or directory:\n")
				options["src_type"] = check_path(options["src_folder"])
		if(options["src_type"]=="file"):return

		while (1):
			if(not options["merge"]):
				option = input("Merge all pdf files in a singel file? (y/n)   ")
				#错误示例：以下判断会造成逻辑表达式短路，无法输入n选项
				#if(option.lower()!='y' or option.lower()!='n'): 
				if(option.lower()=='y'):
					options["merge"] = option
					break
				if(option.lower()=='n'):
					options["merge"] = option
					break
				else:
					print("Key in y(Y) or n(N) only!")
			else:
				break

		while (1):
			if(not options["both_sides"]):
				option = input("Optimize for both-sides print out? (y/n)   ")
				if(option.lower()=='y'):
					options["both_sides"] = option
					break
				if(option.lower()=='n'):
					options["both_sides"] = option
					break
				else:
					print("Key in y(Y) or n(N) only!\n")
			else:
				break
	return options

if __name__=='__main__':
	options = get_options()
	#遍历并过滤文件夹中的Word或Excel文件
	
	if (options["both_sides"]):
		 pass
	if (options["src_type"] == "file"):
		file_name = options["src_folder"].split("\\")[-1]
		print("Converting: "+file_name+" ...")
		doc_to_pdf(path,path.replace())
	if (options["src_type"] == "folder"):
		for root,dirs,files in walk(options["src_folder"]):
			for f in files:
				if(f.startswith("~$") or not f.endswith(('.xls','.xlsx','doc','docx'))):
					pass  #忽略临时文件和其他文件
				else:
					file_list.append(join(root,f)) #保存所有文件绝对路径到一个列表中
		print("%d files found in the specified directory."%len(file_list))

		for doc_path in file_list:
			doc_name = doc_path.split("\\")[-1]
			print("Converting: "+doc_name+" ...")
			pdf_name = doc_name.split(".")[0]+".pdf"
			doc_to_pdf(doc_path,options["src_folder"]+"\\"+pdf_name)
	
	if(options["merge"]=='y' and options["src_type"]=="folder"):
		if(options["both_sides"]=='y'):
			offset_file = options["src_folder"]+"\\"+uuid.uuid4().hex+".pdf" #随机生成文件名
			create_offset_page(offset_file,pdf_maker)
			merge_pdf_file(options["src_folder"],both_sides=1,offset_file=offset_file)
			remove(offset_file)
		else:
			merge_pdf_file(options["src_folder"])
