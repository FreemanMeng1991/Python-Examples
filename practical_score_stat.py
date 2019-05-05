import xlrd
import matplotlib.pyplot as plt
data  = xlrd.open_workbook(r"real_score_book.xlsx")
print(dir(data))
sheets = data.sheet_names()
print(sheets)
grades = ("< 60","60-69","70-79","80-89","90-100")
grade_A,grade_B,grade_C,grade_D,failing = 0,0,0,0,0
for sheet in sheets:
	class_name = sheet
	table = data.sheet_by_name(class_name)
	cols  = table.ncols #工作表列数
	rows  = table.nrows #工作表行数
	print(sheet)
	col_data = table.col_values
	scores = (col_data(7,5,-5)+col_data(15,5,-5))
	print(scores)
	for score in scores:
		#数据有效性验证
		if type(score)== str or score<0 or score>100:
			continue
		if score<60:  
			failing+=1 # 0 -- 59
		if score>=60 and score<70:  
			grade_D+=1 # 60 -- 69
		if score>=70 and score<80:
			grade_C+=1 # 70 -- 79
		if score>=80 and score<90:
			grade_B+=1 # 80 -- 89
		if score>=90 and score<100:
			grade_A+=1 # 90 -- 10
	total = sum([failing,grade_D,grade_C,grade_B,grade_A])
	sections = (failing,grade_D,grade_C,grade_B,grade_A)
	print(class_name,failing,grade_D,grade_C,grade_B,grade_A,total)
	grade_A,grade_B,grade_C,grade_D,failing = 0,0,0,0,0 #清零计数器
    
    #绘制分数段柱状图
	plt.figure(sheet)
	plt.ylabel("人数")
	plt.title(class_name+'班分数段统计')
	# plt.xticks(ind)
	plt.xticks(range(5),grades)
	chart = plt.bar(range(5),sections, width=0.45)
	for rect,x in zip(chart,range(5)):
		height = rect.get_height()
		print(height,rect.get_x(),rect.get_width())
		plt.text(x-0.05,height+0.1,sections[x],fontsize=14, family='SimHei')

    #绘制分数散点图
	# num = range(total)
	# plt.figure(class_name)
	# plt.scatter(num, scores[:total])
	# plt.xlabel('分数', fontsize=12)
	# plt.ylabel('学号', fontsize=12)
	# plt.title(class_name+'班分数统计(按学号)')
	
plt.pause(0)
	
