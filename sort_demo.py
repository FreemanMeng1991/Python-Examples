class Student:
	def __init__(self,name,grade,age):
		self.name  = name
		self.grade = grade
		self.age   = age
	def __repr__(self):
		return((self.name,self.grade,self.age))


s = [("Tim","A",10),\
("King","A",12),\
("LiTao","B",17),\
("Anne","C",20),\
("Tom","D",15),\
("Tony","D",14),\
("Kim","B",13),\
    ]

def sort_by_age(student):
	return(student[2])

def sort_by_grade(student):
	return(student[1])

def sort_by_name(student):
	return(student[0])

result = sorted(s,key=sort_by_grade)
print(result)
