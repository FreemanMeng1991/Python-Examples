class A(object): 
    def __init__(self): 
        self['B'] = "BB" 
        self['D'] = "DD" 
        del self['D'] 

    def __setitem__(self,name,value): 
        '''''
        @summary: 每当属性被赋值的时候都会调用该方法，
        因此不能再该方法内赋值 self.name = value 会死循环
        ''' 
        print("__setitem__:Set %s Value %s"%(name,value))
        self.__dict__[name] = value 
       
    def __getitem__(self,name): 
        ''''' 
        @summary: 当访问不存在的属性时会调用该方法
        ''' 
        try:
            print(self.__dict__[name])
        except:
            print("__getitem__:No attribute named '%s'"%name)
        return None 
       
    def __delitem__(self,name): 
        ''''' 
        @summary: 当删除属性时调用该方法
        ''' 
        print("__delitem__:Delect attribute '%s'"%name)
        del self.__dict__[name] 
        print(self.__dict__)
             
if __name__ == "__main__": 
    X = A() 
    b = X['Value'] 
