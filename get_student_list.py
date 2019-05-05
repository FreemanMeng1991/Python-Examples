import xlrd
import xlwt
data  = xlrd.open_workbook(r"real_score_book.xlsx")
#print(dir(data))
sheets = []
#print(sheets)
workbook =  xlwt.Workbook()
table_header = ["考号","学号","姓名","第一题","第二题","第三题"]
style = xlwt.XFStyle()
print(dir(style))
for sheet in data.sheet_names():
	class_name = sheet
	table = data.sheet_by_name(class_name)
	col_data = table.col_values
	exam_ids = (col_data(1,5,-5)+col_data(9,5,-5))
	student_ids = (col_data(2,5,-5)+col_data(10,5,-5))
	student_names = (col_data(3,5,-5)+col_data(11,5,-5))
	#print(exam_ids,student_ids,student_names)
	new_sheet = workbook.add_sheet(class_name)
	for index,value in enumerate(table_header):
			new_sheet.write(0,index,label=value)
	for row,e_id,s_id,s_name in zip(range(len(exam_ids)),exam_ids,student_ids,student_names):
		new_sheet.write(row+1,0,label=e_id)
		new_sheet.write(row+1,1,label=s_id)
		new_sheet.write(row+1,2,label=s_name)
	new_sheet.col(1).width = 256*20 #便于学号显示完全

workbook.save("student_list.xls")
'''Columns have a property for setting the width. 
The value is an integer specifying the size measured 
in 1/256 of the width of the character ‘0’ as it appears 
in the sheet’s default font. xlwt creates columns with a 
default width of 2962, roughly equivalent to 11 characters wide.'''